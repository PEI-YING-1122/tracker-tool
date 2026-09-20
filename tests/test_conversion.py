import pytest

from tracker_tool.config import ShotConfig
from tracker_tool.conversion import (
    convert_pftrack_source_set,
    convert_tracks,
)


def test_convert_tracks_from_3de_to_pftrack():
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
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        '"Point0001"\n'
        "1\n"
        "3\n"
        "1001 100.25 200.5 1.000000\n"
        "1002 101.25 201.5 1.000000\n"
        "1004 103.25 203.5 1.000000\n"
    )

def test_convert_tracks_from_3de_to_syntheyes():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "3\n"
        "1 960.0 540.0\n"
        "2 480.0 270.0\n"
        "4 1440.0 810.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="SYNTHEYES_2304",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        "Point0001 0 0.000000000 0.000000000 15\n"
        "Point0001 1 -0.500000000 0.500000000 15\n"
        "Point0001 3 0.500000000 -0.500000000 15\n"
    )

def test_convert_tracks_from_pftrack_to_3de():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "3\n"
        "1001 100.25 200.5 1.000000\n"
        "1002 101.25 201.5 1.000000\n"
        "1004 103.25 203.5 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
        pftrack_source_role="AUTOTRACK",
    )

    assert output_text == (
        "1\n"
        "Track0001\n"
        "0\n"
        "3\n"
        "1 100.25 200.5\n"
        "2 101.25 201.5\n"
        "4 103.25 203.5\n"
    )

def test_convert_tracks_from_pftrack_to_syntheyes():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "3\n"
        "1001 960.0 540.0 1.000000\n"
        "1002 480.0 270.0 1.000000\n"
        "1004 1440.0 810.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="SYNTHEYES_2304",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
        pftrack_source_role="AUTOTRACK",
    )

    assert output_text == (
        "Track0001 0 0.000000000 0.000000000 15\n"
        "Track0001 1 -0.500000000 0.500000000 15\n"
        "Track0001 3 0.500000000 -0.500000000 15\n"
    )

def test_convert_tracks_from_syntheyes_to_3de():
    native_text = (
        "Tracker0001 0 0.000000000 0.000000000 15\n"
        "Tracker0001 1 -0.500000000 0.500000000 15\n"
        "Tracker0001 3 0.500000000 -0.500000000 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SYNTHEYES_2304",
        target_software="3DE_R5",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        "1\n"
        "Tracker0001\n"
        "0\n"
        "3\n"
        "1 960.0 540.0\n"
        "2 480.0 270.0\n"
        "4 1440.0 810.0\n"
    )

def test_convert_tracks_from_syntheyes_to_pftrack():
    native_text = (
        "Tracker0001 0 0.000000000 0.000000000 15\n"
        "Tracker0001 1 -0.500000000 0.500000000 15\n"
        "Tracker0001 3 0.500000000 -0.500000000 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SYNTHEYES_2304",
        target_software="PFTRACK_2017",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        '"Tracker0001"\n'
        "1\n"
        "3\n"
        "1001 960.0 540.0 1.000000\n"
        "1002 480.0 270.0 1.000000\n"
        "1004 1440.0 810.0 1.000000\n"
    )

def test_convert_tracks_from_syntheyes_to_3de_preserves_subpixel_coordinates():
    native_text = (
        "Tracker0001 0 -0.895572917 0.628703704 15\n"
        "Tracker0001 1 -0.638413067 0.050640146 15\n"
        "Tracker0001 3 0.587890625 -0.439120370 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SYNTHEYES_2304",
        target_software="3DE_R5",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    lines = output_text.splitlines()

    assert lines[0] == "1"
    assert lines[1] == "Tracker0001"
    assert lines[2] == "0"
    assert lines[3] == "3"

    expected = [
        (1, 100.25, 200.5),
        (2, 347.123456, 512.654321),
        (4, 1524.375, 777.125),
    ]

    for line, (expected_frame, expected_x, expected_y) in zip(
        lines[4:],
        expected,
    ):
        frame_text, x_text, y_text = line.split()

        assert int(frame_text) == expected_frame
        assert float(x_text) == pytest.approx(
            expected_x,
            abs=0.001,
        )
        assert float(y_text) == pytest.approx(
            expected_y,
            abs=0.001,
        )

def test_convert_tracks_from_syntheyes_to_pftrack_preserves_subpixel_coordinates():
    native_text = (
        "Tracker0001 0 -0.895572917 0.628703704 15\n"
        "Tracker0001 1 -0.638413067 0.050640146 15\n"
        "Tracker0001 3 0.587890625 -0.439120370 15\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SYNTHEYES_2304",
        target_software="PFTRACK_2017",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    lines = output_text.splitlines()

    assert lines[0] == '"Tracker0001"'
    assert lines[1] == "1"
    assert lines[2] == "3"

    expected = [
        (1001, 100.25, 200.5),
        (1002, 347.123456, 512.654321),
        (1004, 1524.375, 777.125),
    ]

    for line, (expected_frame, expected_x, expected_y) in zip(
        lines[3:],
        expected,
    ):
        frame_text, x_text, y_text, similarity_text = line.split()

        assert int(frame_text) == expected_frame
        assert float(x_text) == pytest.approx(
            expected_x,
            abs=0.001,
        )
        assert float(y_text) == pytest.approx(
            expected_y,
            abs=0.001,
        )
        assert similarity_text == "1.000000"

def test_convert_tracks_from_pftrack_requires_source_role():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(ValueError):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_from_pftrack_usertrack_to_3de():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 1.000000\n"
        "1003 102.0 202.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
        pftrack_source_role="USERTRACK",
    )

    assert output_text == (
        "1\n"
        "Track0001\n"
        "0\n"
        "2\n"
        "1 100.0 200.0\n"
        "3 102.0 202.0\n"
    )

def test_convert_tracks_from_pftrack_rejects_invalid_source_role():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(ValueError):
        convert_tracks(
            native_text,
            shot_config,
            pftrack_source_role="SOMETHING_ELSE",
        )

def test_convert_tracks_rejects_unknown_source_software():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="UNSUPPORTED_SOURCE_SOFTWARE",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_rejects_unknown_target_software():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK",
    )

    with pytest.raises(
        ValueError,
        match="UNSUPPORTED_TARGET_SOFTWARE",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_rejects_3de_to_3de():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )


