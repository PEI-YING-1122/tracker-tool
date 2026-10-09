import os
from pathlib import Path

import pytest

from tracker_tool.adapters.threed import read_3de_tracks
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import convert_tracks


# Real 3DEqualizer R5 exports write either "0" or "3" on the line after the
# point name. Evidence (v1.0.1 CI-12): importing a file with "0" into 3DE
# and exporting it again produced "3" for every point, with identical track
# names, frame sets and coordinates (max difference 4.5e-13 px). The field
# is not Canonical data, so both verified values must give the same result.

def _native_text(static_fields):
    blocks = [
        (
            "Point0001",
            ["1 100.25 200.5", "2 101.5 201.75", "4 103.125 203.875"],
        ),
        (
            "Point0002",
            ["3 -12.5 2210.25"],
        ),
    ]

    lines = [str(len(blocks))]

    for (name, rows), static_field in zip(blocks, static_fields):
        lines += [name, static_field, str(len(rows))] + rows

    return "\n".join(lines) + "\n"


def _shot_config(target="PFTRACK_2017"):
    return ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="3DE_R5",
        target_software=target,
    )


def _track_data(tracks):
    return [
        (
            track.track_id,
            track.track_name,
            [
                (
                    observation.production_frame,
                    observation.x_pixel,
                    observation.y_pixel,
                )
                for observation in track.observations
            ],
        )
        for track in tracks
    ]


@pytest.mark.parametrize(
    "static_fields",
    [
        ("3", "3"),
        ("0", "3"),
        ("3", "0"),
    ],
)
def test_3de_reader_accepts_verified_static_field_values(static_fields):
    assert _track_data(
        read_3de_tracks(_native_text(static_fields), _shot_config())
    ) == _track_data(
        read_3de_tracks(_native_text(("0", "0")), _shot_config())
    )


@pytest.mark.parametrize(
    "target",
    [
        "PFTRACK_2017",
        "SYNTHEYES_2304",
    ],
)
def test_3de_static_field_value_does_not_change_conversion_output(target):
    assert convert_tracks(
        _native_text(("3", "0")),
        _shot_config(target),
    ) == convert_tracks(
        _native_text(("0", "0")),
        _shot_config(target),
    )


@pytest.mark.parametrize(
    "static_field",
    [
        "1",
        "2",
        "4",
        "-1",
        "00",
        "03",
        "3.0",
        "three",
        "",
    ],
)
def test_3de_reader_rejects_unverified_static_field_values(static_field):
    with pytest.raises(ValueError):
        read_3de_tracks(
            _native_text((static_field, "0")),
            _shot_config(),
        )


@pytest.mark.parametrize(
    "static_field",
    [
        " 3",
        "3 ",
    ],
)
def test_3de_reader_still_rejects_static_field_whitespace(static_field):
    with pytest.raises(ValueError):
        read_3de_tracks(
            _native_text((static_field, "0")),
            _shot_config(),
        )


REAL_EXPORTS_ENV = "TRACKER_TOOL_3DE_REAL_EXPORTS"


@pytest.mark.skipif(
    not os.environ.get(REAL_EXPORTS_ENV),
    reason=(
        f"set {REAL_EXPORTS_ENV} to a directory of real 3DE R5 exports "
        "to run this production-data regression"
    ),
)
def test_3de_reader_reads_real_production_exports():
    paths = sorted(Path(os.environ[REAL_EXPORTS_ENV]).glob("*.txt"))

    assert paths

    for path in paths:
        tracks = read_3de_tracks(
            path.read_text(encoding="utf-8"),
            _shot_config(),
        )

        assert tracks, path.name
