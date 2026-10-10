import pytest

from tracker_tool import main
from tracker_tool.adapters.pftrack import read_pftrack_source_set
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import (
    convert_pftrack_source_set,
    convert_tracks,
)


# CI-11 contract decision (2026-10-09): in a PFTrack source set, each
# explicitly specified member file must yield at least one track. A member
# with zero tracks may be a wrong file, an empty export, a parser problem or
# an export failure, so it is never silently ignored.

FORMAL_ERROR_CODES = {
    "MISSING_REQUIRED_SHOT_METADATA",
    "INVALID_SHOT_METADATA",
    "OBSERVATION_OUTSIDE_SHOT_RANGE",
    "CROSS_SOURCE_TRACK_NAME_COLLISION",
    "SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    "UNSUPPORTED_SOURCE_SOFTWARE",
    "UNSUPPORTED_TARGET_SOFTWARE",
}

AUTOTRACK_TEXT = '"Auto0001"\n1\n1\n1001 10.0 20.0 1.000000\n'
USERTRACK_TEXT = '"User0001"\n1\n1\n1002 30.0 40.0 1.000000\n'

HEADER_ONLY_EXPORT = (
    '# "Name"\n'
    "# clipNumber\n"
    "# frameCount\n"
    "# frame, xpos, ypos, similarity, zdepth\n"
)

EMPTY_MEMBERS = [
    pytest.param("", id="empty-file"),
    pytest.param(HEADER_ONLY_EXPORT, id="header-only-export"),
]


def _shot_config(target="3DE_R5"):
    return ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="PFTRACK_2017",
        target_software=target,
    )


@pytest.mark.parametrize("empty_member", EMPTY_MEMBERS)
def test_source_set_rejects_autotrack_member_without_tracks(empty_member):
    with pytest.raises(ValueError, match="AutoTrack") as caught:
        read_pftrack_source_set(
            autotrack_text=empty_member,
            usertrack_text=USERTRACK_TEXT,
        )

    assert caught.value.args[0] not in FORMAL_ERROR_CODES


@pytest.mark.parametrize("empty_member", EMPTY_MEMBERS)
def test_source_set_rejects_usertrack_member_without_tracks(empty_member):
    with pytest.raises(ValueError, match="UserTrack") as caught:
        read_pftrack_source_set(
            autotrack_text=AUTOTRACK_TEXT,
            usertrack_text=empty_member,
        )

    assert caught.value.args[0] not in FORMAL_ERROR_CODES


def test_source_set_rejects_both_members_without_tracks():
    with pytest.raises(ValueError, match="AutoTrack"):
        read_pftrack_source_set(autotrack_text="", usertrack_text="")


@pytest.mark.parametrize("target", ["3DE_R5", "SYNTHEYES_2304"])
def test_source_set_conversion_with_empty_member_writes_nothing_partial(target):
    with pytest.raises(ValueError):
        convert_pftrack_source_set("", USERTRACK_TEXT, _shot_config(target))


def test_cli_source_set_with_empty_member_creates_no_output(tmp_path):
    autotrack = tmp_path / "autotrack.txt"
    usertrack = tmp_path / "usertrack.txt"
    output = tmp_path / "output.txt"
    autotrack.write_text("", encoding="utf-8")
    usertrack.write_text(USERTRACK_TEXT, encoding="utf-8")

    with pytest.raises(ValueError, match="AutoTrack"):
        main(
            [
                "convert-pftrack-source-set",
                "--autotrack-input",
                str(autotrack),
                "--usertrack-input",
                str(usertrack),
                "--target",
                "3DE_R5",
                "--output",
                str(output),
                "--width",
                "1920",
                "--height",
                "1080",
                "--start-frame",
                "1001",
            ]
        )

    assert not output.exists()


def test_source_set_with_tracks_in_both_members_is_unchanged():
    tracks = read_pftrack_source_set(
        autotrack_text=AUTOTRACK_TEXT,
        usertrack_text=USERTRACK_TEXT,
    )

    assert [(track.track_id, track.track_name) for track in tracks] == [
        ("pf_autotrack::Auto0001", "Auto0001"),
        ("pf_usertrack::User0001", "User0001"),
    ]


def test_cross_source_collision_is_still_reported_when_both_members_have_tracks():
    with pytest.raises(ValueError, match="CROSS_SOURCE_TRACK_NAME_COLLISION"):
        read_pftrack_source_set(
            autotrack_text=AUTOTRACK_TEXT,
            usertrack_text=AUTOTRACK_TEXT,
        )


@pytest.mark.parametrize("empty_input", ["", HEADER_ONLY_EXPORT])
def test_single_file_with_zero_tracks_still_fails_as_before(empty_input):
    with pytest.raises(ValueError, match="Canonical track collection must not be empty"):
        convert_tracks(
            empty_input,
            _shot_config(),
            pftrack_source_role="AUTOTRACK",
        )
