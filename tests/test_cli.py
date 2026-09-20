import pytest

from tracker_tool import main


def test_cli_converts_3de_file_to_pftrack(tmp_path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "2\n"
        "1 100.0 200.0\n"
        "3 102.0 202.0\n",
        encoding="utf-8",
    )

    result = main(
        [
            "convert",
            "--source",
            "3DE_R5",
            "--target",
            "PFTRACK_2017",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--width",
            "1920",
            "--height",
            "1080",
            "--start-frame",
            "1001",
        ]
    )

    assert result == 0

    assert output_path.read_text(
        encoding="utf-8",
    ) == (
        '"Point0001"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 1.000000\n"
        "1003 102.0 202.0 1.000000\n"
    )

def test_cli_converts_pftrack_autotrack_file_to_3de(tmp_path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        '"Track0001"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 1.000000\n"
        "1003 102.0 202.0 1.000000\n",
        encoding="utf-8",
    )

    result = main(
        [
            "convert",
            "--source",
            "PFTRACK_2017",
            "--target",
            "3DE_R5",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--width",
            "1920",
            "--height",
            "1080",
            "--start-frame",
            "1001",
            "--pftrack-source-role",
            "AUTOTRACK",
        ]
    )

    assert result == 0

    assert output_path.read_text(
        encoding="utf-8",
    ) == (
        "1\n"
        "Track0001\n"
        "0\n"
        "2\n"
        "1 100.0 200.0\n"
        "3 102.0 202.0\n"
    )

