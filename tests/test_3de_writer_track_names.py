import pytest

from tracker_tool import main
from tracker_tool.adapters.threed import (
    read_3de_tracks,
    write_3de_tracks,
)
from tracker_tool.canonical import Observation, Track
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import (
    convert_pftrack_source_set,
    convert_tracks,
)


def _shot_config(source="Canonical", target="3DE_R5"):
    return ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software=source,
        target_software=target,
    )


def _single_track(track_name):
    return [
        Track(
            track_id="source::001",
            track_name=track_name,
            observations=[
                Observation(
                    production_frame=1001,
                    x_pixel=100.0,
                    y_pixel=200.0,
                )
            ],
        )
    ]


def _pftrack_block(track_name):
    return (
        f'"{track_name}"\n'
        "1\n"
        "1\n"
        "1001 100.0 200.0 1.000000\n"
    )


NAMES_NOT_REPRESENTABLE_IN_3DE = [
    " Point0001",
    "Point0001 ",
    "\tPoint0001",
    "Point0001\t",
    "  ",
]


@pytest.mark.parametrize(
    "track_name",
    NAMES_NOT_REPRESENTABLE_IN_3DE,
)
def test_3de_writer_rejects_track_name_with_leading_or_trailing_whitespace(
    track_name,
):
    with pytest.raises(ValueError):
        write_3de_tracks(
            _single_track(track_name),
            _shot_config(),
        )


@pytest.mark.parametrize(
    "track_name",
    [
        "Point0001",
        "01",
        "Point 001",
        "Auto000084",
    ],
)
def test_3de_writer_output_round_trips_track_name_exactly(track_name):
    native_text = write_3de_tracks(
        _single_track(track_name),
        _shot_config(),
    )

    tracks = read_3de_tracks(
        native_text,
        _shot_config(source="3DE_R5", target="PFTRACK_2017"),
    )

    assert [track.track_name for track in tracks] == [track_name]


@pytest.mark.parametrize(
    "track_name",
    NAMES_NOT_REPRESENTABLE_IN_3DE,
)
@pytest.mark.parametrize(
    "source_role",
    [
        "AUTOTRACK",
        "USERTRACK",
    ],
)
def test_pftrack_to_3de_rejects_name_not_representable_in_3de(
    track_name,
    source_role,
):
    with pytest.raises(ValueError):
        convert_tracks(
            _pftrack_block(track_name),
            _shot_config(source="PFTRACK_2017", target="3DE_R5"),
            pftrack_source_role=source_role,
        )


def test_pftrack_source_set_to_3de_rejects_name_not_representable_in_3de():
    with pytest.raises(ValueError):
        convert_pftrack_source_set(
            _pftrack_block("Auto000084"),
            _pftrack_block(" Track0001"),
            _shot_config(source="PFTRACK_2017", target="3DE_R5"),
        )


def test_cli_pftrack_to_3de_name_not_representable_writes_no_output(
    tmp_path,
):
    input_path = tmp_path / "pftrack.txt"
    output_path = tmp_path / "output_3de.txt"

    input_path.write_text(
        _pftrack_block("Point0001 "),
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
                "USERTRACK",
            ]
        )

    assert not output_path.exists()
