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
        # The name is a 3DE structural line, which must not have leading or
        # trailing whitespace. The name cannot be trimmed without changing it.
        if track.track_name != track.track_name.strip():
            raise ValueError(
                "3DE track name cannot have leading or trailing whitespace"
            )

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