from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QRadioButton,
    QWidget,
)

from tracker_tool.contract import (
    PFTRACK_SOURCE_ROLE_AUTOTRACK,
    PFTRACK_SOURCE_ROLE_USERTRACK,
    PFTRACK_SOURCE_ROLES,
    SOFTWARE_3DE_R5,
    SOFTWARE_PFTRACK_2017,
    SOFTWARE_SYNTHEYES_2304,
    SUPPORTED_SOFTWARE,
)
from tracker_tool_gui.widgets import PathField


# Presentation only: product names shown next to the formal IDs. The IDs
# themselves come from tracker_tool.contract.
SOFTWARE_LABELS = {
    SOFTWARE_3DE_R5: "3DEqualizer R5",
    SOFTWARE_PFTRACK_2017: "PFTrack 2017",
    SOFTWARE_SYNTHEYES_2304: "SynthEyes 2304",
}

ROLE_LABELS = {
    PFTRACK_SOURCE_ROLE_AUTOTRACK: "AutoTrack",
    PFTRACK_SOURCE_ROLE_USERTRACK: "UserTrack",
}

PLACEHOLDER = "Select…"

SAME_AS_SOURCE_TOOLTIP = (
    "Source and target must be different software. Tracker Tool converts "
    "between applications; it does not rewrite a file for the same "
    "application."
)


def _labelled(identifier, labels):
    return f"{labels[identifier]} ({identifier})"


class ChoiceBox(QComboBox):
    """Combo box with a placeholder and a fixed list of identifiers.

    The identifiers are kept on the Python side instead of in Qt item data,
    and item tooltips are always strings. Passing None through Qt item data
    and bool through QFormLayout.setRowVisible corrupts the reference count
    of None / True in the PySide6 6.12 Linux build (Fatal Python error at
    interpreter exit, seen in CI), so the GUI avoids both.
    """

    def __init__(self, identifiers, labels, parent=None):
        super().__init__(parent)

        self._values = [None, *identifiers]
        self.addItem(PLACEHOLDER)

        for identifier in identifiers:
            self.addItem(_labelled(identifier, labels))

        for index in range(self.count()):
            self.setItemData(index, "", Qt.ItemDataRole.ToolTipRole)

    def values(self) -> list:
        return list(self._values)

    def value(self):
        index = self.currentIndex()
        return self._values[index] if index >= 0 else None

    def index_of(self, value) -> int:
        return self._values.index(value)

    def select(self, value) -> None:
        self.setCurrentIndex(self.index_of(value))


class SourceSection(QWidget):
    """Source software, PFTrack mode and role, and input file(s)."""

    changed = Signal()
    input_chosen = Signal(str)

    def __init__(self, start_directory=None, parent=None):
        super().__init__(parent)

        layout = QFormLayout(self)

        self.software = ChoiceBox(SUPPORTED_SOFTWARE, SOFTWARE_LABELS, self)

        self.single_file_mode = QRadioButton("Single file", self)
        self.source_set_mode = QRadioButton(
            "Source set (AutoTrack + UserTrack)",
            self,
        )
        self.single_file_mode.setChecked(True)
        self._mode_group = QButtonGroup(self)
        self._mode_group.addButton(self.single_file_mode)
        self._mode_group.addButton(self.source_set_mode)

        self.mode_row = QWidget(self)
        mode_layout = QHBoxLayout(self.mode_row)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.addWidget(self.single_file_mode)
        mode_layout.addWidget(self.source_set_mode)

        self.role = ChoiceBox(PFTRACK_SOURCE_ROLES, ROLE_LABELS, self)

        self.input_path = PathField(
            "Choose source file",
            start_directory=start_directory,
            parent=self,
        )
        self.autotrack_path = PathField(
            "Choose PFTrack AutoTrack file",
            start_directory=start_directory,
            parent=self,
        )
        self.usertrack_path = PathField(
            "Choose PFTrack UserTrack file",
            start_directory=start_directory,
            parent=self,
        )

        layout.addRow("Software", self.software)
        layout.addRow("PFTrack mode", self.mode_row)
        layout.addRow("Role", self.role)
        layout.addRow("Input", self.input_path)
        layout.addRow("AutoTrack input", self.autotrack_path)
        layout.addRow("UserTrack input", self.usertrack_path)
        self._layout = layout

        self.software.currentIndexChanged.connect(self._refresh)
        self.single_file_mode.toggled.connect(self._refresh)
        self.role.currentIndexChanged.connect(self.changed)

        for field in (self.input_path, self.autotrack_path, self.usertrack_path):
            field.changed.connect(self.changed)
            field.chosen.connect(self.input_chosen)

        self._refresh()

    def software_id(self) -> str | None:
        return self.software.value()

    def is_pftrack(self) -> bool:
        return self.software_id() == SOFTWARE_PFTRACK_2017

    def is_source_set(self) -> bool:
        return self.is_pftrack() and self.source_set_mode.isChecked()

    def role_id(self) -> str | None:
        if not self.is_pftrack() or self.is_source_set():
            return None

        return self.role.value()

    def _set_row_visible(self, field, visible) -> None:
        # show() / hide() instead of QFormLayout.setRowVisible(field, bool);
        # see ChoiceBox for the PySide6 Linux refcount issue.
        for widget in (self._layout.labelForField(field), field):
            if visible:
                widget.show()
            else:
                widget.hide()

    def _refresh(self) -> None:
        pftrack = self.is_pftrack()
        source_set = self.is_source_set()

        self._set_row_visible(self.mode_row, pftrack)
        self._set_row_visible(self.role, pftrack and not source_set)
        self._set_row_visible(self.input_path, not source_set)
        self._set_row_visible(self.autotrack_path, source_set)
        self._set_row_visible(self.usertrack_path, source_set)

        self.changed.emit()

    def is_complete(self) -> bool:
        if self.software_id() is None:
            return False

        if self.is_source_set():
            return bool(self.autotrack_path.path() and self.usertrack_path.path())

        if self.is_pftrack() and self.role_id() is None:
            return False

        return bool(self.input_path.path())


class TargetSection(QWidget):
    """Target software. The entry equal to the source is disabled.

    Disabling is presentation only; Core still rejects same-source
    conversion (SAME_SOURCE_CONVERSION_NOT_ALLOWED).
    """

    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QFormLayout(self)
        self.software = ChoiceBox(SUPPORTED_SOFTWARE, SOFTWARE_LABELS, self)
        layout.addRow("Software", self.software)

        self.software.currentIndexChanged.connect(self.changed)

    def software_id(self) -> str | None:
        return self.software.value()

    def item_enabled(self, software_id) -> bool:
        index = self.software.index_of(software_id)
        return self.software.model().item(index).isEnabled()

    def set_source(self, source_id) -> None:
        model = self.software.model()

        for index, software_id in enumerate(self.software.values()):
            if software_id is None:
                continue

            same_as_source = software_id == source_id
            model.item(index).setEnabled(not same_as_source)
            self.software.setItemData(
                index,
                SAME_AS_SOURCE_TOOLTIP if same_as_source else "",
                Qt.ItemDataRole.ToolTipRole,
            )

        if source_id is not None and self.software_id() == source_id:
            # Never pick another target on the user's behalf.
            self.software.setCurrentIndex(0)

    def is_complete(self) -> bool:
        target = self.software_id()
        return target is not None and self.item_enabled(target)
