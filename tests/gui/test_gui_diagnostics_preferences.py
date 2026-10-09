import sys
from importlib import metadata

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QByteArray  # noqa: E402
from PySide6.QtGui import QGuiApplication  # noqa: E402

from tracker_tool_gui.diagnostics import format_diagnostics  # noqa: E402
from tracker_tool_gui.main_window import MainWindow  # noqa: E402
from tracker_tool_gui.preferences import (  # noqa: E402
    PERSISTED_KEYS,
    Preferences,
)
from tracker_tool_gui.widgets import PathField, ResultPanel  # noqa: E402


def _raise(exception):
    try:
        raise exception
    except type(exception) as raised:
        return raised


def test_diagnostics_report_environment():
    text = format_diagnostics()

    assert text.startswith("Tracker Tool diagnostics\n")
    assert f"tracker-tool: {metadata.version('tracker-tool')}" in text
    assert f"Python: {sys.version.split()[0]}" in text
    assert "PySide6: " in text
    assert "OS: " in text


def test_diagnostics_report_context_in_given_order():
    text = format_diagnostics(
        [
            ("Output", "C:/out/result.txt"),
            ("Width", 1920),
            ("End frame", None),
        ]
    )

    lines = text.splitlines()

    assert lines.index("Output: C:/out/result.txt") < lines.index(
        "Width: 1920"
    ) < lines.index("End frame: None")


@pytest.mark.parametrize(
    "exception",
    [
        ValueError("INVALID_SHOT_METADATA"),
        IndexError("list index out of range"),
    ],
)
def test_diagnostics_report_exception_as_raised(exception):
    text = format_diagnostics(exception=_raise(exception))

    assert f"Exception type: builtins.{type(exception).__name__}" in text
    assert f"Exception message: {exception}" in text
    assert "Traceback (most recent call last):" in text


def test_preferences_remember_directory_of_chosen_file(ini_settings):
    preferences = Preferences(ini_settings)

    assert preferences.directory("output") == ""

    preferences.remember_file("output", "C:/shots/sh010/out/result.txt")

    assert preferences.directory("output").replace("\\", "/") == (
        "C:/shots/sh010/out"
    )
    assert preferences.directory("input") == ""


def test_preferences_ignore_empty_path(ini_settings):
    preferences = Preferences(ini_settings)

    preferences.remember_file("input", "")

    assert ini_settings.allKeys() == []


def test_preferences_reject_unknown_directory_kind(ini_settings):
    with pytest.raises(ValueError):
        Preferences(ini_settings).directory("shot")


def test_preferences_round_trip_window_geometry(ini_settings):
    preferences = Preferences(ini_settings)

    assert preferences.window_geometry() is None

    preferences.save_window_geometry(QByteArray(b"geometry"))

    assert preferences.window_geometry() == QByteArray(b"geometry")


def test_path_field_starts_in_given_directory_and_reports_choice(qtbot):
    calls = []

    def dialog(parent, caption, directory):
        calls.append(directory)
        return "C:/shots/out.txt"

    field = PathField(
        "Choose file",
        dialog=dialog,
        start_directory=lambda: "C:/shots",
    )
    qtbot.addWidget(field)

    with qtbot.waitSignal(field.chosen, timeout=1000) as blocker:
        field.browse_button.click()

    assert calls == ["C:/shots"]
    assert blocker.args == ["C:/shots/out.txt"]


def test_result_panel_copies_diagnostics_to_clipboard(qtbot):
    panel = ResultPanel()
    qtbot.addWidget(panel)
    panel.show()

    panel.show_idle()
    assert not panel.copy_diagnostics_button.isVisible()

    panel.show_failure("X", "y", diagnostics="Tracker Tool diagnostics\n...")

    assert panel.copy_diagnostics_button.isVisible()

    panel.copy_diagnostics_button.click()

    assert QGuiApplication.clipboard().text() == (
        "Tracker Tool diagnostics\n..."
    )


def test_main_window_remembers_output_directory(qtbot, ini_settings):
    preferences = Preferences(ini_settings)
    window = MainWindow(preferences=preferences)
    qtbot.addWidget(window)

    window.output_path._dialog = (
        lambda parent, caption, directory: "C:/shots/out/result.txt"
    )
    window.output_path.browse_button.click()

    assert preferences.directory("output").replace("\\", "/") == (
        "C:/shots/out"
    )


def test_main_window_restores_geometry_and_never_persists_shot_values(
    qtbot,
    ini_settings,
):
    preferences = Preferences(ini_settings)

    first = MainWindow(preferences=preferences)
    qtbot.addWidget(first)
    # Stay inside the offscreen test screen; restoreGeometry clamps
    # windows to the available screen area.
    available = first.screen().availableGeometry()
    first.resize(
        min(first.minimumSizeHint().width() + 40, available.width() - 20),
        min(first.minimumSizeHint().height() + 30, available.height() - 60),
    )
    closed_size = first.size()
    first.shot_fields.width_field.setText("4608")
    first.shot_fields.start_frame_field.setText("1001")
    first.close()

    assert set(ini_settings.allKeys()) <= PERSISTED_KEYS

    second = MainWindow(preferences=preferences)
    qtbot.addWidget(second)

    assert second.size() == closed_size
    assert second.shot_fields.width_field.text() == ""
    assert second.shot_fields.start_frame_field.text() == ""
