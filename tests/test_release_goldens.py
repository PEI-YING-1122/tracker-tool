import os
from pathlib import Path

import pytest

from tracker_tool import main
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import (
    convert_pftrack_source_set,
    convert_tracks,
)


VALIDATION_DIR = Path(__file__).resolve().parents[1] / "validation"
INPUTS_DIR = VALIDATION_DIR / "inputs"
OUTPUTS_DIR = VALIDATION_DIR / "outputs"

WIDTH = 1920
HEIGHT = 1080
START_FRAME = 1001

# Released v1.0.0 golden outputs. Every output listed in
# validation/README.md is included, plus the two PFTrack UserTrack
# outputs that are present in validation/outputs without a README entry.
SINGLE_SOURCE_GOLDENS = [
    ("3de_golden_01.txt", "3DE_R5", None, "PFTRACK_2017", "3de_to_pftrack_golden_01.txt"),
    ("3de_golden_01.txt", "3DE_R5", None, "SYNTHEYES_2304", "3de_to_syntheyes_golden_01.txt"),
    ("pftrack_golden_01.txt", "PFTRACK_2017", "AUTOTRACK", "3DE_R5", "pftrack_to_3de_golden_01.txt"),
    ("pftrack_golden_01.txt", "PFTRACK_2017", "AUTOTRACK", "SYNTHEYES_2304", "pftrack_to_syntheyes_golden_01.txt"),
    ("pftrack_usertrack_golden_01.txt", "PFTRACK_2017", "USERTRACK", "3DE_R5", "pftrack_usertrack_to_3de_golden_01.txt"),
    ("pftrack_usertrack_golden_01.txt", "PFTRACK_2017", "USERTRACK", "SYNTHEYES_2304", "pftrack_usertrack_to_syntheyes_golden_01.txt"),
    ("syntheyes_golden_01.txt", "SYNTHEYES_2304", None, "3DE_R5", "syntheyes_to_3de_golden_01.txt"),
    ("syntheyes_golden_01.txt", "SYNTHEYES_2304", None, "PFTRACK_2017", "syntheyes_to_pftrack_golden_01.txt"),
]

SOURCE_SET_GOLDENS = [
    ("3DE_R5", "pftrack_source_set_to_3de_golden_01.txt"),
    ("SYNTHEYES_2304", "pftrack_source_set_to_syntheyes_golden_01.txt"),
]

SOURCE_SET_AUTOTRACK = "pftrack_source_set_autotrack_golden_01.txt"
SOURCE_SET_USERTRACK = "pftrack_source_set_usertrack_golden_01.txt"


def _shot_config(source, target):
    return ShotConfig(
        image_width=WIDTH,
        image_height=HEIGHT,
        production_start_frame=START_FRAME,
        production_end_frame=None,
        source_software=source,
        target_software=target,
    )


def _read_text(path):
    return path.read_text(encoding="utf-8")


def _expected_cli_bytes(golden_path):
    # Goldens are stored with LF in Git and checked out as LF or CRLF
    # depending on core.autocrlf. The CLI writes in text mode, so the
    # expected bytes are the golden content with the platform newline.
    # On Windows these are the bytes that passed Artist Import.
    golden_bytes = golden_path.read_bytes().replace(b"\r\n", b"\n")

    assert b"\r" not in golden_bytes

    return golden_bytes.replace(b"\n", os.linesep.encode("ascii"))


def _common_cli_args(output_path):
    return [
        "--output",
        str(output_path),
        "--width",
        str(WIDTH),
        "--height",
        str(HEIGHT),
        "--start-frame",
        str(START_FRAME),
    ]


@pytest.mark.parametrize(
    ("input_name", "source", "role", "target", "golden_name"),
    SINGLE_SOURCE_GOLDENS,
)
def test_conversion_reproduces_released_golden_text(
    input_name,
    source,
    role,
    target,
    golden_name,
):
    output_text = convert_tracks(
        _read_text(INPUTS_DIR / input_name),
        _shot_config(source, target),
        pftrack_source_role=role,
    )

    assert output_text == _read_text(OUTPUTS_DIR / golden_name)


@pytest.mark.parametrize(
    ("target", "golden_name"),
    SOURCE_SET_GOLDENS,
)
def test_source_set_conversion_reproduces_released_golden_text(
    target,
    golden_name,
):
    output_text = convert_pftrack_source_set(
        _read_text(INPUTS_DIR / SOURCE_SET_AUTOTRACK),
        _read_text(INPUTS_DIR / SOURCE_SET_USERTRACK),
        _shot_config("PFTRACK_2017", target),
    )

    assert output_text == _read_text(OUTPUTS_DIR / golden_name)


@pytest.mark.parametrize(
    ("input_name", "source", "role", "target", "golden_name"),
    SINGLE_SOURCE_GOLDENS,
)
def test_cli_output_matches_released_golden_bytes(
    tmp_path,
    input_name,
    source,
    role,
    target,
    golden_name,
):
    output_path = tmp_path / golden_name

    argv = [
        "convert",
        "--source",
        source,
        "--target",
        target,
        "--input",
        str(INPUTS_DIR / input_name),
        *_common_cli_args(output_path),
    ]

    if role is not None:
        argv += [
            "--pftrack-source-role",
            role,
        ]

    assert main(argv) == 0

    assert output_path.read_bytes() == _expected_cli_bytes(
        OUTPUTS_DIR / golden_name
    )


@pytest.mark.parametrize(
    ("target", "golden_name"),
    SOURCE_SET_GOLDENS,
)
def test_cli_source_set_output_matches_released_golden_bytes(
    tmp_path,
    target,
    golden_name,
):
    output_path = tmp_path / golden_name

    assert main(
        [
            "convert-pftrack-source-set",
            "--autotrack-input",
            str(INPUTS_DIR / SOURCE_SET_AUTOTRACK),
            "--usertrack-input",
            str(INPUTS_DIR / SOURCE_SET_USERTRACK),
            "--target",
            target,
            *_common_cli_args(output_path),
        ]
    ) == 0

    assert output_path.read_bytes() == _expected_cli_bytes(
        OUTPUTS_DIR / golden_name
    )
