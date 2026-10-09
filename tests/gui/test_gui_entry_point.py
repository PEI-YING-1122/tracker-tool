import importlib
import tomllib
from pathlib import Path

import pytest

pytest.importorskip("PySide6")

import tracker_tool_gui.__main__ as gui_main  # noqa: E402


PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def test_gui_entry_point_is_declared_as_gui_script():
    project = tomllib.loads(
        PYPROJECT.read_text(encoding="utf-8")
    )["project"]

    module_name, function_name = (
        project["gui-scripts"]["tracker-tool-gui"].split(":")
    )

    assert callable(
        getattr(importlib.import_module(module_name), function_name)
    )


def test_main_shows_window_and_returns_event_loop_exit_code(
    qtbot,
    monkeypatch,
):
    shown_windows = []

    class FakeApplication:
        @staticmethod
        def instance():
            return FakeApplication()

        def exec(self):
            return 7

    original_main_window = gui_main.MainWindow

    def main_window():
        window = original_main_window()
        qtbot.addWidget(window)
        shown_windows.append(window)
        return window

    monkeypatch.setattr(gui_main, "QApplication", FakeApplication)
    monkeypatch.setattr(gui_main, "MainWindow", main_window)

    assert gui_main.main([]) == 7

    assert len(shown_windows) == 1
    assert shown_windows[0].isVisible()
