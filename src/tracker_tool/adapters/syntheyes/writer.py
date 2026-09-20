from tracker_tool.canonical import Track
from tracker_tool.config import ShotConfig


def write_syntheyes_tracks(
    tracks: list[Track],
    shot_config: ShotConfig,
) -> str:
    lines: list[str] = []

    seen_track_names: set[str] = set()

    for track in tracks:
        if any(
            char.isspace()
            for char in track.track_name
        ):
            raise ValueError(
                "SynthEyes track name cannot contain whitespace"
            )

        if track.track_name in seen_track_names:
            raise ValueError(
                "SynthEyes target track names must be unique"
            )

        seen_track_names.add(track.track_name)

        for observation in track.observations:
            syntheyes_frame = (
                observation.production_frame
                - shot_config.production_start_frame
            )

            u = (
                2.0
                * observation.x_pixel
                / shot_config.image_width
                - 1.0
            )

            v = (
                1.0
                - 2.0
                * observation.y_pixel
                / shot_config.image_height
            )

            lines.append(
                f"{track.track_name} "
                f"{syntheyes_frame} "
                f"{u:.9f} "
                f"{v:.9f} "
                "15"
            )

    return "\n".join(lines) + "\n"