from importlib import metadata

from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


WINDOW_TITLE = "Tracker Tool"

# Section order follows docs/gui/GUI_DEVELOPMENT_PLAN.md §6. The controls
# inside each section are added when the GUI is wired to the Core
# integration boundary (tracker_tool.app / tracker_tool.contract, phase P1).
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


def installed_core_version() -> str:
    try:
        return metadata.version("tracker-tool")
    except metadata.PackageNotFoundError:
        return "unknown"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)

        central = QWidget(self)
        layout = QVBoxLayout(central)

        self.sections: dict[str, QGroupBox] = {}

        for title in SECTION_TITLES:
            section = QGroupBox(title, central)
            QVBoxLayout(section)
            layout.addWidget(section)
            self.sections[title] = section

        self.convert_button = QPushButton("Convert", central)
        self.convert_button.setEnabled(False)
        self.convert_button.setToolTip(CORE_INTEGRATION_PENDING)
        layout.addWidget(self.convert_button)

        self.sections["Result"].layout().addWidget(
            QLabel(CORE_INTEGRATION_PENDING, self.sections["Result"])
        )

        self.setCentralWidget(central)

        self.statusBar().showMessage(
            f"tracker-tool {installed_core_version()}"
        )
