import math
from tracker_tool.canonical import Observation, Track


# Header variants verified in real PFTrack 2017 exports. They differ only
# in the column description line; observation rows have 4 values in both.
VERIFIED_PFTRACK_HEADERS = (
    (
        '# "Name"',
        "# clipNumber",
        "# frameCount",
        "# frame, xpos, ypos, similarity, zdepth",
    ),
    (
        '# "Name"',
        "# clipNumber",
        "# frameCount",
        "# frame, xpos, ypos, similarity",
    ),
)


def _require_line(
    lines: list[str],
    line_index: int,
    description: str,
) -> str:
    if line_index >= len(lines):
        raise ValueError(
            f"PFTrack native data ended before {description}"
        )

    return lines[line_index]


def _require_block_line(
    lines: list[str],
    line_index: int,
    description: str,
) -> str:
    line = _require_line(lines, line_index, description)

    if line == "":
        raise ValueError(
            "Unexpected blank line inside PFTrack track block"
        )

    return line


def _reject_misplaced_header(line: str) -> None:
    if line.startswith("#"):
        raise ValueError(
            "PFTrack header is only allowed at the start of the file"
        )


def _read_native_header(lines: list[str]) -> bool:
    if not lines or not lines[0].startswith("#"):
        return False

    if tuple(lines[:4]) not in VERIFIED_PFTRACK_HEADERS:
        raise ValueError("Unknown PFTrack header")

    return True


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

    # Two verified layouts:
    # - headerless blocks with no blank lines (v1.0.0 input and writer output)
    # - PFTrack 2017 export: verified header, then exactly one blank
    #   separator line before every track block
    has_native_header = _read_native_header(lines)

    line_index = 4 if has_native_header else 0
    tracks: list[Track] = []

    while line_index < len(lines):
        _reject_misplaced_header(lines[line_index])

        if has_native_header:
            if lines[line_index] != "":
                raise ValueError(
                    "PFTrack track block must be preceded by one blank separator line"
                )

            line_index += 1

        track_name_line = _require_line(lines, line_index, "track name")
        line_index += 1

        _reject_misplaced_header(track_name_line)

        if track_name_line == "":
            raise ValueError(
                "Unexpected blank line in PFTrack native data"
            )

        if not (
            track_name_line.startswith('"')
            and track_name_line.endswith('"')
        ):
            raise ValueError("Invalid PFTrack track name")

        track_name = track_name_line[1:-1]

        clip_number = int(
            _require_block_line(lines, line_index, "clipNumber")
        )
        line_index += 1

        if clip_number != 1:
            raise ValueError("Unexpected PFTrack clip number")

        frame_count = int(
            _require_block_line(lines, line_index, "frameCount")
        )
        line_index += 1

        observations: list[Observation] = []
        seen_frames: set[int] = set()

        for _ in range(frame_count):
            if line_index >= len(lines):
                raise ValueError(
                    "PFTrack frame count does not match actual observation rows"
                )
        
            frame_text, x_text, y_text, _similarity_text = (
                _require_block_line(
                    lines,
                    line_index,
                    "observation row",
                ).split()
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
    autotrack_tracks = read_pftrack_tracks(
        autotrack_text,
        source_role="AUTOTRACK",
    )

    usertrack_tracks = read_pftrack_tracks(
        usertrack_text,
        source_role="USERTRACK",
    )

    autotrack_names = {
        track.track_name
        for track in autotrack_tracks
    }

    usertrack_names = {
        track.track_name
        for track in usertrack_tracks
    }

    if autotrack_names & usertrack_names:
        raise ValueError(
            "CROSS_SOURCE_TRACK_NAME_COLLISION"
        )

    return autotrack_tracks + usertrack_tracks