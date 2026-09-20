import pytest

from tracker_tool.canonical import (
    Observation,
    Track,
    validate_canonical_tracks,
)


def test_canonical_validation_rejects_duplicate_track_id():
    tracks = [
        Track(
            track_id="track::001",
            track_name="TrackA",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        ),
        Track(
            track_id="track::001",
            track_name="TrackB",
            observations=[
                Observation(
                    production_frame=1002,
                    x_pixel=300.0,
                    y_pixel=400.0,
                )
            ],
        ),
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

def test_canonical_validation_rejects_non_string_track_id():
    tracks = [
        Track(
            track_id=123,
            track_name="TrackA",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

def test_canonical_validation_rejects_non_string_track_name():
    tracks = [
        Track(
            track_id="track::001",
            track_name=123,
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

@pytest.mark.parametrize(
    "x_pixel,y_pixel",
    [
        ("abc", 200.0),
        (100.0, "xyz"),
    ],
)
def test_canonical_validation_rejects_non_numeric_coordinates(
    x_pixel,
    y_pixel,
):
    tracks = [
        Track(
            track_id="track::001",
            track_name="TrackA",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=x_pixel,
                    y_pixel=y_pixel,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

@pytest.mark.parametrize(
    "x_pixel,y_pixel",
    [
        (float("nan"), 200.0),
        (float("inf"), 200.0),
        (100.0, float("-inf")),
    ],
)
def test_canonical_validation_rejects_non_finite_coordinates(
    x_pixel,
    y_pixel,
):
    tracks = [
        Track(
            track_id="track::001",
            track_name="TrackA",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=x_pixel,
                    y_pixel=y_pixel,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

def test_canonical_validation_rejects_same_track_frame_conflict():
    tracks = [
        Track(
            track_id="track::001",
            track_name="TrackA",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                ),
                Observation(
                    production_frame=1001,
                    x_pixel=300.0,
                    y_pixel=400.0,
                ),
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

def test_canonical_validation_allows_natural_frame_gaps():
    tracks = [
        Track(
            track_id="track::001",
            track_name="TrackA",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                ),
                Observation(
                    production_frame=1002,
                    x_pixel=101.0,
                    y_pixel=201.0,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=103.0,
                    y_pixel=203.0,
                ),
            ],
        )
    ]

    validate_canonical_tracks(tracks)

    assert [
        observation.production_frame
        for observation in tracks[0].observations
    ] == [1001, 1002, 1004]

def test_canonical_validation_does_not_modify_observations():
    tracks = [
        Track(
            track_id="track::001",
            track_name="TrackA",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.25,
                    y_pixel=200.5,
                ),
                Observation(
                    production_frame=1004,
                    x_pixel=103.75,
                    y_pixel=203.25,
                ),
            ],
        )
    ]

    validate_canonical_tracks(tracks)

    assert [
        (
            observation.production_frame,
            observation.x_pixel,
            observation.y_pixel,
        )
        for observation in tracks[0].observations
    ] == [
        (1001, 100.25, 200.5),
        (1004, 103.75, 203.25),
    ]

@pytest.mark.parametrize(
    "production_frame",
    [
        1001.5,
        "1001",
        None,
        True,
    ],
)
def test_canonical_validation_rejects_non_integer_production_frame(
    production_frame,
):
    tracks = [
        Track(
            track_id="track-001",
            track_name="Track001",
            observations=[
                Observation(
                    production_frame=production_frame,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

@pytest.mark.parametrize(
    "production_frame",
    [
        0,
        -10,
    ],
)
def test_canonical_validation_allows_non_positive_integer_production_frame(
    production_frame,
):
    tracks = [
        Track(
            track_id="track-001",
            track_name="Track001",
            observations=[
                Observation(
                    production_frame=production_frame,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    validate_canonical_tracks(tracks)

def test_canonical_validation_rejects_empty_track_id():
    tracks = [
        Track(
            track_id="",
            track_name="Track001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

def test_canonical_validation_rejects_empty_track_name():
    tracks = [
        Track(
            track_id="track-001",
            track_name="",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

def test_canonical_validation_rejects_track_without_observations():
    tracks = [
        Track(
            track_id="track-001",
            track_name="Track001",
            observations=[],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

@pytest.mark.parametrize(
    "x_pixel,y_pixel",
    [
        (True, 200.0),
        (100.0, False),
    ],
)
def test_canonical_validation_rejects_boolean_coordinates(
    x_pixel,
    y_pixel,
):
    tracks = [
        Track(
            track_id="track-001",
            track_name="Track001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=x_pixel,
                    y_pixel=y_pixel,
                )
            ],
        )
    ]

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)

@pytest.mark.parametrize(
    "x_pixel,y_pixel",
    [
        (-10.5, 200.0),
        (100.0, -20.25),
    ],
)
def test_canonical_validation_allows_negative_coordinates(
    x_pixel,
    y_pixel,
):
    tracks = [
        Track(
            track_id="track-001",
            track_name="Track001",
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=x_pixel,
                    y_pixel=y_pixel,
                )
            ],
        )
    ]

    validate_canonical_tracks(tracks)

def test_canonical_validation_rejects_empty_track_collection():
    tracks = []

    with pytest.raises(ValueError):
        validate_canonical_tracks(tracks)