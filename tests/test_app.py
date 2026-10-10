import os
from pathlib import Path

import pytest

from tracker_tool import main
from tracker_tool.app import (
    convert_file,
    convert_pftrack_source_set_files,
)
from tracker_tool.config import ShotConfig

from test_release_goldens import (
    INPUTS_DIR,
    OUTPUTS_DIR,
    SINGLE_SOURCE_GOLDENS,
    SOURCE_SET_AUTOTRACK,
    SOURCE_SET_GOLDENS,
    SOURCE_SET_USERTRACK,
    _expected_cli_bytes,
)


# File-level conversion contract (INTERCHANGE_MASTER.md "CLI Contract"):
# success-only write, existing output preserved on failure, input/output
# path collision rejected before anything is written, UTF-8 text, and the
# platform newline translation of text-mode writing.
#
# These tests first ran unchanged against cli.main (before tracker_tool.app
# existed) and now run against tracker_tool.app, so they pin the released
# v1.0.1 behaviour across the move.

THREE_DE_TEXT = (
    "1\n"
    "Point0001\n"
    "0\n"
    "2\n"
    "1 100.0 200.0\n"
    "3 102.0 202.0\n"
)

PFTRACK_EXPECTED = (
    '"Point0001"\n'
    "1\n"
    "2\n"
    "1001 100.0 200.0 1.000000\n"
    "1003 102.0 202.0 1.000000\n"
)

AUTOTRACK_TEXT = '"Auto0001"\n1\n1\n1001 10.0 20.0 1.000000\n'
USERTRACK_TEXT = '"User0001"\n1\n1\n1002 30.0 40.0 1.000000\n'


def _shot_config(source, target, width, height, start_frame, end_frame):
    return ShotConfig(
        image_width=width,
        image_height=height,
        production_start_frame=start_frame,
        production_end_frame=end_frame,
        source_software=source,
        target_software=target,
    )


def _run_single(
    input_path,
    output_path,
    *,
    source="3DE_R5",
    target="PFTRACK_2017",
    width=1920,
    height=1080,
    start_frame=1001,
    end_frame=None,
    pftrack_source_role=None,
):
    convert_file(
        input_path,
        output_path,
        _shot_config(source, target, width, height, start_frame, end_frame),
        pftrack_source_role=pftrack_source_role,
    )


def _run_source_set(
    autotrack_path,
    usertrack_path,
    output_path,
    *,
    target="3DE_R5",
    width=1920,
    height=1080,
    start_frame=1001,
    end_frame=None,
):
    convert_pftrack_source_set_files(
        autotrack_path,
        usertrack_path,
        output_path,
        _shot_config("PFTRACK_2017", target, width, height, start_frame, end_frame),
    )


def _platform_bytes(text):
    return text.replace("\n", os.linesep).encode("utf-8")


@pytest.fixture
def three_de_input(tmp_path):
    path = tmp_path / "input_3de.txt"
    path.write_text(THREE_DE_TEXT, encoding="utf-8")
    return path


@pytest.fixture
def source_set_inputs(tmp_path):
    autotrack = tmp_path / "autotrack.txt"
    usertrack = tmp_path / "usertrack.txt"
    autotrack.write_text(AUTOTRACK_TEXT, encoding="utf-8")
    usertrack.write_text(USERTRACK_TEXT, encoding="utf-8")
    return autotrack, usertrack


def test_success_writes_output_with_platform_newlines(tmp_path, three_de_input):
    output_path = tmp_path / "output.txt"

    _run_single(three_de_input, output_path)

    assert output_path.read_bytes() == _platform_bytes(PFTRACK_EXPECTED)


def test_source_set_success_writes_output(tmp_path, source_set_inputs):
    output_path = tmp_path / "output_3de.txt"

    _run_source_set(*source_set_inputs, output_path)

    assert output_path.read_text(encoding="utf-8") == (
        "2\nAuto0001\n0\n1\n1 10.0 20.0\nUser0001\n0\n1\n2 30.0 40.0\n"
    )