def test_cli_rejects_pftrack_source_without_role(tmp_path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        main(
            [
                "convert",
                "--source",
                "PFTRACK_2017",
                "--target",
                "3DE_R5",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_rejects_same_source_conversion_without_writing_output(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    ):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "3DE_R5",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_rejects_missing_required_argument(tmp_path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "PFTRACK_2017",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                # 故意沒有 --start-frame
            ]
        )

    assert not output_path.exists()

def test_cli_rejects_source_software_alias_without_writing_output(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="UNSUPPORTED_SOURCE_SOFTWARE",
    ):
        main(
            [
                "convert",
                "--source",
                "3DE",
                "--target",
                "PFTRACK_2017",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_rejects_target_software_alias_without_writing_output(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="UNSUPPORTED_TARGET_SOFTWARE",
    ):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "PFTRACK",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_rejects_lowercase_pftrack_source_role(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        main(
            [
                "convert",
                "--source",
                "PFTRACK_2017",
                "--target",
                "3DE_R5",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
                "--pftrack-source-role",
                "autotrack",
            ]
        )

    assert not output_path.exists()

def test_cli_allows_missing_end_frame(tmp_path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    result = main(
        [
            "convert",
            "--source",
            "3DE_R5",
            "--target",
            "PFTRACK_2017",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--width",
            "1920",
            "--height",
            "1080",
            "--start-frame",
            "1001",
            # 故意不提供 --end-frame
        ]
    )

    assert result == 0

    assert output_path.read_text(
        encoding="utf-8",
    ) == (
        '"Point0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

def test_cli_converts_pftrack_source_set_to_3de(tmp_path):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto0001"\n'
        "1\n"
        "2\n"
        "1001 100.0 200.0 1.000000\n"
        "1003 102.0 202.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User0001"\n'
        "1\n"
        "2\n"
        "1002 300.0 400.0 1.000000\n"
        "1004 302.0 402.0 1.000000\n",
        encoding="utf-8",
    )

    result = main(
        [
            "convert-pftrack-source-set",
            "--autotrack-input",
            str(autotrack_path),
            "--usertrack-input",
            str(usertrack_path),
            "--target",
            "3DE_R5",
            "--output",
            str(output_path),
            "--width",
            "1920",
            "--height",
            "1080",
            "--start-frame",
            "1001",
        ]
    )

    assert result == 0

    assert output_path.read_text(
        encoding="utf-8",
    ) == (
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

def test_cli_converts_pftrack_source_set_to_syntheyes(tmp_path):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto0001"\n'
        "1\n"
        "2\n"
        "1001 960.0 540.0 1.000000\n"
        "1003 1440.0 810.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User0001"\n'
        "1\n"
        "2\n"
        "1002 480.0 270.0 1.000000\n"
        "1004 240.0 135.0 1.000000\n",
        encoding="utf-8",
    )

    result = main(
        [
            "convert-pftrack-source-set",
            "--autotrack-input",
            str(autotrack_path),
            "--usertrack-input",
            str(usertrack_path),
            "--target",
            "SYNTHEYES_2304",
            "--output",
            str(output_path),
            "--width",
            "1920",
            "--height",
            "1080",
            "--start-frame",
            "1001",
        ]
    )

    assert result == 0

    assert output_path.read_text(
        encoding="utf-8",
    ) == (
        "Auto0001 0 0.000000000 0.000000000 15\n"
        "Auto0001 2 0.500000000 -0.500000000 15\n"
        "User0001 1 -0.500000000 0.500000000 15\n"
        "User0001 3 -0.750000000 0.750000000 15\n"
    )

def test_cli_pftrack_source_set_rejects_cross_source_name_collision(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"Track0001"\n'
        "1\n"
        "1\n"
        "1002 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="CROSS_SOURCE_TRACK_NAME_COLLISION",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_pftrack_source_set_rejects_pftrack_target(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User0001"\n'
        "1\n"
        "1\n"
        "1002 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "PFTRACK_2017",
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_pftrack_source_set_rejects_unsupported_target_without_writing_output(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="UNSUPPORTED_TARGET_SOFTWARE",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "UNKNOWN_TARGET",
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_pftrack_source_set_rejects_missing_required_metadata(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User0001"\n'
        "1\n"
        "1\n"
        "1002 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(output_path),
                "--height",
                "1080",
                "--start-frame",
                "1001",
                # 故意缺 --width
            ]
        )

    assert not output_path.exists()

def test_cli_pftrack_source_set_allows_missing_end_frame(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto0001"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User0001"\n'
        "1\n"
        "1\n"
        "1002 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    result = main(
        [
            "convert-pftrack-source-set",
            "--autotrack-input",
            str(autotrack_path),
            "--usertrack-input",
            str(usertrack_path),
            "--target",
            "3DE_R5",
            "--output",
            str(output_path),
            "--width",
            "1920",
            "--height",
            "1080",
            "--start-frame",
            "1001",
            # 故意不提供 --end-frame
        ]
    )

    assert result == 0

    assert output_path.read_text(
        encoding="utf-8",
    ) == (
        "2\n"
        "Auto0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
        "User0001\n"
        "0\n"
        "1\n"
        "2 300.0 400.0\n"
    )

def test_cli_rejects_zero_width_without_writing_output(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "PFTRACK_2017",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "0",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_rejects_end_frame_before_start_without_writing_output(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "PFTRACK_2017",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
                "--end-frame",
                "1000",
            ]
        )

    assert not output_path.exists()

def test_cli_rejects_observation_outside_shot_range_without_writing_output(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        '"Point0001"\n'
        "1\n"
        "1\n"
        "1101 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="OBSERVATION_OUTSIDE_SHOT_RANGE",
    ):
        main(
            [
                "convert",
                "--source",
                "PFTRACK_2017",
                "--target",
                "3DE_R5",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
                "--end-frame",
                "1100",
                "--pftrack-source-role",
                "AUTOTRACK",
            ]
        )

    assert not output_path.exists()

def test_cli_failure_preserves_existing_output_file(
    tmp_path,
):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text(
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n",
        encoding="utf-8",
    )

    original_output = "EXISTING_VALID_OUTPUT\n"

    output_path.write_text(
        original_output,
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "PFTRACK_2017",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--width",
                "0",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert output_path.exists()

    assert output_path.read_text(
        encoding="utf-8",
    ) == original_output

def test_cli_rejects_same_input_and_output_path(
    tmp_path,
):
    input_path = tmp_path / "tracks.txt"

    original_input = (
        "1\n"
        "Point0001\n"
        "0\n"
        "1\n"
        "1 100.0 200.0\n"
    )

    input_path.write_text(
        original_input,
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Input and output paths must be different",
    ):
        main(
            [
                "convert",
                "--source",
                "3DE_R5",
                "--target",
                "PFTRACK_2017",
                "--input",
                str(input_path),
                "--output",
                str(input_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert input_path.read_text(
        encoding="utf-8",
    ) == original_input

def test_cli_pftrack_source_set_rejects_observation_outside_shot_range_without_writing_output(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User_A"\n'
        "1\n"
        "1\n"
        "1101 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="OBSERVATION_OUTSIDE_SHOT_RANGE",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
                "--end-frame",
                "1100",
            ]
        )

    assert not output_path.exists()

def test_cli_pftrack_source_set_failure_preserves_existing_output_file(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    original_output = "EXISTING_VALID_OUTPUT\n"

    output_path.write_text(
        original_output,
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(output_path),
                "--width",
                "0",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert output_path.exists()

    assert output_path.read_text(
        encoding="utf-8",
    ) == original_output

def test_cli_pftrack_source_set_rejects_autotrack_as_output_path(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"

    original_autotrack = (
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )

    autotrack_path.write_text(
        original_autotrack,
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Input and output paths must be different",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(autotrack_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert autotrack_path.read_text(
        encoding="utf-8",
    ) == original_autotrack

def test_cli_pftrack_source_set_rejects_usertrack_as_output_path(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"

    autotrack_path.write_text(
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    original_usertrack = (
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n"
    )

    usertrack_path.write_text(
        original_usertrack,
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Input and output paths must be different",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(usertrack_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert usertrack_path.read_text(
        encoding="utf-8",
    ) == original_usertrack

def test_cli_pftrack_source_set_rejects_zero_width_without_writing_output(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(output_path),
                "--width",
                "0",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output_path.exists()

def test_cli_pftrack_source_set_rejects_end_before_start_without_writing_output(
    tmp_path,
):
    autotrack_path = tmp_path / "autotrack.txt"
    usertrack_path = tmp_path / "usertrack.txt"
    output_path = tmp_path / "output.txt"

    autotrack_path.write_text(
        '"Auto_A"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n",
        encoding="utf-8",
    )

    usertrack_path.write_text(
        '"User_A"\n'
        "1\n"
        "1\n"
        "1001 300.0 400.0 1.000000\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="INVALID_SHOT_METADATA",
    ):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack_path),
                "--usertrack-input",
                str(usertrack_path),
                "--target",
                "3DE_R5",
                "--output",
                str(output_path),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
                "--end-frame",
                "1000",
            ]
        )

    assert not output_path.exists()