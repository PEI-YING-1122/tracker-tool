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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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