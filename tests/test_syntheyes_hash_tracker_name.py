from tracker_tool.adapters.syntheyes import (
    read_syntheyes_tracks,
    write_syntheyes_tracks,
)
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import convert_tracks


# ADAPTER_SYNTHEYES_2304 §2 / §8: every row is
# <TRACKER_NAME> <FRAME> <U> <V> <OUTCOME>, and the exact tracker name is the
# grouping key. "#" is a valid tracker name; the verified grammar has no
# comment or header rows.
#
# Evidence (v1.0.1 CI-13): the "# 0 0.000000 0.000000 15" row in real
# SynthEyes re-exports is a tracker named "#" that exists in those scenes.
# Every affected scene had imported a historical pre-Core file whose first
# line was a "# ..." comment; an original artist export has no such row.
# The reader must keep treating it as a tracker, not skip it as a comment.

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


def test_syntheyes_reader_reads_hash_row_as_tracker_named_hash():
    tracks = read_syntheyes_tracks(
        HASH_ROW + TRACKER_ROWS,
        _shot_config(),
    )

    assert [
        (track.track_id, track.track_name, len(track.observations))
        for track in tracks
    ] == [
        ("syntheyes::#", "#", 1),
        ("syntheyes::Tracker0001", "Tracker0001", 2),
    ]

    observation = tracks[0].observations[0]

    assert (
        observation.production_frame,
        observation.x_pixel,
        observation.y_pixel,
    ) == (1001, 2304.0, 878.5)


def test_hash_tracker_is_preserved_through_conversion():
    native_text = convert_tracks(
        HASH_ROW + TRACKER_ROWS,
        _shot_config("3DE_R5"),
    )

    lines = native_text.splitlines()

    assert lines[0] == "2"
    assert lines[1] == "#"


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
