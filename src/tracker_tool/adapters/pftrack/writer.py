from tracker_tool.canonical import Track


def write_pftrack_tracks(
    tracks: list[Track],
) -> str:
    lines: list[str] = []

    for track in tracks:
        lines.append(f'"{track.track_name}"')
        lines.append("1")
        lines.append(str(len(track.observations)))

        for observation in track.observations:
            lines.append(
                f"{observation.production_frame} "
                f"{observation.x_pixel} "
                f"{observation.y_pixel} "
                "1.000000"
            )

    return "\n".join(lines) + "\n"