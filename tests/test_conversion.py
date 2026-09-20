import pytest
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import convert_tracks


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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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