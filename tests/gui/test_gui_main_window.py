from importlib import metadata

import pytest

pytest.importorskip("PySide6")

from tracker_tool_gui.main_window import (  # noqa: E402
    SECTION_TITLES,
    WINDOW_TITLE,
    MainWindow,
)


@pytest.fixture
def window(qtbot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)

    return main_window


def test_main_window_shows_plan_sections_in_order(window):
    assert window.windowTitle() == WINDOW_TITLE

    assert list(window.sections) == list(SECTION_TITLES)

    assert [
        section.title()
        for section in window.sections.values()
    ] == list(SECTION_TITLES)


def test_convert_is_disabled_until_core_integration(window):
    assert not window.convert_button.isEnabled()
    assert window.convert_button.toolTip()


def test_status_bar_shows_installed_core_version(window):
    assert metadata.version("tracker-tool") in (
        window.statusBar().currentMessage()
    )
