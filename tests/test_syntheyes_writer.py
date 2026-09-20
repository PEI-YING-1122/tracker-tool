import pytest
from tracker_tool.adapters.syntheyes import (
    read_syntheyes_tracks,
    write_syntheyes_tracks,
)
from tracker_tool.canonical import Observation, Track
from tracker_tool.config import ShotConfig


def test_syntheyes_writer_serializes_single_track():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Tracker0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=960.0,
                    y_pixel=540.0,
                ),
                Observation(
                    production_frame=1002,
                    x_pixel=480.0,
                    y_pixel=270.0,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=1440.0,
                    y_pixel=810.0,
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
        target_software="SynthEyes 2304",
    )

    native_text = write_syntheyes_tracks(
        tracks,
        shot_config,
    )

    assert native_text == (
        "Tracker0001 0 0.000000000 0.000000000 15\n"
        "Tracker0001 1 -0.500000000 0.500000000 15\n"
        "Tracker0001 3 0.500000000 -0.500000000 15\n"
    )

def test_syntheyes_writer_serializes_multiple_tracks():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Tracker0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=960.0,
                    y_pixel=540.0,
                ),
                Observation(
                    production_frame=1003,
                    x_pixel=1440.0,
                    y_pixel=810.0,
                ),
            ],
        ),
        Track(
            track_id="source::002",
            track_name="Tracker0002",
            observations=[
                Observation(
                    production_frame=1002,
                    x_pixel=480.0,
                    y_pixel=270.0,
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
        target_software="SynthEyes 2304",
    )

    native_text = write_syntheyes_tracks(
        tracks,
        shot_config,
    )

    assert native_text == (
        "Tracker0001 0 0.000000000 0.000000000 15\n"
        "Tracker0001 2 0.500000000 -0.500000000 15\n"
        "Tracker0002 1 -0.500000000 0.500000000 15\n"
    )

def test_syntheyes_writer_uses_track_name_not_track_id():
    tracks = [
        Track(
            track_id="syntheyes::Tracker0001",
            track_name="Tracker0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=960.0,
                    y_pixel=540.0,
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
        target_software="SynthEyes 2304",
    )

    native_text = write_syntheyes_tracks(
        tracks,
        shot_config,
    )

    assert "Tracker0001 0 " in native_text
    assert "syntheyes::Tracker0001" not in native_text

def test_syntheyes_writer_round_trip_preserves_track_data():
    source_tracks = [
        Track(
            track_id="source::001",
            track_name="Tracker0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=960.0,
                    y_pixel=540.0,
                ),
                Observation(
                    production_frame=1002,
                    x_pixel=480.0,
                    y_pixel=270.0,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=1440.0,
                    y_pixel=810.0,
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
        target_software="SynthEyes 2304",
    )

    native_text = write_syntheyes_tracks(
        source_tracks,
        shot_config,
    )

    round_trip_tracks = read_syntheyes_tracks(
        native_text,
        shot_config,
    )

    assert len(round_trip_tracks) == 1

    round_trip_track = round_trip_tracks[0]

    assert round_trip_track.track_name == "Tracker0001"

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
        (960.0, 540.0),
        (480.0, 270.0),
        (1440.0, 810.0),
    ]

def test_syntheyes_writer_round_trip_preserves_multiple_tracks():
    source_tracks = [
        Track(
            track_id="source::001",
            track_name="Tracker0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=960.0,
                    y_pixel=540.0,
                ),
                Observation(
                    production_frame=1003,
                    x_pixel=1440.0,
                    y_pixel=810.0,
                ),
            ],
        ),
        Track(
            track_id="source::002",
            track_name="Tracker0002",
            observations=[
                Observation(
                    production_frame=1002,
                    x_pixel=480.0,
                    y_pixel=270.0,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=240.0,
                    y_pixel=135.0,
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
        target_software="SynthEyes 2304",
    )

    native_text = write_syntheyes_tracks(
        source_tracks,
        shot_config,
    )

    round_trip_tracks = read_syntheyes_tracks(
        native_text,
        shot_config,
    )

    assert len(round_trip_tracks) == 2

    assert round_trip_tracks[0].track_name == "Tracker0001"
    assert round_trip_tracks[1].track_name == "Tracker0002"

    assert [
        observation.production_frame
        for observation in round_trip_tracks[0].observations
    ] == [1001, 1003]

    assert [
        observation.production_frame
        for observation in round_trip_tracks[1].observations
    ] == [1002, 1004]

def test_syntheyes_writer_round_trip_preserves_subpixel_coordinates():
    source_tracks = [
        Track(
            track_id="source::001",
            track_name="Tracker0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.25,
                    y_pixel=200.5,
                ),
                Observation(
                    production_frame=1002,
                    x_pixel=347.123456,
                    y_pixel=512.654321,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=1524.375,
                    y_pixel=777.125,
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
        target_software="SynthEyes 2304",
    )

    native_text = write_syntheyes_tracks(
        source_tracks,
        shot_config,
    )

    round_trip_tracks = read_syntheyes_tracks(
        native_text,
        shot_config,
    )

    round_trip_observations = (
        round_trip_tracks[0].observations
    )

    assert [
        observation.production_frame
        for observation in round_trip_observations
    ] == [1001, 1002, 1004]

    expected_coordinates = [
        (100.25, 200.5),
        (347.123456, 512.654321),
        (1524.375, 777.125),
    ]

    for observation, (expected_x, expected_y) in zip(
        round_trip_observations,
        expected_coordinates,
    ):
        assert observation.x_pixel == pytest.approx(
            expected_x,
            abs=0.001,
        )

        assert observation.y_pixel == pytest.approx(
            expected_y,
            abs=0.001,
        )

def test_syntheyes_writer_uses_nine_decimal_digits_for_uv():
    tracks = [
        Track(
            track_id="source::001",
            track_name="Tracker0001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.25,
                    y_pixel=200.5,
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
        target_software="SynthEyes 2304",
    )

    native_text = write_syntheyes_tracks(
        tracks,
        shot_config,
    )

    row = native_text.strip()
    fields = row.split()

    u_text = fields[2]
    v_text = fields[3]

    assert len(u_text.split(".")[1]) >= 9
    assert len(v_text.split(".")[1]) >= 9

def test_syntheyes_writer_rejects_track_name_with_whitespace():
    tracks = [
        Track(
            track_id="test::1",
            track_name="Point 001",
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
        production_end_frame=None,
        source_software="3DE_R5",
        target_software="SYNTHEYES_2304",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes track name cannot contain whitespace",
    ):
        write_syntheyes_tracks(
            tracks,
            shot_config,
        )

def test_syntheyes_writer_rejects_duplicate_target_track_names():
    tracks = [
        Track(
            track_id="test::1",
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
            track_id="test::2",
            track_name="Point0001",
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
        production_end_frame=None,
        source_software="3DE_R5",
        target_software="SYNTHEYES_2304",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes target track names must be unique",
    ):
        write_syntheyes_tracks(
            tracks,
            shot_config,
        )