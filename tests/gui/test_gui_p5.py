import pytest

pytest.importorskip("PySide6")

from tracker_tool.contract import FORMAL_ERROR_CODES  # noqa: E402
from tracker_tool_gui.main_window import (  # noqa: E402
    CANCELLED_MESSAGE,
    MainWindow,
)
from tracker_tool_gui.results import (  # noqa: E402
    FORMAL_ERROR_EXPLANATIONS,
    FORMAL_ERROR_SECTIONS,
)

THREE_DE_TEXT = "1\nPoint0001\n0\n2\n1 100.0 200.0\n3 102.0 202.0\n"


class Recorder:
    def __init__(self, answer=True):
        self.answer = answer
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args[-1])
        return self.answer


@pytest.fixture
def confirm():
    return Recorder()


@pytest.fixture
def opened():
    return Recorder()


@pytest.fixture
def window(qtbot, confirm, opened):
    main_window = MainWindow(confirm_overwrite=confirm, open_folder=opened)
    qtbot.addWidget(main_window)
    yield main_window
    qtbot.waitUntil(lambda: not main_window.runner.busy, timeout=5000)


@pytest.fixture
def three_de_input(tmp_path):
    path = tmp_path / "input_3de.txt"
    path.write_text(THREE_DE_TEXT, encoding="utf-8")
    return path


def _fill(window, input_path, output, width="1920"):
    window.source.software.setCurrentIndex(window.source.software.findData("3DE_R5"))
    window.source.input_path.path_edit.setText(str(input_path))
    window.target.software.setCurrentIndex(window.target.software.findData("PFTRACK_2017"))
    window.shot_fields.width_field.setText(width)
    window.shot_fields.height_field.setText("1080")
    window.shot_fields.start_frame_field.setText("1001")
    window.output_path.path_edit.setText(str(output))


def _convert(qtbot, window):
    window.convert_button.click()
    qtbot.waitUntil(
        lambda: window.result_panel.heading.text().startswith(("PASS", "FAIL")),
        timeout=10000,
    )
    return window.result_panel.heading.text()


def test_every_formal_code_has_explanation_and_sections():
    assert set(FORMAL_ERROR_EXPLANATIONS) == FORMAL_ERROR_CODES
    assert set(FORMAL_ERROR_SECTIONS) == FORMAL_ERROR_CODES


def test_formal_shot_error_highlights_shot_section(qtbot, window, tmp_path, three_de_input):
    _fill(window, three_de_input, tmp_path / "out.txt", width="0")

    assert _convert(qtbot, window) == "FAIL — INVALID_SHOT_METADATA"
    assert window.attention_sections() == ["Shot"]


def test_cross_source_collision_highlights_source_section(qtbot, window, tmp_path):
    autotrack = tmp_path / "auto.txt"
    usertrack = tmp_path / "user.txt"
    autotrack.write_text('"A"\n1\n1\n1001 1 2 1.0\n', encoding="utf-8")
    usertrack.write_text('"A"\n1\n1\n1002 1 2 1.0\n', encoding="utf-8")
    window.source.software.setCurrentIndex(window.source.software.findData("PFTRACK_2017"))
    window.source.source_set_mode.setChecked(True)
    window.source.autotrack_path.path_edit.setText(str(autotrack))
    window.source.usertrack_path.path_edit.setText(str(usertrack))
    window.target.software.setCurrentIndex(window.target.software.findData("3DE_R5"))
    window.shot_fields.width_field.setText("1920")
    window.shot_fields.height_field.setText("1080")
    window.shot_fields.start_frame_field.setText("1001")
    window.output_path.path_edit.setText(str(tmp_path / "out.txt"))

    assert _convert(qtbot, window) == "FAIL — CROSS_SOURCE_TRACK_NAME_COLLISION"
    assert window.attention_sections() == ["Source"]


def test_non_contract_error_highlights_nothing(qtbot, window, tmp_path):
    bad = tmp_path / "bad.txt"
    bad.write_text("2\nPoint0001\n0\n1\n1 1 2\n", encoding="utf-8")
    _fill(window, bad, tmp_path / "out.txt")

    assert _convert(qtbot, window) == "FAIL — Core rejected the input"
    assert window.attention_sections() == []


def test_highlight_clears_when_input_changes(qtbot, window, tmp_path, three_de_input):
    _fill(window, three_de_input, tmp_path / "out.txt", width="0")
    _convert(qtbot, window)

    window.shot_fields.width_field.setText("1920")

    assert window.attention_sections() == []


def test_new_output_is_written_without_asking(qtbot, window, confirm, tmp_path, three_de_input):
    _fill(window, three_de_input, tmp_path / "out.txt")

    assert _convert(qtbot, window) == "PASS"
    assert confirm.calls == []


def test_existing_typed_output_asks_and_cancel_keeps_file(
    qtbot,
    window,
    confirm,
    tmp_path,
    three_de_input,
):
    confirm.answer = False
    output = tmp_path / "out.txt"
    output.write_bytes(b"keep me\n")
    _fill(window, three_de_input, output)

    window.convert_button.click()

    assert confirm.calls == [str(output)]
    assert not window.runner.busy
    assert window.result_panel.message.text() == CANCELLED_MESSAGE
    assert output.read_bytes() == b"keep me\n"


def test_existing_typed_output_asks_and_confirm_overwrites(
    qtbot,
    window,
    confirm,
    tmp_path,
    three_de_input,
):
    output = tmp_path / "out.txt"
    output.write_bytes(b"old\n")
    _fill(window, three_de_input, output)

    assert _convert(qtbot, window) == "PASS"
    assert confirm.calls == [str(output)]
    assert output.read_bytes() != b"old\n"


def test_output_chosen_in_save_dialog_is_not_asked_again(
    qtbot,
    window,
    confirm,
    tmp_path,
    three_de_input,
):
    output = tmp_path / "out.txt"
    output.write_bytes(b"old\n")
    _fill(window, three_de_input, tmp_path / "placeholder.txt")
    window.output_path._dialog = lambda parent, caption, directory: str(output)

    window.output_path.browse_button.click()

    assert _convert(qtbot, window) == "PASS"
    assert confirm.calls == []


def test_open_output_folder_after_success(qtbot, window, opened, tmp_path, three_de_input):
    output = tmp_path / "out.txt"
    _fill(window, three_de_input, output)

    assert _convert(qtbot, window) == "PASS"
    assert window.result_panel.open_folder_button.isVisibleTo(window.result_panel)

    window.result_panel.open_folder_button.click()

    assert opened.calls == [str(tmp_path)]


def test_no_open_folder_after_failure(qtbot, window, tmp_path, three_de_input):
    _fill(window, three_de_input, tmp_path / "out.txt", width="0")

    _convert(qtbot, window)

    assert not window.result_panel.open_folder_button.isVisibleTo(window.result_panel)
