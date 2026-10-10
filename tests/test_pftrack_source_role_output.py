from pathlib import Path

import pytest

from tracker_tool.config import ShotConfig
from tracker_tool.conversion import convert_tracks


INPUTS_DIR = Path(__file__).resolve().parents[1] / "validation" / "inputs"

NATIVE_EXPORT_TEXT = (
    '# "Name"\n'
    "# clipNumber\n"
    "# frameCount\n"
    "# frame, xpos, ypos, similarity, zdepth\n"
    "\n"
    '"Tracker0001"\n'
    "1\n"
    "2\n"
    "1001 1500.250000 1200.500000 1.000000\n"
    "1003 1510.750000 1195.125000 0.998000\n"
)

# The PFTrack source role is provenance only. It changes Canonical track_id,
# which no Writer emits, so AUTOTRACK and USERTRACK must produce identical
# target output. Native import evidence for one role therefore applies to
# the other.
PFTRACK_INPUTS = [
    pytest.param(
        (INPUTS_DIR / name).read_text(encoding="utf-8"),
        id=name,
    )
    for name in [
        "pftrack_golden_01.txt",
        "pftrack_usertrack_golden_01.txt",
        "pftrack_source_set_autotrack_golden_01.txt",
        "pftrack_source_set_usertrack_golden_01.txt",
    ]
] + [
    pytest.param(
        NATIVE_EXPORT_TEXT,
        id="native_export_layout",
    ),
]


@pytest.mark.parametrize(
    "native_text",
    PFTRACK_INPUTS,
)
@pytest.mark.parametrize(
    "target",
    [
        "3DE_R5",
        "SYNTHEYES_2304",
    ],
)
def test_pftrack_source_role_does_not_change_target_output(
    native_text,
    target,
):
    shot_config = ShotConfig(
        image_width=1920,
        image_height=1080,
        production_start_frame=1001,
        production_end_frame=None,
        source_software="PFTRACK_2017",
        target_software=target,
    )

    assert convert_tracks(
        native_text,
        shot_config,
        pftrack_source_role="AUTOTRACK",
    ) == convert_tracks(
        native_text,
        shot_config,
        pftrack_source_role="USERTRACK",
    )
