import math
from tracker_tool.canonical import Observation, Track


def read_pftrack_tracks(
    native_text: str,
    source_role: str,
) -> list[Track]:
    lines = native_text.splitlines()

    if source_role == "AUTOTRACK":
        track_id_prefix = "pf_autotrack"
    elif source_role == "USERTRACK":
        track_id_prefix = "pf_usertrack"
    else:
        raise ValueError("Unsupported PFTrack source role")

    line_index = 0
    tracks: list[Track] = []

    while line_index < len(lines):
        track_name_line = lines[line_index]
        line_index += 1

        if not (
            track_name_line.startswith('"')
            and track_name_line.endswith('"')
        ):
            raise ValueError("Invalid PFTrack track name")

        track_name = track_name_line[1:-1]

        clip_number = int(lines[line_index])
        line_index += 1

        if clip_number != 1:
            raise ValueError("Unexpected PFTrack clip number")

        frame_count = int(lines[line_index])
        line_index += 1

        observations: list[Observation] = []
        seen_frames: set[int] = set()

        for _ in range(frame_count):
            if line_index >= len(lines):
                raise ValueError(
                    "PFTrack frame count does not match actual observation rows"
                )
        
            frame_text, x_text, y_text, _similarity_text = (
                lines[line_index].split()
            )
            line_index += 1

            production_frame = int(frame_text)
            if production_frame in seen_frames:
                raise ValueError(
                    "PFTrack track contains duplicate frame observations"
                )

            seen_frames.add(production_frame)

            x_pixel = float(x_text)
            y_pixel = float(y_text)

            if not math.isfinite(x_pixel) or not math.isfinite(y_pixel):
                raise ValueError(
                    "PFTrack observation coordinates must be finite"
                )

            observations.append(
                Observation(
                    production_frame=production_frame,
                    x_pixel=x_pixel,
                    y_pixel=y_pixel,
                )
            )

        tracks.append(
            Track(
                track_id=f"{track_id_prefix}::{track_name}",
                track_name=track_name,
                observations=observations,
            )
        )

    return tracks

def read_pftrack_source_set(
    autotrack_text: str,
    usertrack_text: str,
) -> list[Track]:
    autotracks = read_pftrack_tracks(
        autotrack_text,
        source_role="AUTOTRACK",
    )

    usertracks = read_pftrack_tracks(
        usertrack_text,
        source_role="USERTRACK",
    )

    return autotracks + usertracks