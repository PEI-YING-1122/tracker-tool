"""PyInstaller entry script for the Tracker Tool GUI.

When TRACKER_TOOL_GUI_SMOKE_TEST is set, the application exits by itself
shortly after start-up: code 0 if the main window is visible, 3 if not.
packaging/smoke_test_frozen.py uses this to check a frozen bundle.
"""

import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from tracker_tool_gui.__main__ import main
from tracker_tool_gui.main_window import WINDOW_TITLE


SMOKE_TEST_ENV = "TRACKER_TOOL_GUI_SMOKE_TEST"
SMOKE_TEST_DELAY_MS = 2000
SMOKE_TEST_WINDOW_MISSING = 3


def _exit_after_checking_main_window(app) -> None:
    def check():
        visible = any(
            widget.windowTitle() == WINDOW_TITLE and widget.isVisible()
            for widget in app.topLevelWidgets()
        )
        app.exit(0 if visible else SMOKE_TEST_WINDOW_MISSING)

    QTimer.singleShot(SMOKE_TEST_DELAY_MS, check)


if __name__ == "__main__":
    application = QApplication(sys.argv)

    if os.environ.get(SMOKE_TEST_ENV):
        _exit_after_checking_main_window(application)

    raise SystemExit(main())
