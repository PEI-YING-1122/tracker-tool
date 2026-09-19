from tracker_tool.canonical import Track
from tracker_tool.config import ShotConfig


def write_syntheyes_tracks(
    tracks: list[Track],
    shot_config: ShotConfig,
) -> str:
    lines: list[str] = []

    for track in tracks:
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