FAILURES = [
    pytest.param({"width": 0}, ValueError, "INVALID_SHOT_METADATA", id="formal-code"),
    pytest.param({"end_frame": 1001}, ValueError, "OBSERVATION_OUTSIDE_SHOT_RANGE", id="frame-range"),
    pytest.param({"target": "3DE_R5"}, ValueError, "SAME_SOURCE_CONVERSION_NOT_ALLOWED", id="same-source"),
]


@pytest.mark.parametrize(("overrides", "error", "message"), FAILURES)
def test_failure_creates_no_output(tmp_path, three_de_input, overrides, error, message):
    output_path = tmp_path / "output.txt"

    with pytest.raises(error, match=message):
        _run_single(three_de_input, output_path, **overrides)

    assert not output_path.exists()


@pytest.mark.parametrize(
    "native_text",
    [
        pytest.param("2\nPoint0001\n0\n1\n1 1 2\n", id="truncated"),
        pytest.param("1\nPoint0001\n7\n1\n1 1 2\n", id="unverified-static-field"),
    ],
)
def test_reader_failure_creates_no_output(tmp_path, native_text):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"
    input_path.write_text(native_text, encoding="utf-8")

    with pytest.raises(ValueError):
        _run_single(input_path, output_path)

    assert not output_path.exists()


@pytest.mark.parametrize(("overrides", "error", "message"), FAILURES)
def test_failure_preserves_existing_output_bytes(
    tmp_path,
    three_de_input,
    overrides,
    error,
    message,
):
    output_path = tmp_path / "output.txt"
    existing = b"existing output\r\nkeep me exactly\n"
    output_path.write_bytes(existing)

    with pytest.raises(error, match=message):
        _run_single(three_de_input, output_path, **overrides)

    assert output_path.read_bytes() == existing


def test_source_set_failure_preserves_existing_output(tmp_path):
    autotrack = tmp_path / "autotrack.txt"
    usertrack = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"
    autotrack.write_text(AUTOTRACK_TEXT, encoding="utf-8")
    usertrack.write_text(AUTOTRACK_TEXT, encoding="utf-8")
    existing = b"existing output\n"
    output_path.write_bytes(existing)

    with pytest.raises(ValueError, match="CROSS_SOURCE_TRACK_NAME_COLLISION"):
        _run_source_set(autotrack, usertrack, output_path)

    assert output_path.read_bytes() == existing


def test_missing_input_raises_file_error_and_creates_no_output(tmp_path):
    output_path = tmp_path / "output.txt"

    with pytest.raises(FileNotFoundError):
        _run_single(tmp_path / "missing.txt", output_path)

    assert not output_path.exists()


def test_output_equal_to_input_is_rejected_before_writing(three_de_input):
    original = three_de_input.read_bytes()

    with pytest.raises(ValueError, match="Input and output paths must be different"):
        _run_single(three_de_input, three_de_input)

    assert three_de_input.read_bytes() == original


def test_output_equal_to_input_by_different_spelling_is_rejected(
    tmp_path,
    three_de_input,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)
    original = three_de_input.read_bytes()

    for output_spelling in [
        Path(".") / three_de_input.name,
        three_de_input.name,
        Path("subdir") / ".." / three_de_input.name,
    ]:
        with pytest.raises(ValueError, match="Input and output paths must be different"):
            _run_single(three_de_input, output_spelling)

    assert three_de_input.read_bytes() == original


@pytest.mark.parametrize("collides_with", ["autotrack", "usertrack"])
def test_source_set_output_equal_to_an_input_is_rejected(
    source_set_inputs,
    collides_with,
):
    autotrack, usertrack = source_set_inputs
    output_path = autotrack if collides_with == "autotrack" else usertrack
    originals = (autotrack.read_bytes(), usertrack.read_bytes())

    with pytest.raises(ValueError, match="Input and output paths must be different"):
        _run_source_set(autotrack, usertrack, output_path)

    assert (autotrack.read_bytes(), usertrack.read_bytes()) == originals


