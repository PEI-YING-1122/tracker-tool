import pytest

pytest.importorskip("PySide6")

from tracker_tool_gui.widgets import (  # noqa: E402
    ARTIST_IMPORT_NOTE,
    PathField,
    ResultPanel,
    ShotFields,
    ShotFieldValues,
)


@pytest.fixture
def shot_fields(qtbot):
    widget = ShotFields()
    qtbot.addWidget(widget)
    return widget


def _fill(shot_fields, width="", height="", start="", end=""):
    shot_fields.width_field.setText(width)
    shot_fields.height_field.setText(height)
    shot_fields.start_frame_field.setText(start)
    shot_fields.end_frame_field.setText(end)


def test_shot_fields_map_integers(shot_fields):
    _fill(shot_fields, "1920", "1080", "1001", "1100")

    assert shot_fields.values() == ShotFieldValues(1920, 1080, 1001, 1100)


def test_empty_shot_fields_map_to_none(shot_fields):
    assert shot_fields.values() == ShotFieldValues(None, None, None, None)


@pytest.mark.parametrize(
    ("width", "height", "start", "end"),
    [
        ("0", "1080", "1001", ""),
        ("-1920", "1080", "1001", ""),
        ("1920", "1080", "1001", "1000"),
        ("1920", "1080", "-10", "-1"),
    ],
)
def test_shot_fields_do_not_enforce_core_value_rules(
    shot_fields,
    width,
    height,
    start,
    end,
):
    # Range rules belong to Core (INVALID_SHOT_METADATA). The GUI passes
    # every integer through unchanged.
    _fill(shot_fields, width, height, start, end)

    assert shot_fields.values() == ShotFieldValues(
        int(width),
        int(height),
        int(start),
        int(end) if end else None,
    )


@pytest.mark.parametrize(
    "typed",
    [
        "1920.5",
        "abc",
        "1e3",
        " 1920",
        "+1920",
    ],
)
def test_shot_fields_reject_non_integer_typing(qtbot, shot_fields, typed):
    shot_fields.width_field.clear()
    qtbot.keyClicks(shot_fields.width_field, typed)

    text = shot_fields.width_field.text()

    assert text == "" or text.lstrip("-").isdigit()


def test_lone_minus_sign_is_incomplete_input(shot_fields):
    _fill(shot_fields, "1920", "1080", "-", "")

    assert shot_fields.has_incomplete_input()

    with pytest.raises(ValueError):
        shot_fields.values()


def test_unknown_end_frame_clears_and_disables_field(shot_fields):
    _fill(shot_fields, "1920", "1080", "1001", "1100")

    shot_fields.end_frame_unknown.setChecked(True)

    assert not shot_fields.end_frame_field.isEnabled()
    assert shot_fields.values().production_end_frame is None

    shot_fields.end_frame_unknown.setChecked(False)

    assert shot_fields.end_frame_field.isEnabled()
    assert shot_fields.values().production_end_frame is None


def test_shot_fields_emit_changed(qtbot, shot_fields):
    with qtbot.waitSignal(shot_fields.changed, timeout=1000):
        shot_fields.width_field.setText("1920")

    with qtbot.waitSignal(shot_fields.changed, timeout=1000):
        shot_fields.end_frame_unknown.setChecked(True)


@pytest.mark.parametrize("mode", ["open", "save"])
def test_path_field_uses_dialog_result(qtbot, mode):
    calls = []

    def dialog(parent, caption, directory):
        calls.append(caption)
        return "C:/shots/native file.txt"

    field = PathField("Choose file", mode=mode, dialog=dialog)
    qtbot.addWidget(field)

    field.browse_button.click()

    assert calls == ["Choose file"]
    assert field.path() == "C:/shots/native file.txt"


def test_path_field_keeps_path_when_dialog_is_cancelled(qtbot):
    field = PathField("Choose file", dialog=lambda parent, caption, directory: "")
    qtbot.addWidget(field)
    field.path_edit.setText("existing.txt")

    field.browse_button.click()

    assert field.path() == "existing.txt"


def test_path_field_passes_typed_path_unchanged(qtbot):
    field = PathField("Choose file")
    qtbot.addWidget(field)

    field.path_edit.setText(" spaced name .txt")

    assert field.path() == " spaced name .txt"


def test_path_field_rejects_unknown_mode():
    with pytest.raises(ValueError):
        PathField("Choose file", mode="append")


@pytest.fixture
def result_panel(qtbot):
    panel = ResultPanel()
    qtbot.addWidget(panel)
    panel.show()
    return panel


def test_success_always_states_artist_import_is_not_verified(result_panel):
    result_panel.show_success("C:/out/output_3de.txt")

    assert result_panel.heading.text() == "PASS"
    assert "C:/out/output_3de.txt" in result_panel.message.text()
    assert result_panel.note.text() == ARTIST_IMPORT_NOTE
    assert result_panel.note.isVisible()


def test_failure_shows_heading_message_and_details(result_panel):
    result_panel.show_failure(
        "INVALID_SHOT_METADATA",
        "Shot metadata is invalid.",
        details="Traceback ...",
    )

    assert result_panel.heading.text() == "FAIL — INVALID_SHOT_METADATA"
    assert result_panel.message.text() == "Shot metadata is invalid."
    assert result_panel.details.toPlainText() == "Traceback ..."
    assert result_panel.details.isVisible()
    assert not result_panel.note.isVisible()


def test_busy_and_idle_clear_previous_outcome(result_panel):
    result_panel.show_failure("X", "y", details="z")

    result_panel.show_busy()

    assert result_panel.heading.text() == "Converting…"
    assert not result_panel.details.isVisible()

    result_panel.show_idle("Ready")

    assert result_panel.heading.text() == ""
    assert result_panel.message.text() == "Ready"
