from tracker_tool.adapters.pftrack import (
    read_pftrack_source_set,
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
        not isinstance(
            shot_config.image_width,
            int,
        )
        or isinstance(
            shot_config.image_width,
            bool,
       )
        or not isinstance(
            shot_config.image_height,
            int,
        )
        or isinstance(
            shot_config.image_height,
            bool,
        )
        or not isinstance(
            shot_config.production_start_frame,
            int,
        )
        or isinstance(
            shot_config.production_start_frame,
            bool,
        )
         or (
            shot_config.production_end_frame is not None
            and (
                not isinstance(
                    shot_config.production_end_frame,
                    int,
                )
                or isinstance(
                    shot_config.production_end_frame,
                    bool,
                )
            )
        )
    ):
        raise ValueError(
            "INVALID_SHOT_METADATA"
        )

    if (
        shot_config.image_width <= 0
        or shot_config.image_height <= 0
    ):
        raise ValueError(
            "INVALID_SHOT_METADATA"
        )

    if (
        shot_config.production_end_frame is not None
        and shot_config.production_end_frame
        < shot_config.production_start_frame
    ):
        raise ValueError(
            "INVALID_SHOT_METADATA"
        )

    if (
        shot_config.source_software
        == shot_config.target_software
    ):
        raise ValueError(
            "SAME_SOURCE_CONVERSION_NOT_ALLOWED"
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
            "UNSUPPORTED_SOURCE_SOFTWARE"
        )

    validate_canonical_tracks(tracks)

    for track in tracks:
        for observation in track.observations:
            if (
                observation.production_frame
                < shot_config.production_start_frame
            ):
                raise ValueError(
                    "OBSERVATION_OUTSIDE_SHOT_RANGE"
                )

            if (
                shot_config.production_end_frame is not None
                and observation.production_frame
                > shot_config.production_end_frame
            ):
                raise ValueError(
                    "OBSERVATION_OUTSIDE_SHOT_RANGE"
                )

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
        "UNSUPPORTED_TARGET_SOFTWARE"
    )

def convert_pftrack_source_set(
    autotrack_text: str,
    usertrack_text: str,
    shot_config: ShotConfig,
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
        not isinstance(
            shot_config.image_width,
            int,
        )
        or isinstance(
            shot_config.image_width,
            bool,
        )
        or not isinstance(
            shot_config.image_height,
            int,
        )
        or isinstance(
            shot_config.image_height,
            bool,
        )
        or not isinstance(
            shot_config.production_start_frame,
            int,
        )
        or isinstance(
            shot_config.production_start_frame,
            bool,
        )
        or (
            shot_config.production_end_frame is not None
            and (
                not isinstance(
                    shot_config.production_end_frame,
                    int,
                )
                or isinstance(
                    shot_config.production_end_frame,
                    bool,
                )
            )
        )
    ):
        raise ValueError(
            "INVALID_SHOT_METADATA"
        )

    if (
        shot_config.image_width <= 0
        or shot_config.image_height <= 0
    ):
        raise ValueError(
            "INVALID_SHOT_METADATA"
        )

    if (
        shot_config.production_end_frame is not None
        and shot_config.production_end_frame
        < shot_config.production_start_frame
    ):
        raise ValueError(
            "INVALID_SHOT_METADATA"
        )

    if shot_config.source_software != "PFTRACK_2017":
        raise ValueError(
            "UNSUPPORTED_SOURCE_SOFTWARE"
        )

    if (
        shot_config.source_software
        == shot_config.target_software
    ):
        raise ValueError(
            "SAME_SOURCE_CONVERSION_NOT_ALLOWED"
        )

    tracks = read_pftrack_source_set(
        autotrack_text=autotrack_text,
        usertrack_text=usertrack_text,
    )

    validate_canonical_tracks(tracks)

    for track in tracks:
        for observation in track.observations:
            if (
                observation.production_frame
                < shot_config.production_start_frame
            ):
                raise ValueError(
                    "OBSERVATION_OUTSIDE_SHOT_RANGE"
                )

            if (
                shot_config.production_end_frame is not None
                and observation.production_frame
                > shot_config.production_end_frame
            ):
                raise ValueError(
                    "OBSERVATION_OUTSIDE_SHOT_RANGE"
                )

    if shot_config.target_software == "3DE_R5":
        return write_3de_tracks(
            tracks,
            shot_config,
        )

    if shot_config.target_software == "SYNTHEYES_2304":
        return write_syntheyes_tracks(
            tracks,
            shot_config,
        )

    raise ValueError(
        "UNSUPPORTED_TARGET_SOFTWARE"
    )