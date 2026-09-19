import pytest
from tracker_tool.adapters.syntheyes import read_syntheyes_tracks
from tracker_tool.config import ShotConfig


def test_syntheyes_reader_maps_single_tracker_to_canonical():
    native_text = (
        "Tracker0001 0 0.0 0.0 15\n"
        "Tracker0001 1 -0.5 0.5 15\n"
        "Tracker0001 3 0.5 -0.5 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    tracks = read_syntheyes_tracks(
        native_text,
        shot_config,
    )

    assert len(tracks) == 1

    track = tracks[0]

    assert track.track_id == "syntheyes::Tracker0001"
    assert track.track_name == "Tracker0001"

    assert [
        observation.production_frame
        for observation in track.observations
    ] == [1001, 1002, 1004]

    assert [
        (observation.x_pixel, observation.y_pixel)
        for observation in track.observations
    ] == [
        (960.0, 540.0),
        (480.0, 270.0),
        (1440.0, 810.0),
    ]

def test_syntheyes_reader_groups_multiple_trackers_by_exact_name():
    native_text = (
        "Tracker0001 0 0.0 0.0 15\n"
        "Tracker0002 0 -0.5 0.5 15\n"
        "Tracker0001 2 0.5 -0.5 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    tracks = read_syntheyes_tracks(
        native_text,
        shot_config,
    )

    assert len(tracks) == 2

    assert tracks[0].track_id == "syntheyes::Tracker0001"
    assert tracks[0].track_name == "Tracker0001"

    assert [
        observation.production_frame
        for observation in tracks[0].observations
    ] == [1001, 1003]

    assert tracks[1].track_id == "syntheyes::Tracker0002"
    assert tracks[1].track_name == "Tracker0002"

    assert [
        observation.production_frame
        for observation in tracks[1].observations
    ] == [1001]

@pytest.mark.parametrize(
    "native_text",
    [
        "Tracker0001 0 0.0 0.0\n",
        "Tracker0001 0 0.0 0.0 15 EXTRA\n",
    ],
)
def test_syntheyes_reader_rejects_wrong_field_count(native_text):
    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes row must contain exactly 5 fields",
    ):
        read_syntheyes_tracks(
            native_text,
            shot_config,
        )

@pytest.mark.parametrize(
    "frame_text",
    [
        "1.5",
        "abc",
    ],
)
def test_syntheyes_reader_rejects_non_integer_frame(frame_text):
    native_text = (
        f"Tracker0001 {frame_text} 0.0 0.0 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes frame must be an integer",
    ):
        read_syntheyes_tracks(
            native_text,
            shot_config,
        )

@pytest.mark.parametrize(
    "u_text,v_text",
    [
        ("nan", "0.0"),
        ("inf", "0.0"),
        ("0.0", "-inf"),
    ],
)
def test_syntheyes_reader_rejects_non_finite_uv(
    u_text,
    v_text,
):
    native_text = (
        f"Tracker0001 0 {u_text} {v_text} 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes U/V must be finite",
    ):
        read_syntheyes_tracks(
            native_text,
            shot_config,
        )

@pytest.mark.parametrize(
    "outcome_text",
    [
        "15.5",
        "abc",
    ],
)
def test_syntheyes_reader_rejects_non_integer_outcome(
    outcome_text,
):
    native_text = (
        f"Tracker0001 0 0.0 0.0 {outcome_text}\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes Outcome must be an integer",
    ):
        read_syntheyes_tracks(
            native_text,
            shot_config,
        )

def test_syntheyes_reader_rejects_duplicate_frame_within_same_tracker():
    native_text = (
        "Tracker0001 0 0.0 0.0 15\n"
        "Tracker0001 0 0.5 -0.5 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes track contains duplicate frame observations",
    ):
        read_syntheyes_tracks(
            native_text,
            shot_config,
        )

def test_syntheyes_reader_preserves_exact_tracker_names():
    native_text = (
        "Tracker0001 0 0.0 0.0 15\n"
        "tracker0001 0 0.5 0.5 15\n"
        "Tracker001 0 -0.5 -0.5 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    tracks = read_syntheyes_tracks(
        native_text,
        shot_config,
    )

    assert len(tracks) == 3

    assert [track.track_id for track in tracks] == [
        "syntheyes::Tracker0001",
        "syntheyes::tracker0001",
        "syntheyes::Tracker001",
    ]

    assert [track.track_name for track in tracks] == [
        "Tracker0001",
        "tracker0001",
        "Tracker001",
    ]

@pytest.mark.parametrize(
    "u_text,v_text",
    [
        ("abc", "0.0"),
        ("0.0", "xyz"),
    ],
)
def test_syntheyes_reader_rejects_non_numeric_uv(
    u_text,
    v_text,
):
    native_text = (
        f"Tracker0001 0 {u_text} {v_text} 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes U/V must be numeric",
    ):
        read_syntheyes_tracks(
            native_text,
            shot_config,
        )

def test_syntheyes_reader_rejects_blank_row_between_observations():
    native_text = (
        "Tracker0001 0 0.0 0.0 15\n"
        "\n"
        "Tracker0001 1 0.1 0.1 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SynthEyes 2304",
        target_software="Canonical",
    )

    with pytest.raises(
        ValueError,
        match="SynthEyes row must contain exactly 5 fields",
    ):
        read_syntheyes_tracks(
            native_text,
            shot_config,
        )