from pathlib import Path

import pytest

from tracker_tool import main
from tracker_tool.adapters.pftrack import read_pftrack_tracks
from tracker_tool.adapters.syntheyes import read_syntheyes_tracks
from tracker_tool.adapters.threed import read_3de_tracks
from tracker_tool.config import ShotConfig


INPUTS_DIR = Path(__file__).resolve().parents[1] / "validation" / "inputs"


def _shot_config(source, target):
    return ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software=source,
        target_software=target,
    )


def _read_3de(native_text):
    return read_3de_tracks(
        native_text,
        _shot_config("3DE_R5", "PFTRACK_2017"),
    )


def _read_pftrack(native_text):
    return read_pftrack_tracks(
        native_text,
        source_role="AUTOTRACK",
    )


def _read_syntheyes(native_text):
    return read_syntheyes_tracks(
        native_text,
        _shot_config("SYNTHEYES_2304", "3DE_R5"),
    )


GOLDEN_READERS = [
    ("3de_golden_01.txt", _read_3de),
    ("pftrack_golden_01.txt", _read_pftrack),
    ("pftrack_usertrack_golden_01.txt", _read_pftrack),
    ("pftrack_source_set_autotrack_golden_01.txt", _read_pftrack),
    ("pftrack_source_set_usertrack_golden_01.txt", _read_pftrack),
    ("syntheyes_golden_01.txt", _read_syntheyes),
]


def _assert_parses_or_raises_value_error(reader, native_text):
    # Malformed native input must be reported as ValueError, as defined by
    # the v1 Error Contract. Any other exception type fails the test.
    try:
        reader(native_text)
    except ValueError:
        pass


@pytest.mark.parametrize(
    ("input_name", "reader"),
    GOLDEN_READERS,
)
def test_reader_truncated_at_every_line_raises_only_value_error(
    input_name,
    reader,
):
    lines = (INPUTS_DIR / input_name).read_text(
        encoding="utf-8",
    ).splitlines()

    for line_count in range(len(lines)):
        native_text = "".join(
            line + "\n"
            for line in lines[:line_count]
        )

        _assert_parses_or_raises_value_error(
            reader,
            native_text,
        )


@pytest.mark.parametrize(
    ("input_name", "reader"),
    GOLDEN_READERS,
)
def test_reader_truncated_at_every_character_raises_only_value_error(
    input_name,
    reader,
):
    native_text = (INPUTS_DIR / input_name).read_text(
        encoding="utf-8",
    )

    for character_count in range(len(native_text)):
        _assert_parses_or_raises_value_error(
            reader,
            native_text[:character_count],
        )


@pytest.mark.parametrize(
    "native_text",
    [
        "",
        "1\n",
        "1\nPoint0001\n",
        "1\nPoint0001\n0\n",
        "2\nPoint0001\n0\n1\n1 100.0 200.0\n",
    ],
)
def test_3de_reader_rejects_truncated_structure_with_value_error(
    native_text,
):
    with pytest.raises(ValueError):
        _read_3de(native_text)


@pytest.mark.parametrize(
    "native_text",
    [
        '"Auto000084"\n',
        '"Auto000084"\n1\n',
        '"Auto000084"\n1\n1\n1001 100.0 200.0 1.000000\n"Auto000094"\n',
    ],
)
def test_pftrack_reader_rejects_truncated_structure_with_value_error(
    native_text,
):
    with pytest.raises(ValueError):
        _read_pftrack(native_text)


def test_cli_truncated_3de_input_fails_without_writing_output(tmp_path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "2\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "PFTRACK_2017",
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
        )

    assert not output_path.exists()
