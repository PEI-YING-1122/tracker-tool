from tracker_tool.canonical import Track
from tracker_tool.config import ShotConfig


def write_3de_tracks(
    tracks: list[Track],
    shot_config: ShotConfig,
) -> str:
    lines: list[str] = [
        str(len(tracks)),
    ]

    for track in tracks:
        lines.append(track.track_name)
        lines.append("0")
        lines.append(str(len(track.observations)))

        for observation in track.observations:
            internal_frame = (
                observation.production_frame
                - shot_config.production_start_frame
                + 1
            )

            lines.append(
                f"{internal_frame} "
                f"{observation.x_pixel} "
                f"{observation.y_pixel}"
            )

    return "\n".join(lines) + "\n"