def test_non_ascii_track_name_is_preserved_through_utf8(tmp_path):
    input_path = tmp_path / "input_3de.txt"
    output_path = tmp_path / "output.txt"
    input_path.write_text("1\n點位A\n0\n1\n1 1.5 2.5\n", encoding="utf-8")

    _run_single(input_path, output_path)

    assert output_path.read_text(encoding="utf-8").splitlines()[0] == '"點位A"'


def test_non_ascii_paths_are_supported(tmp_path):
    directory = tmp_path / "副檔 測試"
    directory.mkdir()
    input_path = directory / "輸入.txt"
    output_path = directory / "輸出.txt"
    input_path.write_text(THREE_DE_TEXT, encoding="utf-8")

    _run_single(input_path, output_path)

    assert output_path.read_bytes() == _platform_bytes(PFTRACK_EXPECTED)


def test_missing_shot_metadata_is_a_formal_error_and_writes_nothing(
    tmp_path,
    three_de_input,
):
    # The CLI parser rejects a missing --width before Core runs; the app
    # interface (used by the GUI) passes None and Core reports the code.
    output_path = tmp_path / "output.txt"

    with pytest.raises(ValueError, match="MISSING_REQUIRED_SHOT_METADATA"):
        _run_single(three_de_input, output_path, width=None)

    assert not output_path.exists()


def _cli_single(input_path, output_path, source, target, role):
    argv = [
        "convert",
        "--source",
        source,
        "--target",
        target,
        "--input",
        str(input_path),
        "--output",
        str(output_path),
        "--width",
        "1920",
        "--height",
        "1080",
        "--start-frame",
        "1001",
    ]

    if role is not None:
        argv += ["--pftrack-source-role", role]

    assert main(argv) == 0


@pytest.mark.parametrize(
    ("input_name", "source", "role", "target", "golden_name"),
    SINGLE_SOURCE_GOLDENS,
)
def test_cli_and_app_produce_identical_golden_bytes(
    tmp_path,
    input_name,
    source,
    role,
    target,
    golden_name,
):
    cli_output = tmp_path / "cli.txt"
    app_output = tmp_path / "app.txt"

    _cli_single(INPUTS_DIR / input_name, cli_output, source, target, role)
    _run_single(
        INPUTS_DIR / input_name,
        app_output,
        source=source,
        target=target,
        pftrack_source_role=role,
    )

    expected = _expected_cli_bytes(OUTPUTS_DIR / golden_name)

    assert cli_output.read_bytes() == app_output.read_bytes() == expected


@pytest.mark.parametrize(
    ("target", "golden_name"),
    SOURCE_SET_GOLDENS,
)
def test_cli_and_app_produce_identical_source_set_golden_bytes(
    tmp_path,
    target,
    golden_name,
):
    cli_output = tmp_path / "cli.txt"
    app_output = tmp_path / "app.txt"

    assert main(
        [
            "convert-pftrack-source-set",
            "--autotrack-input",
            str(INPUTS_DIR / SOURCE_SET_AUTOTRACK),
            "--usertrack-input",
            str(INPUTS_DIR / SOURCE_SET_USERTRACK),
            "--target",
            target,
            "--output",
            str(cli_output),
            "--width",
            "1920",
            "--height",
            "1080",
            "--start-frame",
            "1001",
        ]
    ) == 0

    _run_source_set(
        INPUTS_DIR / SOURCE_SET_AUTOTRACK,
        INPUTS_DIR / SOURCE_SET_USERTRACK,
        app_output,
        target=target,
    )

    expected = _expected_cli_bytes(OUTPUTS_DIR / golden_name)

    assert cli_output.read_bytes() == app_output.read_bytes() == expected
