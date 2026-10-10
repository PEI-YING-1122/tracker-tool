import threading
from importlib import metadata

import pytest

pytest.importorskip("PySide6")

from tracker_tool_gui.main_window import (  # noqa: E402
    BUSY_STATUS,
    SECTION_TITLES,
    WINDOW_TITLE,
    MainWindow,
)
from tracker_tool_gui.widgets import PathField, ShotFields  # noqa: E402


@pytest.fixture
def window(qtbot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    yield main_window
    qtbot.waitUntil(lambda: not main_window.runner.busy, timeout=5000)


def test_main_window_shows_plan_sections_in_order(window):
    assert window.windowTitle() == WINDOW_TITLE

    assert list(window.sections) == list(SECTION_TITLES)

    assert [
        section.title()
        for section in window.sections.values()
    ] == list(SECTION_TITLES)


def test_shot_and_output_sections_hold_their_inputs(window):
    assert isinstance(window.shot_fields, ShotFields)
    assert window.shot_fields.parent() is window.sections["Shot"]

    assert isinstance(window.output_path, PathField)
    assert window.output_path.parent() is window.sections["Output"]


def test_convert_is_disabled_until_the_form_is_complete(window):
    window.shot_fields.width_field.setText("1920")
    window.output_path.path_edit.setText("out.txt")

    assert not window.convert_button.isEnabled()


def test_status_bar_shows_installed_core_version(window):
    assert metadata.version("tracker-tool") in (
        window.statusBar().currentMessage()
    )


def test_busy_state_locks_inputs_and_restores_them(qtbot, window):
    release = threading.Event()

    with qtbot.waitSignal(window.runner.busy_changed, timeout=5000):
        window.runner.start(lambda: release.wait(5))

    for title in ("Source", "Target", "Shot", "Output"):
        assert not window.sections[title].isEnabled()

    assert window.sections["Result"].isEnabled()
    assert not window.convert_button.isEnabled()
    assert window.result_panel.heading.text() == "Converting…"
    assert window.statusBar().currentMessage() == BUSY_STATUS

    with qtbot.waitSignal(window.runner.succeeded, timeout=5000):
        release.set()

    for title in SECTION_TITLES:
        assert window.sections[title].isEnabled()

    assert metadata.version("tracker-tool") in (
        window.statusBar().currentMessage()
    )
