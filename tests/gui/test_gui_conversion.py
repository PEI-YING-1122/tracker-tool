import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import Qt  # noqa: E402

import tracker_tool.app  # noqa: E402
from tracker_tool import main  # noqa: E402
from tracker_tool.config import ShotConfig  # noqa: E402
from tracker_tool.contract import (  # noqa: E402
    PFTRACK_SOURCE_ROLES,
    SUPPORTED_SOFTWARE,
)
from tracker_tool_gui.main_window import MainWindow  # noqa: E402
from tracker_tool_gui.results import NON_CONTRACT_NOTE  # noqa: E402
from tracker_tool_gui.selection import (  # noqa: E402
    PLACEHOLDER,
    SAME_AS_SOURCE_TOOLTIP,
)
from tracker_tool_gui.widgets import ARTIST_IMPORT_NOTE  # noqa: E402


def _load_release_goldens():
    path = Path(__file__).resolve().parents[1] / "test_release_goldens.py"
    spec = importlib.util.spec_from_file_location("release_goldens", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GOLDENS = _load_release_goldens()

THREE_DE_TEXT = "1\nPoint0001\n0\n2\n1 100.0 200.0\n3 102.0 202.0\n"


@pytest.fixture
def window(qtbot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    yield main_window
    qtbot.waitUntil(lambda: not main_window.runner.busy, timeout=5000)


def _select(combo, data):
    index = combo.findData(data)
    assert index >= 0, data
    combo.setCurrentIndex(index)


def _fill(
    window,
    *,
    source,
    target,
    output,
    input_path=None,
    autotrack=None,
    usertrack=None,
    role=None,
    width="1920",
    height="1080",
    start="1001",
    end="",
):
    _select(window.source.software, source)

    if autotrack is not None:
        window.source.source_set_mode.setChecked(True)
        window.source.autotrack_path.path_edit.setText(str(autotrack))
        window.source.usertrack_path.path_edit.setText(str(usertrack))
    else:
        window.source.single_file_mode.setChecked(True)
        window.source.input_path.path_edit.setText(str(input_path))

    if role is not None:
        _select(window.source.role, role)

    _select(window.target.software, target)
    window.shot_fields.width_field.setText(width)
    window.shot_fields.height_field.setText(height)
    window.shot_fields.start_frame_field.setText(start)
    window.shot_fields.end_frame_field.setText(end)
    window.output_path.path_edit.setText(str(output))


def _convert(qtbot, window):
    assert window.convert_button.isEnabled()
    window.convert_button.click()
    qtbot.waitUntil(
        lambda: window.result_panel.heading.text().startswith(("PASS", "FAIL")),
        timeout=10000,
    )
    return window.result_panel.heading.text()


# --- Source / Target presentation ------------------------------------------


def test_software_choices_come_from_contract(window):
    for combo in (window.source.software, window.target.software):
        assert [combo.itemData(i) for i in range(combo.count())] == [
            None,
            *SUPPORTED_SOFTWARE,
        ]
        assert combo.itemText(0) == PLACEHOLDER

        for index, software_id in enumerate(SUPPORTED_SOFTWARE, start=1):
            assert combo.itemText(index).endswith(f"({software_id})")

    role = window.source.role
    assert [role.itemData(i) for i in range(role.count())] == [
        None,
        *PFTRACK_SOURCE_ROLES,
    ]


@pytest.mark.parametrize("source", SUPPORTED_SOFTWARE)
def test_target_equal_to_source_is_disabled_with_tooltip(window, source):
    _select(window.source.software, source)

    for software_id in SUPPORTED_SOFTWARE:
        index = window.target.software.findData(software_id)
        enabled = window.target.item_enabled(software_id)
        tooltip = window.target.software.itemData(index, Qt.ItemDataRole.ToolTipRole)

        assert enabled == (software_id != source)
        assert tooltip == (SAME_AS_SOURCE_TOOLTIP if software_id == source else None)


def test_changing_source_to_current_target_resets_target(window):
    _select(window.source.software, "3DE_R5")
    _select(window.target.software, "PFTRACK_2017")

    _select(window.source.software, "PFTRACK_2017")

    assert window.target.software_id() is None
    assert window.target.software.currentText() == PLACEHOLDER


def test_changing_source_keeps_a_still_valid_target(window):
    _select(window.source.software, "3DE_R5")
    _select(window.target.software, "SYNTHEYES_2304")

    _select(window.source.software, "PFTRACK_2017")

    assert window.target.software_id() == "SYNTHEYES_2304"


def _visible(window, widget):
    return widget.isVisibleTo(window.source)


def test_pftrack_controls_appear_only_for_pftrack_source(window):
    _select(window.source.software, "3DE_R5")

    assert not _visible(window, window.source.mode_row)
    assert not _visible(window, window.source.role)
    assert _visible(window, window.source.input_path)

    _select(window.source.software, "PFTRACK_2017")

    assert _visible(window, window.source.mode_row)
    assert _visible(window, window.source.role)
    assert _visible(window, window.source.input_path)
    assert not _visible(window, window.source.autotrack_path)

    window.source.source_set_mode.setChecked(True)

    assert not _visible(window, window.source.role)
    assert not _visible(window, window.source.input_path)
    assert _visible(window, window.source.autotrack_path)
    assert _visible(window, window.source.usertrack_path)


def test_pftrack_role_has_no_default_and_is_required(window, tmp_path):
    _fill(
        window,
        source="PFTRACK_2017",
        target="3DE_R5",
        input_path=tmp_path / "in.txt",
        output=tmp_path / "out.txt",
    )

    assert window.source.role.currentData() is None
    assert not window.convert_button.isEnabled()

    _select(window.source.role, "USERTRACK")

    assert window.convert_button.isEnabled()


def test_convert_requires_complete_form(window, tmp_path):
    _fill(
        window,
        source="3DE_R5",
        target="PFTRACK_2017",
        input_path=tmp_path / "in.txt",
        output=tmp_path / "out.txt",
    )

    assert window.convert_button.isEnabled()

    window.output_path.path_edit.setText("")
    assert not window.convert_button.isEnabled()

    window.output_path.path_edit.setText(str(tmp_path / "out.txt"))
    window.shot_fields.start_frame_field.setText("-")
    assert not window.convert_button.isEnabled()

    window.shot_fields.start_frame_field.setText("1001")
    _select(window.target.software, "3DE_R5")
    assert not window.convert_button.isEnabled()


def test_empty_shot_fields_do_not_block_convert(window, tmp_path):
    # Missing metadata is reported by Core, not pre-checked by the GUI.
    _fill(
        window,
        source="3DE_R5",
        target="PFTRACK_2017",
        input_path=tmp_path / "in.txt",
        output=tmp_path / "out.txt",
        width="",
    )

    assert window.convert_button.isEnabled()


# --- GUI uses the same Core path as the CLI --------------------------------


def test_gui_single_file_conversion_calls_tracker_tool_app(
    qtbot,
    window,
    tmp_path,
    monkeypatch,
):
    calls = []
    monkeypatch.setattr(
        tracker_tool.app,
        "convert_file",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    _fill(
        window,
        source="PFTRACK_2017",
        target="SYNTHEYES_2304",
        input_path=tmp_path / "in.txt",
        output=tmp_path / "out.txt",
        role="AUTOTRACK",
        end="1100",
    )

    assert _convert(qtbot, window) == "PASS"
    assert calls == [
        (
            (
                str(tmp_path / "in.txt"),
                str(tmp_path / "out.txt"),
                ShotConfig(1920, 1080, 1001, 1100, "PFTRACK_2017", "SYNTHEYES_2304"),
            ),
            {"pftrack_source_role": "AUTOTRACK"},
        )
    ]


def test_gui_source_set_conversion_calls_tracker_tool_app(
    qtbot,
    window,
    tmp_path,
    monkeypatch,
):
    calls = []
    monkeypatch.setattr(
        tracker_tool.app,
        "convert_pftrack_source_set_files",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    _fill(
        window,
        source="PFTRACK_2017",
        target="3DE_R5",
        autotrack=tmp_path / "auto.txt",
        usertrack=tmp_path / "user.txt",
        output=tmp_path / "out.txt",
    )

    assert _convert(qtbot, window) == "PASS"
    assert calls == [
        (
            (
                str(tmp_path / "auto.txt"),
                str(tmp_path / "user.txt"),
                str(tmp_path / "out.txt"),
                ShotConfig(1920, 1080, 1001, None, "PFTRACK_2017", "3DE_R5"),
            ),
            {},
        )
    ]


def _cli_bytes(tmp_path, argv):
    output = tmp_path / "cli_output.txt"
    assert main(argv + ["--output", str(output), "--width", "1920", "--height", "1080", "--start-frame", "1001"]) == 0
    return output.read_bytes()


@pytest.mark.parametrize(
    ("input_name", "source", "role", "target", "golden_name"),
    GOLDENS.SINGLE_SOURCE_GOLDENS,
)
def test_gui_output_matches_cli_and_released_golden_bytes(
    qtbot,
    window,
    tmp_path,
    input_name,
    source,
    role,
    target,
    golden_name,
):
    gui_output = tmp_path / "gui_output.txt"
    _fill(
        window,
        source=source,
        target=target,
        input_path=GOLDENS.INPUTS_DIR / input_name,
        output=gui_output,
        role=role,
    )

    assert _convert(qtbot, window) == "PASS"

    argv = ["convert", "--source", source, "--target", target, "--input", str(GOLDENS.INPUTS_DIR / input_name)]
    if role is not None:
        argv += ["--pftrack-source-role", role]

    expected = GOLDENS._expected_cli_bytes(GOLDENS.OUTPUTS_DIR / golden_name)

    assert gui_output.read_bytes() == _cli_bytes(tmp_path, argv) == expected


@pytest.mark.parametrize(
    ("target", "golden_name"),
    GOLDENS.SOURCE_SET_GOLDENS,
)
def test_gui_source_set_output_matches_cli_and_released_golden_bytes(
    qtbot,
    window,
    tmp_path,
    target,
    golden_name,
):
    gui_output = tmp_path / "gui_output.txt"
    autotrack = GOLDENS.INPUTS_DIR / GOLDENS.SOURCE_SET_AUTOTRACK
    usertrack = GOLDENS.INPUTS_DIR / GOLDENS.SOURCE_SET_USERTRACK
    _fill(
        window,
        source="PFTRACK_2017",
        target=target,
        autotrack=autotrack,
        usertrack=usertrack,
        output=gui_output,
    )

    assert _convert(qtbot, window) == "PASS"

    argv = [
        "convert-pftrack-source-set",
        "--autotrack-input",
        str(autotrack),
        "--usertrack-input",
        str(usertrack),
        "--target",
        target,
    ]
    expected = GOLDENS._expected_cli_bytes(GOLDENS.OUTPUTS_DIR / golden_name)

    assert gui_output.read_bytes() == _cli_bytes(tmp_path, argv) == expected


# --- Result and error presentation -----------------------------------------


@pytest.fixture
def three_de_input(tmp_path):
    path = tmp_path / "input_3de.txt"
    path.write_text(THREE_DE_TEXT, encoding="utf-8")
    return path


def test_success_shows_output_artist_note_and_diagnostics(
    qtbot,
    window,
    tmp_path,
    three_de_input,
):
    output = tmp_path / "out.txt"
    _fill(window, source="3DE_R5", target="PFTRACK_2017", input_path=three_de_input, output=output)

    assert _convert(qtbot, window) == "PASS"
    assert str(output) in window.result_panel.message.text()
    assert window.result_panel.note.text() == ARTIST_IMPORT_NOTE
    assert "Source: 3DE_R5" in window.result_panel.diagnostics()
    assert window.convert_button.isEnabled()


@pytest.mark.parametrize(
    ("overrides", "code"),
    [
        ({"width": ""}, "MISSING_REQUIRED_SHOT_METADATA"),
        ({"width": "0"}, "INVALID_SHOT_METADATA"),
        ({"start": "1001", "end": "1000"}, "INVALID_SHOT_METADATA"),
        ({"end": "1001"}, "OBSERVATION_OUTSIDE_SHOT_RANGE"),
    ],
)
def test_formal_error_is_shown_by_code(
    qtbot,
    window,
    tmp_path,
    three_de_input,
    overrides,
    code,
):
    output = tmp_path / "out.txt"
    _fill(
        window,
        source="3DE_R5",
        target="PFTRACK_2017",
        input_path=three_de_input,
        output=output,
        **overrides,
    )

    assert _convert(qtbot, window) == f"FAIL — {code}"
    assert NON_CONTRACT_NOTE not in window.result_panel.message.text()
    assert f"Exception message: {code}" in window.result_panel.diagnostics()
    assert not output.exists()


def test_cross_source_collision_is_shown_by_code(qtbot, window, tmp_path):
    autotrack = tmp_path / "auto.txt"
    usertrack = tmp_path / "user.txt"
    autotrack.write_text('"A"\n1\n1\n1001 1 2 1.0\n', encoding="utf-8")
    usertrack.write_text('"A"\n1\n1\n1002 1 2 1.0\n', encoding="utf-8")
    _fill(
        window,
        source="PFTRACK_2017",
        target="3DE_R5",
        autotrack=autotrack,
        usertrack=usertrack,
        output=tmp_path / "out.txt",
    )

    assert _convert(qtbot, window) == "FAIL — CROSS_SOURCE_TRACK_NAME_COLLISION"


def test_non_contract_core_error_is_shown_verbatim(qtbot, window, tmp_path):
    input_path = tmp_path / "bad.txt"
    input_path.write_text("2\nPoint0001\n0\n1\n1 1 2\n", encoding="utf-8")
    _fill(window, source="3DE_R5", target="PFTRACK_2017", input_path=input_path, output=tmp_path / "out.txt")

    assert _convert(qtbot, window) == "FAIL — Core rejected the input"

    message = window.result_panel.message.text()
    assert "3DE native data ended before track name" in message
    assert NON_CONTRACT_NOTE in message


def test_file_error_is_shown_as_file_error(qtbot, window, tmp_path):
    _fill(
        window,
        source="3DE_R5",
        target="PFTRACK_2017",
        input_path=tmp_path / "missing.txt",
        output=tmp_path / "out.txt",
    )

    assert _convert(qtbot, window) == "FAIL — File error"


def test_unexpected_exception_is_shown_with_traceback(
    qtbot,
    window,
    tmp_path,
    monkeypatch,
):
    def broken(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(tracker_tool.app, "convert_file", broken)
    _fill(window, source="3DE_R5", target="PFTRACK_2017", input_path=tmp_path / "in.txt", output=tmp_path / "out.txt")

    assert _convert(qtbot, window) == "FAIL — Unexpected Core failure"
    assert "Traceback (most recent call last)" in window.result_panel.details.toPlainText()
    assert "RuntimeError: boom" in window.result_panel.details.toPlainText()


def test_failure_preserves_existing_output_file(qtbot, window, tmp_path, three_de_input):
    output = tmp_path / "out.txt"
    existing = b"existing output\r\n"
    output.write_bytes(existing)
    window._confirm_overwrite = lambda parent, path: True
    _fill(window, source="3DE_R5", target="PFTRACK_2017", input_path=three_de_input, output=output, width="0")

    assert _convert(qtbot, window) == "FAIL — INVALID_SHOT_METADATA"
    assert output.read_bytes() == existing


def test_form_is_usable_again_after_failure(qtbot, window, tmp_path, three_de_input):
    output = tmp_path / "out.txt"
    _fill(window, source="3DE_R5", target="PFTRACK_2017", input_path=three_de_input, output=output, width="0")

    assert _convert(qtbot, window).startswith("FAIL")

    for title in ("Source", "Target", "Shot", "Output"):
        assert window.sections[title].isEnabled()

    window.shot_fields.width_field.setText("1920")

    assert _convert(qtbot, window) == "PASS"
    assert output.exists()
