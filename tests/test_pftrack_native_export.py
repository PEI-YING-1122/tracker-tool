import os
from pathlib import Path

import pytest

from tracker_tool import main
from tracker_tool.adapters.pftrack import (
    read_pftrack_source_set,
    read_pftrack_tracks,
)
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import (
    convert_pftrack_source_set,
    convert_tracks,
)


# Layout of real PFTrack 2017 exports (characterized from 11 production
# exports, including the Test 08 AutoTrack / UserTrack source set):
#
#   4 header lines (two verified variants, differing only in line 4)
#   exactly one blank line before every track block, including the first
#   no other blank lines, no trailing blank line, CRLF newlines
#   observation rows always have 4 values, even when the header lists zdepth
#
# The production files are not stored in this public repository. The
# fixtures below reproduce the layout with synthetic values.

HEADER_WITH_ZDEPTH = (
    '# "Name"\n'
    "# clipNumber\n"
    "# frameCount\n"
    "# frame, xpos, ypos, similarity, zdepth\n"
)

HEADER_WITHOUT_ZDEPTH = (
    '# "Name"\n'
    "# clipNumber\n"
    "# frameCount\n"
    "# frame, xpos, ypos, similarity\n"
)

BLOCK_A = (
    '"Tracker0001"\n'
    "1\n"
    "3\n"
    "1001 1500.250000 1200.500000 1.000000\n"
    "1002 1510.750000 1195.125000 0.998000\n"
    "1004 1532.000000 1187.375000 0.997000\n"
)

BLOCK_B = (
    '"Tracker0002"\n'
    "1\n"
    "2\n"
    "1003 -12.500000 2210.250000 0.950000\n"
    "1005 10.000000 20.000000 0.990000\n"
)

HEADERLESS_TEXT = BLOCK_A + BLOCK_B


def _export_text(header, blocks):
    return header + "".join(
        "\n" + block
        for block in blocks
    )


def _shot_config(target):
    return ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="PFTRACK_2017",
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
    "header",
    [
        HEADER_WITH_ZDEPTH,
        HEADER_WITHOUT_ZDEPTH,
    ],
)
@pytest.mark.parametrize(
    "source_role",
    [
        "AUTOTRACK",
        "USERTRACK",
    ],
)
def test_pftrack_reader_accepts_native_export_layout(
    header,
    source_role,
):
    tracks = read_pftrack_tracks(
        _export_text(header, [BLOCK_A, BLOCK_B]),
        source_role=source_role,
    )

    assert _track_data(tracks) == _track_data(
        read_pftrack_tracks(
            HEADERLESS_TEXT,
            source_role=source_role,
        )
    )


def test_pftrack_reader_maps_native_export_to_canonical():
    tracks = read_pftrack_tracks(
        _export_text(HEADER_WITH_ZDEPTH, [BLOCK_A, BLOCK_B]),
        source_role="AUTOTRACK",
    )

    assert _track_data(tracks) == [
        (
            "pf_autotrack::Tracker0001",
            "Tracker0001",
            [
                (1001, 1500.25, 1200.5),
                (1002, 1510.75, 1195.125),
                (1004, 1532.0, 1187.375),
            ],
        ),
        (
            "pf_autotrack::Tracker0002",
            "Tracker0002",
            [
                (1003, -12.5, 2210.25),
                (1005, 10.0, 20.0),
            ],
        ),
    ]


def test_pftrack_reader_accepts_native_export_with_single_track():
    tracks = read_pftrack_tracks(
        _export_text(HEADER_WITHOUT_ZDEPTH, [BLOCK_A]),
        source_role="USERTRACK",
    )

    assert [track.track_name for track in tracks] == ["Tracker0001"]


@pytest.mark.parametrize(
    "target",
    [
        "3DE_R5",
        "SYNTHEYES_2304",
    ],
)
def test_native_export_converts_like_headerless_equivalent(target):
    assert convert_tracks(
        _export_text(HEADER_WITH_ZDEPTH, [BLOCK_A, BLOCK_B]),
        _shot_config(target),
        pftrack_source_role="AUTOTRACK",
    ) == convert_tracks(
        HEADERLESS_TEXT,
        _shot_config(target),
        pftrack_source_role="AUTOTRACK",
    )


@pytest.mark.parametrize(
    "target",
    [
        "3DE_R5",
        "SYNTHEYES_2304",
    ],
)
def test_native_export_source_set_converts_like_headerless_equivalent(
    target,
):
    assert convert_pftrack_source_set(
        _export_text(HEADER_WITHOUT_ZDEPTH, [BLOCK_A]),
        _export_text(HEADER_WITH_ZDEPTH, [BLOCK_B]),
        _shot_config(target),
    ) == convert_pftrack_source_set(
        BLOCK_A,
        BLOCK_B,
        _shot_config(target),
    )


def test_native_export_source_set_still_rejects_cross_source_collision():
    with pytest.raises(
        ValueError,
        match="CROSS_SOURCE_TRACK_NAME_COLLISION",
    ):
        read_pftrack_source_set(
            autotrack_text=_export_text(HEADER_WITH_ZDEPTH, [BLOCK_A]),
            usertrack_text=_export_text(HEADER_WITH_ZDEPTH, [BLOCK_A]),
        )


