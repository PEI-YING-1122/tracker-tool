from importlib import metadata

from PySide6.QtWidgets import (
    QGroupBox,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tracker_tool import app
from tracker_tool.config import ShotConfig
from tracker_tool_gui.diagnostics import format_diagnostics
from tracker_tool_gui.preferences import Preferences
from tracker_tool_gui.results import describe_failure
from tracker_tool_gui.selection import SourceSection, TargetSection
from tracker_tool_gui.widgets import PathField, ResultPanel, ShotFields
from tracker_tool_gui.worker import TaskRunner


WINDOW_TITLE = "Tracker Tool"

# Section order follows docs/gui/GUI_DEVELOPMENT_PLAN.md §6.
SECTION_TITLES = (
    "Source",
    "Target",
    "Shot",
    "Output",
    "Result",
)

READY_MESSAGE = "Choose source, target, shot metadata and output, then Convert."
BUSY_STATUS = "Converting…"


def installed_core_version() -> str:
    try:
        return metadata.version("tracker-tool")
    except metadata.PackageNotFoundError:
        return "unknown"


class MainWindow(QMainWindow):
    def __init__(self, parent=None, runner=None, preferences=None):
        super().__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)

        self.preferences = preferences or Preferences()
        self.runner = runner or TaskRunner(self)
        self.runner.busy_changed.connect(self._on_busy_changed)
        self.runner.succeeded.connect(self._on_succeeded)
        self.runner.failed.connect(self._on_failed)

        central = QWidget(self)
        layout = QVBoxLayout(central)

        self.sections: dict[str, QGroupBox] = {}

        for title in SECTION_TITLES:
            section = QGroupBox(title, central)
            QVBoxLayout(section)
            layout.addWidget(section)
            self.sections[title] = section

        self.source = SourceSection(
            start_directory=lambda: self.preferences.directory("input"),
            parent=self.sections["Source"],
        )
        self.sections["Source"].layout().addWidget(self.source)

        self.target = TargetSection(self.sections["Target"])
        self.sections["Target"].layout().addWidget(self.target)

        self.shot_fields = ShotFields(self.sections["Shot"])
        self.sections["Shot"].layout().addWidget(self.shot_fields)

        self.output_path = PathField(
            "Choose output file",
            mode="save",
            start_directory=lambda: self.preferences.directory("output"),
            parent=self.sections["Output"],
        )
        self.sections["Output"].layout().addWidget(self.output_path)

        self.result_panel = ResultPanel(self.sections["Result"])
        self.sections["Result"].layout().addWidget(self.result_panel)
        self.result_panel.show_idle(READY_MESSAGE)

        self.convert_button = QPushButton("Convert", central)
        layout.addWidget(self.convert_button)

        self.setCentralWidget(central)

        self.source.changed.connect(self._on_source_changed)
        self.source.input_chosen.connect(
            lambda path: self.preferences.remember_file("input", path)
        )
        self.target.changed.connect(self._update_convert_enabled)
        self.shot_fields.changed.connect(self._update_convert_enabled)
        self.output_path.changed.connect(self._update_convert_enabled)
        self.output_path.chosen.connect(
            lambda path: self.preferences.remember_file("output", path)
        )
        self.convert_button.clicked.connect(self.start_conversion)

        self._request_context = []
        self._request_output = ""

        self._idle_status = f"tracker-tool {installed_core_version()}"
        self._update_convert_enabled()
        self.statusBar().showMessage(self._idle_status)

        geometry = self.preferences.window_geometry()

        if geometry is not None:
            self.restoreGeometry(geometry)

    def closeEvent(self, event) -> None:
        self.preferences.save_window_geometry(self.saveGeometry())
        self.preferences.sync()
        super().closeEvent(event)

    def _input_sections(self):
        return [
            section
            for title, section in self.sections.items()
            if title != "Result"
        ]

    def _on_source_changed(self) -> None:
        self.target.set_source(self.source.software_id())
        self._update_convert_enabled()

    def can_convert(self) -> bool:
        return (
            not self.runner.busy
            and self.source.is_complete()
            and self.target.is_complete()
            and not self.shot_fields.has_incomplete_input()
            and bool(self.output_path.path())
        )

    def _update_convert_enabled(self) -> None:
        self.convert_button.setEnabled(self.can_convert())

    def _request(self):
        """Build the Core call for the current form, and its context.

        All validation of the values (ranges, same-source, software IDs)
        is done by Core.
        """

        values = self.shot_fields.values()
        source = self.source.software_id()
        target = self.target.software_id()
        output = self.output_path.path()

        shot_config = ShotConfig(
            image_width=values.image_width,
            image_height=values.image_height,
            production_start_frame=values.production_start_frame,
            production_end_frame=values.production_end_frame,
            source_software=source,
            target_software=target,
        )

        context = [
            ("Source", source),
            ("Target", target),
        ]

        if self.source.is_source_set():
            autotrack = self.source.autotrack_path.path()
            usertrack = self.source.usertrack_path.path()
            context += [
                ("Mode", "PFTrack source set"),
                ("AutoTrack input", autotrack),
                ("UserTrack input", usertrack),
            ]

            def job():
                app.convert_pftrack_source_set_files(
                    autotrack,
                    usertrack,
                    output,
                    shot_config,
                )

        else:
            input_path = self.source.input_path.path()
            role = self.source.role_id()
            context += [
                ("PFTrack source role", role),
                ("Input", input_path),
            ]

            def job():
                app.convert_file(
                    input_path,
                    output,
                    shot_config,
                    pftrack_source_role=role,
                )

        context += [
            ("Output", output),
            ("Width", values.image_width),
            ("Height", values.image_height),
            ("Start frame", values.production_start_frame),
            ("End frame", values.production_end_frame),
        ]

        return job, context, output

    def start_conversion(self) -> None:
        if not self.can_convert():
            return

        job, self._request_context, self._request_output = self._request()
        self.runner.start(job)

    def _on_succeeded(self, _result) -> None:
        self.result_panel.show_success(
            self._request_output,
            diagnostics=format_diagnostics(self._request_context),
        )

    def _on_failed(self, exc) -> None:
        failure = describe_failure(exc)
        self.result_panel.show_failure(
            failure.heading,
            failure.message,
            details=failure.details,
            diagnostics=format_diagnostics(self._request_context, exc),
        )

    def _on_busy_changed(self, busy: bool) -> None:
        for section in self._input_sections():
            section.setEnabled(not busy)

        if busy:
            self.convert_button.setEnabled(False)
            self.result_panel.show_busy()
            self.statusBar().showMessage(BUSY_STATUS)
        else:
            self._update_convert_enabled()
            self.statusBar().showMessage(self._idle_status)
