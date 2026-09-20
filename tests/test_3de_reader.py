import pytest

from tracker_tool.adapters.threed import read_3de_tracks
from tracker_tool.config import ShotConfig


def test_3de_reader_maps_single_track_to_canonical():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "3\n"
        "1 100.25 200.5\n"
        "2 101.25 201.5\n"
        "4 103.25 203.5\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    tracks = read_3de_tracks(native_text, shot_config)

    assert len(tracks) == 1

    track = tracks[0]

    assert track.track_id == "3de::000001::Point0001"
    assert track.track_name == "Point0001"

    assert [
        observation.production_frame
        for observation in track.observations
    ] == [1001, 1002, 1004]

    assert [
        (observation.x_pixel, observation.y_pixel)
        for observation in track.observations
    ] == [
        (100.25, 200.5),
        (101.25, 201.5),
        (103.25, 203.5),
    ]

def test_3de_reader_keeps_same_name_tracks_as_separate_identities():
    native_text = (
        "2\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "2 300.0 400.0\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    tracks = read_3de_tracks(native_text, shot_config)

    assert len(tracks) == 2

    assert tracks[0].track_id == "3de::000001::Point0001"
    assert tracks[1].track_id == "3de::000002::Point0001"

    assert tracks[0].track_name == "Point0001"
    assert tracks[1].track_name == "Point0001"

    assert tracks[0].track_id != tracks[1].track_id

def test_3de_reader_rejects_trailing_track_data_beyond_declared_track_count():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
        "Point0002\n"
        "0\n"
        "1\n"
        "2 300.0 400.0\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    with pytest.raises(ValueError):
        read_3de_tracks(native_text, shot_config)

def test_3de_reader_rejects_missing_observation_rows_for_declared_sample_count():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "3\n"
        "1 100.0 200.0\n"
        "2 101.0 201.0\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    with pytest.raises(ValueError):
        read_3de_tracks(native_text, shot_config)

def test_3de_reader_rejects_blank_line_between_track_blocks():
    native_text = (
        "2\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
        "\n"
        "Point0002\n"
        "0\n"
        "1\n"
        "2 300.0 400.0\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    with pytest.raises(ValueError):
        read_3de_tracks(native_text, shot_config)


def test_3de_reader_rejects_leading_space_on_track_count():
    native_text = (
        " 1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    with pytest.raises(ValueError):
        read_3de_tracks(native_text, shot_config)

@pytest.mark.parametrize(
    "native_text",
    [
        (
            "1\n"
            "Point0001 \n"
            "0\n"
            "1\n"
            "1 100.0 200.0\n"
        ),
        (
            "1\n"
            "Point0001\n"
            " 0\n"
            "1\n"
            "1 100.0 200.0\n"
        ),
        (
            "1\n"
            "Point0001\n"
            "0\n"
            "1 \n"
            "1 100.0 200.0\n"
        ),
    ],
)
def test_3de_reader_rejects_whitespace_on_structural_lines(native_text):
    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    with pytest.raises(ValueError):
        read_3de_tracks(native_text, shot_config)

@pytest.mark.parametrize(
    "x_text,y_text",
    [
        ("nan", "200.0"),
        ("inf", "200.0"),
        ("100.0", "-inf"),
    ],
)
def test_3de_reader_rejects_non_finite_coordinates(
    x_text,
    y_text,
):
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        f"1 {x_text} {y_text}\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    with pytest.raises(ValueError):
        read_3de_tracks(native_text, shot_config)

def test_3de_reader_rejects_duplicate_frame_within_same_track():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "2\n"
        "1 100.0 200.0\n"
        "1 300.0 400.0\n"
    )

    shot_config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    with pytest.raises(ValueError):
        read_3de_tracks(native_text, shot_config)
