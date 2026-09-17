from tracker_tool.canonical import Observation, Track


def test_track_preserves_identity_and_exact_observation_frames():
    observations = [
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
    ]

    track = Track(
        track_id="pf_autotrack::Auto000084",
        track_name="Auto000084",
        observations=observations,
    )

    assert track.track_id == "pf_autotrack::Auto000084"
    assert track.track_name == "Auto000084"

    production_frames = [
        observation.production_frame
        for observation in track.observations
    ]

    assert production_frames == [1001, 1002, 1004]
    assert 1003 not in production_frames