@pytest.mark.parametrize(
    "target",
    [
        "3DE_R5",
        "SYNTHEYES_2304",
    ],
)
def test_cli_converts_crlf_native_export_file(tmp_path, target):
    export_path = tmp_path / "pftrack_export.txt"
    headerless_path = tmp_path / "pftrack_headerless.txt"
    export_output = tmp_path / "from_export.txt"
    headerless_output = tmp_path / "from_headerless.txt"

    export_path.write_bytes(
        _export_text(HEADER_WITH_ZDEPTH, [BLOCK_A, BLOCK_B])
        .replace("\n", "\r\n")
        .encode("utf-8")
    )
    headerless_path.write_bytes(
        HEADERLESS_TEXT.encode("utf-8")
    )

    for input_path, output_path in [
        (export_path, export_output),
        (headerless_path, headerless_output),
    ]:
        assert main(
            [
                "convert",
                "--source",
                "PFTRACK_2017",
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
                "--pftrack-source-role",
                "AUTOTRACK",
            ]
        ) == 0

    assert export_output.read_bytes() == headerless_output.read_bytes()


@pytest.mark.parametrize(
    ("description", "native_text"),
    [
        (
            "unknown header line",
            _export_text(
                HEADER_WITH_ZDEPTH.replace(
                    "similarity, zdepth",
                    "similarity, zdepth, extra",
                ),
                [BLOCK_A],
            ),
        ),
        (
            "incomplete header",
            '# "Name"\n# clipNumber\n# frameCount\n' + "\n" + BLOCK_A,
        ),
        (
            "header line with trailing whitespace",
            _export_text(
                HEADER_WITH_ZDEPTH.replace(
                    "# clipNumber\n",
                    "# clipNumber \n",
                ),
                [BLOCK_A],
            ),
        ),
        (
            "header repeated in the middle of the file",
            _export_text(HEADER_WITH_ZDEPTH, [BLOCK_A])
            + "\n"
            + HEADER_WITH_ZDEPTH
            + "\n"
            + BLOCK_B,
        ),
        (
            "comment line between track blocks",
            _export_text(HEADER_WITH_ZDEPTH, [BLOCK_A])
            + "# comment\n"
            + "\n"
            + BLOCK_B,
        ),
        (
            "header without separator before first block",
            HEADER_WITH_ZDEPTH + BLOCK_A,
        ),
        (
            "missing separator between track blocks",
            HEADER_WITH_ZDEPTH + "\n" + BLOCK_A + BLOCK_B,
        ),
        (
            "two blank lines between track blocks",
            HEADER_WITH_ZDEPTH + "\n" + BLOCK_A + "\n\n" + BLOCK_B,
        ),
        (
            "trailing blank line",
            _export_text(HEADER_WITH_ZDEPTH, [BLOCK_A]) + "\n",
        ),
        (
            "whitespace-only separator line",
            HEADER_WITH_ZDEPTH + " \n" + BLOCK_A,
        ),
        (
            "blank line after track name",
            HEADER_WITH_ZDEPTH
            + "\n"
            + BLOCK_A.replace('"Tracker0001"\n', '"Tracker0001"\n\n'),
        ),
        (
            "blank line after clipNumber",
            HEADER_WITH_ZDEPTH
            + "\n"
            + BLOCK_A.replace('"Tracker0001"\n1\n', '"Tracker0001"\n1\n\n'),
        ),
        (
            "blank line between observation rows",
            HEADER_WITH_ZDEPTH
            + "\n"
            + BLOCK_A.replace(
                "1.000000\n1002",
                "1.000000\n\n1002",
            ),
        ),
        (
            "headerless data with separator blank lines",
            BLOCK_A + "\n" + BLOCK_B,
        ),
        (
            "headerless data with leading blank line",
            "\n" + BLOCK_A,
        ),
        (
            "header with five-value observation rows",
            HEADER_WITH_ZDEPTH
            + "\n"
            + '"Tracker0001"\n1\n1\n1001 1.0 2.0 1.000000 0.000000\n',
        ),
    ],
)
def test_pftrack_reader_rejects_unverified_layout(description, native_text):
    with pytest.raises(ValueError):
        read_pftrack_tracks(
            native_text,
            source_role="AUTOTRACK",
        )


REAL_EXPORTS_ENV = "TRACKER_TOOL_PFTRACK_REAL_EXPORTS"


def _real_export_paths():
    directory = os.environ.get(REAL_EXPORTS_ENV)

    if not directory:
        return []

    return sorted(Path(directory).glob("*.txt"))


@pytest.mark.skipif(
    not os.environ.get(REAL_EXPORTS_ENV),
    reason=(
        f"set {REAL_EXPORTS_ENV} to a directory of real PFTrack 2017 "
        "exports to run this production-data regression"
    ),
)
def test_pftrack_reader_reads_real_production_exports():
    paths = _real_export_paths()

    assert paths

    for path in paths:
        native_text = path.read_text(encoding="utf-8")
        lines = native_text.splitlines()

        tracks = read_pftrack_tracks(
            native_text,
            source_role="AUTOTRACK",
        )

        assert len(tracks) == sum(
            line.startswith('"')
            for line in lines
        ), path.name

        assert sum(
            len(track.observations)
            for track in tracks
        ) == sum(
            len(line.split()) == 4
            for line in lines
            if not line.startswith("#")
        ), path.name