def test_convert_tracks_rejects_pftrack_to_pftrack():
    native_text = (
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 0.750000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    ):
        convert_tracks(
            native_text,
            shot_config,
            pftrack_source_role="AUTOTRACK",
        )


def test_convert_tracks_rejects_syntheyes_to_syntheyes():
    native_text = (
        "Tracker0001 0 0.000000000 0.000000000 7\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="SYNTHEYES_2304",
        target_software="SYNTHEYES_2304",
    )

    with pytest.raises(
        ValueError,
        match="SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_rejects_missing_image_width():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=None,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="MISSING_REQUIRED_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )


def test_convert_tracks_rejects_missing_image_height():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=None,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="MISSING_REQUIRED_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )


def test_convert_tracks_rejects_missing_production_start_frame():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=None,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="MISSING_REQUIRED_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_allows_missing_production_end_frame():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        '"Point0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

def test_convert_tracks_checks_required_metadata_before_native_parsing():
    native_text = "THIS IS NOT VALID 3DE DATA"

    shot_config = ShotConfig(
        image_width=None,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="MISSING_REQUIRED_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_checks_start_frame_before_native_parsing():
    native_text = "THIS IS NOT VALID 3DE DATA"

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=None,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="MISSING_REQUIRED_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_pftrack_source_set_to_3de():
    autotrack_text = (
        '"Auto0001"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 1.000000\n"
        "1003 102.0 202.0 1.000000\n"
    )

    usertrack_text = (
        '"User0001"\n'
        "1\n"
        "2\n"
        "1002 300.0 400.0 1.000000\n"
        "1004 302.0 402.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    output_text = convert_pftrack_source_set(
        autotrack_text,
        usertrack_text,
        shot_config,
    )

    assert output_text == (
        "2\n"
        "Auto0001\n"
        "0\n"
        "2\n"
        "1 100.0 200.0\n"
        "3 102.0 202.0\n"
        "User0001\n"
        "0\n"
        "2\n"
        "2 300.0 400.0\n"
        "4 302.0 402.0\n"
    )

def test_convert_pftrack_source_set_to_syntheyes():
    autotrack_text = (
        '"Auto0001"\n'
        "1\n"
        "2\n"
        "1001 960.0 540.0 1.000000\n"
        "1003 1440.0 810.0 1.000000\n"
    )

    usertrack_text = (
        '"User0001"\n'
        "1\n"
        "2\n"
        "1002 480.0 270.0 1.000000\n"
        "1004 240.0 135.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="SYNTHEYES_2304",
    )

    output_text = convert_pftrack_source_set(
        autotrack_text,
        usertrack_text,
        shot_config,
    )

    assert output_text == (
        "Auto0001 0 0.000000000 0.000000000 15\n"
        "Auto0001 2 0.500000000 -0.500000000 15\n"
        "User0001 1 -0.500000000 0.500000000 15\n"
        "User0001 3 -0.750000000 0.750000000 15\n"
    )

def test_convert_pftrack_source_set_rejects_cross_source_name_collision():
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
        "1002 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="CROSS_SOURCE_TRACK_NAME_COLLISION",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

def test_convert_pftrack_source_set_rejects_same_source_conversion():
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="PFTRACK_2017",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

def test_convert_pftrack_source_set_rejects_unsupported_source_software():
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="PFTRACK",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="UNSUPPORTED_SOURCE_SOFTWARE",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

def test_convert_pftrack_source_set_rejects_unsupported_target_software():
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="PFTRACK_2017",
        target_software="UNKNOWN_TARGET",
    )

    with pytest.raises(
        ValueError,
        match="UNSUPPORTED_TARGET_SOFTWARE",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

def test_convert_pftrack_source_set_checks_metadata_before_native_parsing():
    autotrack_text = "THIS IS NOT VALID PFTRACK DATA"
    usertrack_text = "THIS IS ALSO NOT VALID PFTRACK DATA"

    shot_config = ShotConfig(
        image_width=None,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="MISSING_REQUIRED_SHOT_METADATA",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

def test_convert_tracks_rejects_non_positive_image_width():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=0,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_rejects_non_positive_image_height():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=-1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_allows_zero_production_start_frame():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=0,
        production_end_frame=None,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        '"Point0001"\n'
        "1\n"
        "1\n"
        "0 100.0 200.0 1.000000\n"
    )

def test_convert_tracks_allows_negative_production_start_frame():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=-10,
        production_end_frame=None,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        '"Point0001"\n'
        "1\n"
        "1\n"
        "-10 100.0 200.0 1.000000\n"
    )

