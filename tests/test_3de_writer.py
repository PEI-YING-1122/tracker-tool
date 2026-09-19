from tracker_tool.adapters.threed import (
    read_3de_tracks,
    write_3de_tracks,
)
from tracker_tool.canonical import Observation, Track
from tracker_tool.config import ShotConfig


def test_3de_writer_serializes_single_track():
    tracks = [
        Track(
            track_id="source::internal::001",
            track_name="Point0001",
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

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        tracks,
        shot_config,
    )

    assert native_text == (
        "1\n"
        "Point0001\n"
        "0\n"
        "3\n"
        "1 100.25 200.5\n"
        "2 101.25 201.5\n"
        "4 103.25 203.5\n"
    )

def test_3de_writer_serializes_multiple_tracks():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Point0001",
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
            track_name="Point0002",
            observations=[
                Observation(
                    production_frame=1002,
                    x_pixel=300.0,
                    y_pixel=400.0,
                ),
            ],
        ),
    ]

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        tracks,
        shot_config,
    )

    assert native_text == (
        "2\n"
        "Point0001\n"
        "0\n"
        "2\n"
        "1 100.0 200.0\n"
        "3 102.0 202.0\n"
        "Point0002\n"
        "0\n"
        "1\n"
        "2 300.0 400.0\n"
    )

def test_3de_writer_emits_no_blank_lines():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Point0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        ),
        Track(
            track_id="source::002",
            track_name="Point0002",
            observations=[
                Observation(
                    production_frame=1002,
                    x_pixel=300.0,
                    y_pixel=400.0,
                )
            ],
        ),
    ]

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        tracks,
        shot_config,
    )

    assert "\n\n" not in native_text

def test_3de_writer_emits_no_structural_line_whitespace():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Point0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        tracks,
        shot_config,
    )

    lines = native_text.splitlines()

    assert lines[0] == lines[0].strip()
    assert lines[1] == lines[1].strip()
    assert lines[2] == lines[2].strip()
    assert lines[3] == lines[3].strip()

def test_3de_writer_sample_count_uses_actual_observation_count():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Point0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=103.0,
                    y_pixel=203.0,
                ),
            ],
        )
    ]

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        tracks,
        shot_config,
    )

    assert native_text == (
        "1\n"
        "Point0001\n"
        "0\n"
        "2\n"
        "1 100.0 200.0\n"
        "4 103.0 203.0\n"
    )

def test_3de_writer_round_trip_preserves_track_data():
    source_tracks = [
        Track(
            track_id="source::001",
            track_name="Point0001",
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

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        source_tracks,
        shot_config,
    )

    round_trip_tracks = read_3de_tracks(
        native_text,
        shot_config,
    )

    assert len(round_trip_tracks) == 1

    round_trip_track = round_trip_tracks[0]

    assert round_trip_track.track_name == "Point0001"

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

def test_3de_writer_round_trip_preserves_multiple_tracks():
    source_tracks = [
        Track(
            track_id="source::001",
            track_name="Point0001",
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
            track_name="Point0002",
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

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        source_tracks,
        shot_config,
    )

    round_trip_tracks = read_3de_tracks(
        native_text,
        shot_config,
    )

    assert len(round_trip_tracks) == 2

    assert round_trip_tracks[0].track_name == "Point0001"
    assert round_trip_tracks[1].track_name == "Point0002"

    assert [
        observation.production_frame
        for observation in round_trip_tracks[0].observations
    ] == [1001, 1003]

    assert [
        observation.production_frame
        for observation in round_trip_tracks[1].observations
    ] == [1002, 1004]

    assert [
        (
            observation.x_pixel,
            observation.y_pixel,
        )
        for observation in round_trip_tracks[0].observations
    ] == [
        (100.0, 200.0),
        (102.0, 202.0),
    ]

    assert [
        (
            observation.x_pixel,
            observation.y_pixel,
        )
        for observation in round_trip_tracks[1].observations
    ] == [
        (300.0, 400.0),
        (302.0, 402.0),
    ]

def test_3de_writer_uses_track_name_not_track_id():
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

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="Canonical",
        target_software="3DE R5",
    )

    native_text = write_3de_tracks(
        tracks,
        shot_config,
    )

    assert "Auto000084\n" in native_text
    assert "pf_autotrack::Auto000084" not in native_text