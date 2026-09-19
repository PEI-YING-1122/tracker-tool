import math
from tracker_tool.canonical import Observation, Track
from tracker_tool.config import ShotConfig

def _require_exact_structural_line(line: str) -> str:
    if line != line.strip():
        raise ValueError(
            "3DE native structural line has leading or trailing whitespace"
        )

    return line


def read_3de_tracks(
    native_text: str,
    shot_config: ShotConfig,
) -> list[Track]:
    lines = native_text.splitlines()

    track_count = int(
    _require_exact_structural_line(lines[0])
)
    line_index = 1

    tracks: list[Track] = []

    for native_track_index in range(1, track_count + 1):
        track_name = _require_exact_structural_line(
            lines[line_index]
        )
        line_index += 1

        static_field = _require_exact_structural_line(
            lines[line_index]
        )
        line_index += 1

        if static_field != "0":
            raise ValueError("Unexpected 3DE static field")

        sample_count = int(
            _require_exact_structural_line(
                lines[line_index]
            )
        )
        line_index += 1

        observations: list[Observation] = []
        seen_internal_frames: set[int] = set()

        for _ in range(sample_count):
            if line_index >= len(lines):
                raise ValueError(
                "3DE sample count does not match actual observation rows"
                )

            frame_text, x_text, y_text = lines[line_index].split()
            line_index += 1

            internal_frame = int(frame_text)

            if internal_frame in seen_internal_frames:
                raise ValueError(
                    "3DE track contains duplicate frame observations"
                )

            seen_internal_frames.add(internal_frame)

            x_pixel = float(x_text)
            y_pixel = float(y_text)

            if not math.isfinite(x_pixel) or not math.isfinite(y_pixel):
                raise ValueError(
                    "3DE observation coordinates must be finite"
                )

            production_frame = (
                shot_config.production_start_frame
                + internal_frame
                - 1
            )

            observations.append(
                Observation(
                    production_frame=production_frame,
                    x_pixel=x_pixel,
                    y_pixel=y_pixel,
                )
            )

        track_id = (
            f"3de::{native_track_index:06d}::{track_name}"
        )

        tracks.append(
            Track(
                track_id=track_id,
                track_name=track_name,
                observations=observations,
            )
        )

    if line_index != len(lines):
        raise ValueError(
            "Unexpected trailing 3DE native data"
        )

    return tracks