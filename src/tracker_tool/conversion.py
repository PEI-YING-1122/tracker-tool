from tracker_tool.adapters.pftrack import (
    read_pftrack_tracks,
    write_pftrack_tracks,
)
from tracker_tool.adapters.syntheyes import (
    read_syntheyes_tracks,
    write_syntheyes_tracks,
)
from tracker_tool.adapters.threed import (
    read_3de_tracks,
    write_3de_tracks,
)
from tracker_tool.canonical import validate_canonical_tracks
from tracker_tool.config import ShotConfig


def convert_tracks(
    native_text: str,
    shot_config: ShotConfig,
    *,
    pftrack_source_role: str | None = None,
) -> str:
    required_metadata = (
        shot_config.image_width,
        shot_config.image_height,
        shot_config.production_start_frame,
    )

    if any(
        value is None
        for value in required_metadata
    ):
        raise ValueError(
            "MISSING_REQUIRED_SHOT_METADATA"
        )

    if (
        shot_config.source_software
        == shot_config.target_software
    ):
        raise ValueError(
            "Same-source conversion is not allowed"
        )

    if shot_config.source_software == "3DE_R5":
        tracks = read_3de_tracks(
            native_text,
            shot_config,
        )

    elif shot_config.source_software == "PFTRACK_2017":
        tracks = read_pftrack_tracks(
            native_text,
            source_role=pftrack_source_role,
        )

    elif shot_config.source_software == "SYNTHEYES_2304":
        tracks = read_syntheyes_tracks(
            native_text,
            shot_config,
        )

    else:
        raise ValueError(
            f"Unsupported source software: "
            f"{shot_config.source_software}"
        )

    validate_canonical_tracks(tracks)

    if shot_config.target_software == "3DE_R5":
        return write_3de_tracks(
            tracks,
            shot_config,
        )

    if shot_config.target_software == "PFTRACK_2017":
        return write_pftrack_tracks(tracks)

    if shot_config.target_software == "SYNTHEYES_2304":
        return write_syntheyes_tracks(
            tracks,
            shot_config,
        )

    raise ValueError(
        f"Unsupported target software: "
        f"{shot_config.target_software}"
    )