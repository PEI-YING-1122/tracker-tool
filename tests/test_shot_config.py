from tracker_tool.config import ShotConfig


def test_shot_config_preserves_explicit_runtime_metadata():
    config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=1227,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    assert config.image_width == 4096
    assert config.image_height == 2160
    assert config.production_start_frame == 1001
    assert config.production_end_frame == 1227
    assert config.source_software == "3DEqualizer R5"
    assert config.target_software == "PFTrack 2017"

def test_shot_config_allows_unknown_production_end_frame():
    config = ShotConfig(
        image_width=4096,
        image_height=2160,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="3DEqualizer R5",
        target_software="PFTrack 2017",
    )

    assert config.production_end_frame is None