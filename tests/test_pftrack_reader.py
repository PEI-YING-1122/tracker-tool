import pytest
from tracker_tool.adapters.pftrack import (
    read_pftrack_source_set,
    read_pftrack_tracks,
)


def test_pftrack_reader_maps_autotrack_block_to_canonical():
    native_text = (
        '"Auto000084"\n'
        "1\n"
        "3\n"
        "1001 100.25 200.5 0.950000\n"
        "1002 101.25 201.5 0.900000\n"
        "1004 103.25 203.5 0.850000\n"
    )

    tracks = read_pftrack_tracks(
        native_text,
        source_role="AUTOTRACK",
    )

    assert len(tracks) == 1

    track = tracks[0]

    assert track.track_id == "pf_autotrack::Auto000084"
    assert track.track_name == "Auto000084"

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

def test_pftrack_reader_uses_usertrack_identity_namespace():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 0.900000\n"
    )

    tracks = read_pftrack_tracks(
        native_text,
        source_role="USERTRACK",
    )

    assert len(tracks) == 1

    track = tracks[0]

    assert track.track_id == "pf_usertrack::Track0001"
    assert track.track_name == "Track0001"

def test_pftrack_autotrack_and_usertrack_same_name_have_different_ids():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 0.900000\n"
    )

    autotrack = read_pftrack_tracks(
        native_text,
        source_role="AUTOTRACK",
    )[0]

    usertrack = read_pftrack_tracks(
        native_text,
        source_role="USERTRACK",
    )[0]

    assert autotrack.track_name == "Track0001"
    assert usertrack.track_name == "Track0001"

    assert autotrack.track_id == "pf_autotrack::Track0001"
    assert usertrack.track_id == "pf_usertrack::Track0001"

    assert autotrack.track_id != usertrack.track_id

def test_pftrack_reader_rejects_legacy_flat_row_format():
    native_text = (
        "01 1001 100.0 200.0 1.000000\n"
        "02 1002 101.0 201.0 1.000000\n"
    )

    with pytest.raises(ValueError):
        read_pftrack_tracks(
            native_text,
            source_role="AUTOTRACK",
        )

def test_pftrack_reader_rejects_missing_rows_for_declared_frame_count():
    native_text = (
        '"Auto000084"\n'
        "1\n"
        "3\n"
        "1001 100.0 200.0 1.000000\n"
        "1002 101.0 201.0 1.000000\n"
    )

    with pytest.raises(ValueError):
        read_pftrack_tracks(
            native_text,
            source_role="AUTOTRACK",
        )

@pytest.mark.parametrize(
    "x_text,y_text",
    [
        ("nan", "200.0"),
        ("inf", "200.0"),
        ("100.0", "-inf"),
    ],
)

def test_pftrack_reader_rejects_non_finite_coordinates(
    x_text,
    y_text,
):
    native_text = (
        '"Auto000084"\n'
        "1\n"
        "1\n"
        f"1001 {x_text} {y_text} 1.000000\n"
    )

    with pytest.raises(ValueError):
        read_pftrack_tracks(
            native_text,
            source_role="AUTOTRACK",
        )

def test_pftrack_reader_rejects_duplicate_frame_within_same_track():
    native_text = (
        '"Auto000084"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 1.000000\n"
        "1001 300.0 400.0 1.000000\n"
    )

    with pytest.raises(ValueError):
        read_pftrack_tracks(
            native_text,
            source_role="AUTOTRACK",
        )

def test_pftrack_source_set_aggregates_autotrack_and_usertrack():
    autotrack_text = (
        '"Auto000084"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User000001"\n'
        "1\n"
        "1\n"
        "1002 300.0 400.0 1.000000\n"
    )

    tracks = read_pftrack_source_set(
        autotrack_text=autotrack_text,
        usertrack_text=usertrack_text,
    )

    assert len(tracks) == 2

    assert tracks[0].track_id == "pf_autotrack::Auto000084"
    assert tracks[0].track_name == "Auto000084"

    assert tracks[1].track_id == "pf_usertrack::User000001"
    assert tracks[1].track_name == "User000001"

def test_pftrack_source_set_preserves_multiple_tracks_and_observations():
    autotrack_text = (
        '"Auto000001"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 0.900000\n"
        "1003 102.0 202.0 0.800000\n"
        '"Auto000002"\n'
        "1\n"
        "1\n"
        "1002 300.0 400.0 0.700000\n"
    )

    usertrack_text = (
        '"User000001"\n'
        "1\n"
        "2\n"
        "1001 500.0 600.0 0.950000\n"
        "1002 501.0 601.0 0.850000\n"
        '"User000002"\n'
        "1\n"
        "1\n"
        "1004 700.0 800.0 0.750000\n"
    )

    tracks = read_pftrack_source_set(
        autotrack_text=autotrack_text,
        usertrack_text=usertrack_text,
    )

    assert len(tracks) == 4

    assert [track.track_id for track in tracks] == [
        "pf_autotrack::Auto000001",
        "pf_autotrack::Auto000002",
        "pf_usertrack::User000001",
        "pf_usertrack::User000002",
    ]

    assert [
        observation.production_frame
        for observation in tracks[0].observations
    ] == [1001, 1003]

    assert [
        (observation.production_frame,
         observation.x_pixel,
         observation.y_pixel)
        for observation in tracks[2].observations
    ] == [
        (1001, 500.0, 600.0),
        (1002, 501.0, 601.0),
    ]

def test_pftrack_source_set_keeps_same_name_tracks_separate():
    autotrack_text = (
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    tracks = read_pftrack_source_set(
        autotrack_text=autotrack_text,
        usertrack_text=usertrack_text,
    )

    assert len(tracks) == 2

    assert tracks[0].track_id == "pf_autotrack::Track0001"
    assert tracks[1].track_id == "pf_usertrack::Track0001"

    assert tracks[0].track_name == "Track0001"
    assert tracks[1].track_name == "Track0001"

    assert tracks[0].observations[0].x_pixel == 100.0
    assert tracks[1].observations[0].x_pixel == 300.0