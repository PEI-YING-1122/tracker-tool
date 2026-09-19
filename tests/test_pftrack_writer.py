from tracker_tool.adapters.pftrack import (
    read_pftrack_tracks,
    write_pftrack_tracks,
)
from tracker_tool.canonical import Observation, Track


def test_pftrack_writer_serializes_single_track():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Track0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.25,
                    y_pixel=200.5,
                ),
                Observation(
                    production_frame=1002,
                    x_pixel=101.25,
                    y_pixel=201.5,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=103.25,
                    y_pixel=203.5,
                ),
            ],
        )
    ]

    native_text = write_pftrack_tracks(tracks)

    assert native_text == (
        '"Track0001"\n'
        "1\n"
        "3\n"
        "1001 100.25 200.5 1.000000\n"
        "1002 101.25 201.5 1.000000\n"
        "1004 103.25 203.5 1.000000\n"
    )

def test_pftrack_writer_serializes_multiple_tracks():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Track0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                ),
                Observation(
                    production_frame=1003,
                    x_pixel=102.0,
                    y_pixel=202.0,
                ),
            ],
        ),
        Track(
            track_id="source::002",
            track_name="Track0002",
            observations=[
                Observation(
                    production_frame=1002,
                    x_pixel=300.0,
                    y_pixel=400.0,
                ),
            ],
        ),
    ]

    native_text = write_pftrack_tracks(tracks)

    assert native_text == (
        '"Track0001"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 1.000000\n"
        "1003 102.0 202.0 1.000000\n"
        '"Track0002"\n'
        "1\n"
        "1\n"
        "1002 300.0 400.0 1.000000\n"
    )

def test_pftrack_writer_uses_track_name_not_track_id():
    tracks = [
        Track(
            track_id="pf_autotrack::Auto000084",
            track_name="Auto000084",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    native_text = write_pftrack_tracks(tracks)

    assert '"Auto000084"\n' in native_text
    assert "pf_autotrack::Auto000084" not in native_text

def test_pftrack_writer_round_trip_preserves_track_data():
    source_tracks = [
        Track(
            track_id="source::001",
            track_name="Track0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.25,
                    y_pixel=200.5,
                ),
                Observation(
                    production_frame=1002,
                    x_pixel=101.25,
                    y_pixel=201.5,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=103.25,
                    y_pixel=203.5,
                ),
            ],
        )
    ]

    native_text = write_pftrack_tracks(source_tracks)

    round_trip_tracks = read_pftrack_tracks(
        native_text,
        source_role="AUTOTRACK",
    )

    assert len(round_trip_tracks) == 1

    round_trip_track = round_trip_tracks[0]

    assert round_trip_track.track_name == "Track0001"

    assert [
        observation.production_frame
        for observation in round_trip_track.observations
    ] == [1001, 1002, 1004]

    assert [
        (
            observation.x_pixel,
            observation.y_pixel,
        )
        for observation in round_trip_track.observations
    ] == [
        (100.25, 200.5),
        (101.25, 201.5),
        (103.25, 203.5),
    ]

def test_pftrack_writer_round_trip_preserves_multiple_tracks():
    source_tracks = [
        Track(
            track_id="source::001",
            track_name="Track0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                ),
                Observation(
                    production_frame=1003,
                    x_pixel=102.0,
                    y_pixel=202.0,
                ),
            ],
        ),
        Track(
            track_id="source::002",
            track_name="Track0002",
            observations=[
                Observation(
                    production_frame=1002,
                    x_pixel=300.0,
                    y_pixel=400.0,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=302.0,
                    y_pixel=402.0,
                ),
            ],
        ),
    ]

    native_text = write_pftrack_tracks(source_tracks)

    round_trip_tracks = read_pftrack_tracks(
        native_text,
        source_role="AUTOTRACK",
    )

    assert len(round_trip_tracks) == 2

    assert round_trip_tracks[0].track_name == "Track0001"
    assert round_trip_tracks[1].track_name == "Track0002"

    assert [
        observation.production_frame
        for observation in round_trip_tracks[0].observations
    ] == [1001, 1003]

    assert [
        observation.production_frame
        for observation in round_trip_tracks[1].observations
    ] == [1002, 1004]