def test_convert_tracks_rejects_end_frame_before_start_frame():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1000,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

def test_convert_tracks_allows_end_frame_equal_to_start_frame():
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1001,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
    )

    assert output_text == (
        '"Point0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

def test_convert_pftrack_source_set_rejects_end_frame_before_start_frame():
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1000,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

@pytest.mark.parametrize(
    "image_width,image_height",
    [
        ("1920", 1080),
        (1920.0, 1080),
        (True, 1080),
        (1920, "1080"),
        (1920, 1080.0),
        (1920, False),
    ],
)
def test_convert_tracks_rejects_invalid_dimension_types(
    image_width,
    image_height,
):
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=image_width,
        image_height=image_height,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

@pytest.mark.parametrize(
    "production_start_frame,production_end_frame",
    [
        ("1001", None),
        (1001.0, None),
        (True, None),
        (1001, "1100"),
        (1001, 1100.0),
        (1001, False),
    ],
)
def test_convert_tracks_rejects_invalid_frame_metadata_types(
    production_start_frame,
    production_end_frame,
):
    native_text = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=production_start_frame,
        production_end_frame=production_end_frame,
        source_software="3DE_R5",
        target_software="PFTRACK_2017",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_tracks(
            native_text,
            shot_config,
        )

@pytest.mark.parametrize(
    "image_width,image_height",
    [
        ("1920", 1080),
        (1920, False),
    ],
)
def test_convert_pftrack_source_set_rejects_invalid_dimension_types(
    image_width,
    image_height,
):
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=image_width,
        image_height=image_height,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

@pytest.mark.parametrize(
    "production_start_frame,production_end_frame",
    [
        ("1001", None),
        (1001, True),
    ],
)
def test_convert_pftrack_source_set_rejects_invalid_frame_metadata_types(
    production_start_frame,
    production_end_frame,
):
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=production_start_frame,
        production_end_frame=production_end_frame,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

def test_convert_tracks_rejects_observation_before_start_frame():
    native_text = (
        '"Point0001"\n'
        "1\n"
        "1\n"
        "1000 100.0 200.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="OBSERVATION_OUTSIDE_SHOT_RANGE",
    ):
        convert_tracks(
            native_text,
            shot_config,
            pftrack_source_role="AUTOTRACK",
        )

def test_convert_tracks_rejects_observation_after_end_frame():
    native_text = (
        '"Point0001"\n'
        "1\n"
        "1\n"
        "1101 100.0 200.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="OBSERVATION_OUTSIDE_SHOT_RANGE",
    ):
        convert_tracks(
            native_text,
            shot_config,
            pftrack_source_role="AUTOTRACK",
        )

@pytest.mark.parametrize(
    "production_frame",
    [
        1001,
        1100,
    ],
)
def test_convert_tracks_allows_observation_on_shot_range_boundary(
    production_frame,
):
    native_text = (
        '"Point0001"\n'
        "1\n"
        "1\n"
        f"{production_frame} 100.0 200.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    convert_tracks(
        native_text,
        shot_config,
        pftrack_source_role="AUTOTRACK",
    )

def test_convert_pftrack_source_set_rejects_observation_before_start_frame():
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1000 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="OBSERVATION_OUTSIDE_SHOT_RANGE",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )

def test_convert_pftrack_source_set_rejects_observation_after_end_frame():
    autotrack_text = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    usertrack_text = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1101 300.0 400.0 1.000000\n"
    )

    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=1100,
        source_software="PFTRACK_2017",
        target_software="3DE_R5",
    )

    with pytest.raises(
        ValueError,
        match="OBSERVATION_OUTSIDE_SHOT_RANGE",
    ):
        convert_pftrack_source_set(
            autotrack_text,
            usertrack_text,
            shot_config,
        )
