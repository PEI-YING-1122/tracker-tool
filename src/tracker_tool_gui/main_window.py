from importlib import metadata

from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tracker_tool_gui.preferences import Preferences
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

CORE_INTEGRATION_PENDING = (
    "Conversion is not available yet: the GUI is not connected to the "
    "Tracker Tool Core."
)

# Source and Target choices come from tracker_tool.contract, which is
# added with the Core integration boundary (phase P1).
SOFTWARE_SELECTION_PENDING = (
    "Software selection becomes available with the Core integration."
)

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

        central = QWidget(self)
        layout = QVBoxLayout(central)

        self.sections: dict[str, QGroupBox] = {}

        for title in SECTION_TITLES:
            section = QGroupBox(title, central)
            QVBoxLayout(section)
            layout.addWidget(section)
            self.sections[title] = section

        for title in ("Source", "Target"):
            placeholder = QLabel(
                SOFTWARE_SELECTION_PENDING,
                self.sections[title],
            )
            placeholder.setWordWrap(True)
            self.sections[title].layout().addWidget(placeholder)

        self.shot_fields = ShotFields(self.sections["Shot"])
        self.sections["Shot"].layout().addWidget(self.shot_fields)

        self.output_path = PathField(
            "Choose output file",
            mode="save",
            start_directory=lambda: self.preferences.directory("output"),
            parent=self.sections["Output"],
        )
        self.output_path.chosen.connect(
            lambda path: self.preferences.remember_file("output", path)
        )
        self.sections["Output"].layout().addWidget(self.output_path)

        self.result_panel = ResultPanel(self.sections["Result"])
        self.sections["Result"].layout().addWidget(self.result_panel)
        self.result_panel.show_idle(CORE_INTEGRATION_PENDING)

        self.convert_button = QPushButton("Convert", central)
        self.convert_button.setToolTip(CORE_INTEGRATION_PENDING)
        layout.addWidget(self.convert_button)

        self.setCentralWidget(central)

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

    def _update_convert_enabled(self) -> None:
        # Enabled only once the GUI is connected to Core (phase P1).
        self.convert_button.setEnabled(False)

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
