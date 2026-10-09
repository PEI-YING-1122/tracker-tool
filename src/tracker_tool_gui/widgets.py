from typing import NamedTuple

from PySide6.QtCore import QRegularExpression, Signal
from PySide6.QtGui import QGuiApplication, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


NATIVE_FILE_FILTER = "Text files (*.txt);;All files (*)"

ARTIST_IMPORT_NOTE = (
    "Artist Import: NOT VERIFIED. A successful conversion does not prove "
    "that the target software accepts the file. Import it into the target "
    "software to verify."
)


class ShotFieldValues(NamedTuple):
    image_width: int | None
    image_height: int | None
    production_start_frame: int | None
    production_end_frame: int | None


def _integer_field(parent):
    field = QLineEdit(parent)
    # Type-level input check only: an optional minus sign and digits.
    # Value ranges (e.g. width > 0, end >= start) are validated by Core.
    field.setValidator(
        QRegularExpressionValidator(
            QRegularExpression(r"-?[0-9]*"),
            field,
        )
    )
    return field


def _integer_or_none(text: str) -> int | None:
    if text == "":
        return None

    return int(text)


class ShotFields(QWidget):
    """Shot metadata input.

    An empty field means "not provided" and is passed to Core as None, so
    Core reports MISSING_REQUIRED_SHOT_METADATA where it applies.
    """

    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QFormLayout(self)

        self.width_field = _integer_field(self)
        self.height_field = _integer_field(self)
        self.start_frame_field = _integer_field(self)
        self.end_frame_field = _integer_field(self)
        self.end_frame_unknown = QCheckBox("Unknown", self)

        end_frame_row = QHBoxLayout()
        end_frame_row.addWidget(self.end_frame_field)
        end_frame_row.addWidget(self.end_frame_unknown)

        layout.addRow("Width", self.width_field)
        layout.addRow("Height", self.height_field)
        layout.addRow("Start frame", self.start_frame_field)
        layout.addRow("End frame", end_frame_row)

        for field in self._fields():
            field.textChanged.connect(self.changed)

        self.end_frame_unknown.toggled.connect(self._on_end_frame_unknown)

    def _fields(self):
        return (
            self.width_field,
            self.height_field,
            self.start_frame_field,
            self.end_frame_field,
        )

    def _on_end_frame_unknown(self, unknown: bool) -> None:
        if unknown:
            self.end_frame_field.clear()

        self.end_frame_field.setEnabled(not unknown)
        self.changed.emit()

    def has_incomplete_input(self) -> bool:
        # A lone "-" is accepted while typing but is not an integer.
        return any(
            not field.hasAcceptableInput()
            or field.text() == "-"
            for field in self._fields()
        )

    def values(self) -> ShotFieldValues:
        if self.has_incomplete_input():
            raise ValueError("Shot fields contain incomplete input")

        return ShotFieldValues(
            image_width=_integer_or_none(self.width_field.text()),
            image_height=_integer_or_none(self.height_field.text()),
            production_start_frame=_integer_or_none(
                self.start_frame_field.text()
            ),
            production_end_frame=_integer_or_none(
                self.end_frame_field.text()
            ),
        )


def _open_file_dialog(parent, caption, directory):
    path, _ = QFileDialog.getOpenFileName(
        parent,
        caption,
        directory,
        NATIVE_FILE_FILTER,
    )
    return path


def _save_file_dialog(parent, caption, directory):
    path, _ = QFileDialog.getSaveFileName(
        parent,
        caption,
        directory,
        NATIVE_FILE_FILTER,
    )
    return path


class PathField(QWidget):
    """A file path with a Browse button.

    The path is passed on exactly as entered or chosen.
    """

    changed = Signal()
    chosen = Signal(str)

    def __init__(
        self,
        caption,
        mode="open",
        dialog=None,
        start_directory=None,
        parent=None,
    ):
        super().__init__(parent)

        if mode not in ("open", "save"):
            raise ValueError(f"Unsupported path field mode: {mode}")

        self._caption = caption
        self._start_directory = start_directory or (lambda: "")
        self._dialog = dialog or (
            _open_file_dialog if mode == "open" else _save_file_dialog
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.path_edit = QLineEdit(self)
        self.browse_button = QPushButton("Browse…", self)

        layout.addWidget(self.path_edit)
        layout.addWidget(self.browse_button)

        self.path_edit.textChanged.connect(self.changed)
        self.browse_button.clicked.connect(self._browse)

    def _browse(self) -> None:
        path = self._dialog(
            self,
            self._caption,
            self._start_directory(),
        )

        if path:
            self.path_edit.setText(path)
            self.chosen.emit(path)

    def path(self) -> str:
        return self.path_edit.text()


class ResultPanel(QWidget):
    """Presents the outcome of the last conversion.

    It only displays what it is given. Deciding what an outcome means is
    not its job.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.heading = QLabel(self)
        self.message = QLabel(self)
        self.message.setWordWrap(True)
        self.note = QLabel(self)
        self.note.setWordWrap(True)
        self.details = QPlainTextEdit(self)
        self.details.setReadOnly(True)
        self.copy_diagnostics_button = QPushButton("Copy diagnostics", self)
        self.copy_diagnostics_button.clicked.connect(self._copy_diagnostics)

        layout.addWidget(self.heading)
        layout.addWidget(self.message)
        layout.addWidget(self.note)
        layout.addWidget(self.details)
        layout.addWidget(self.copy_diagnostics_button)

        self._diagnostics = ""
        self.show_idle()

    def _show(self, heading, message="", note="", details="", diagnostics=""):
        self.heading.setText(heading)
        self.message.setText(message)
        self.note.setText(note)
        self.note.setVisible(bool(note))
        self.details.setPlainText(details)
        self.details.setVisible(bool(details))
        self._diagnostics = diagnostics
        self.copy_diagnostics_button.setVisible(bool(diagnostics))

    def diagnostics(self) -> str:
        return self._diagnostics

    def _copy_diagnostics(self) -> None:
        QGuiApplication.clipboard().setText(self._diagnostics)

    def show_idle(self, message="") -> None:
        self._show("", message)

    def show_busy(self) -> None:
        self._show("Converting…")

    def show_success(self, output_path, diagnostics="") -> None:
        self._show(
            "PASS",
            f"Written to {output_path}",
            ARTIST_IMPORT_NOTE,
            diagnostics=diagnostics,
        )

    def show_failure(self, heading, message, details="", diagnostics="") -> None:
        self._show(
            f"FAIL — {heading}",
            message,
            details=details,
            diagnostics=diagnostics,
        )
