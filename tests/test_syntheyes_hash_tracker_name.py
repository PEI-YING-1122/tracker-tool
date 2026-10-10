import pytest

from tracker_tool import main
from tracker_tool.adapters.syntheyes import (
    read_syntheyes_tracks,
    write_syntheyes_tracks,
)
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import convert_tracks


# ADAPTER_SYNTHEYES_2304 §2 / §8: every row is
# <TRACKER_NAME> <FRAME> <U> <V> <OUTCOME>; the grammar has no header or
# comment rows.
#
# CI-13 (v1.0.1), approved as a conservative input guard against a source
# data integrity risk. In every verified case, a tracker named "#" came from
# SynthEyes importing a file whose first line started with "#"; a re-export
# of a scene built without "#" lines has no such row (A6-a). This does not
# mean every tracker named "#" is junk.
#
# The reader stops with an explicit error instead of carrying the tracker
# into the target. It never skips or deletes rows silently.

HASH_ROW = "# 0 0.000000 0.000000 15\n"
TRACKER_ROWS = (
    "Tracker0001 0 -0.250000000 -0.500000000 15\n"
    "Tracker0001 2 -0.240000000 -0.490000000 15\n"
)


def _shot_config(target="3DE_R5"):
    return ShotConfig(
        image_width=4608,
        image_height=1757,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="SYNTHEYES_2304",
        target_software=target,
    )


@pytest.mark.parametrize(
    "native_text",
    [
        HASH_ROW + TRACKER_ROWS,
        TRACKER_ROWS + HASH_ROW,
        HASH_ROW,
    ],
)
def test_syntheyes_reader_stops_on_tracker_named_hash(native_text):
    with pytest.raises(ValueError, match="'#'"):
        read_syntheyes_tracks(native_text, _shot_config())


@pytest.mark.parametrize(
    "target",
    [
        "3DE_R5",
        "PFTRACK_2017",
    ],
)
def test_conversion_stops_instead_of_writing_hash_tracker(target):
    with pytest.raises(ValueError):
        convert_tracks(
            HASH_ROW + TRACKER_ROWS,
            _shot_config(target),
        )


def test_cli_writes_no_output_for_hash_tracker(tmp_path):
    input_path = tmp_path / "syntheyes_export.txt"
    output_path = tmp_path / "output_3de.txt"

    input_path.write_text(
        HASH_ROW + TRACKER_ROWS,
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        main(
            [
                "convert",
                "--source",
                "SYNTHEYES_2304",
                "--target",
                "3DE_R5",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "4608",
                "--height",
                "1757",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()


@pytest.mark.parametrize(
    "tracker_name",
    [
        "#1",
        "Tracker#1",
        "##",
    ],
)
def test_other_names_containing_hash_are_still_tracker_names(tracker_name):
    # Only the evidenced name "#" is stopped. Other names are not guessed
    # to be comments.
    tracks = read_syntheyes_tracks(
        f"{tracker_name} 0 0.100000000 0.200000000 15\n",
        _shot_config(),
    )

    assert [track.track_name for track in tracks] == [tracker_name]


def test_syntheyes_export_without_hash_row_still_converts():
    native_text = convert_tracks(
        TRACKER_ROWS,
        _shot_config("3DE_R5"),
    )

    assert native_text.splitlines()[:2] == ["1", "Tracker0001"]


def test_syntheyes_writer_emits_only_tracker_rows():
    tracks = read_syntheyes_tracks(
        TRACKER_ROWS,
        _shot_config(),
    )

    native_text = write_syntheyes_tracks(
        tracks,
        _shot_config(),
    )

    assert all(
        line.startswith("Tracker0001 ")
        for line in native_text.splitlines()
    )
