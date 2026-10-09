import sys

from PySide6.QtWidgets import QApplication

from tracker_tool_gui.main_window import MainWindow


def main(argv=None) -> int:
    app = QApplication.instance() or QApplication(
        sys.argv if argv is None else argv
    )

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
