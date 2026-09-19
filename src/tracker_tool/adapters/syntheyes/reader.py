import math
from tracker_tool.canonical import Observation, Track
from tracker_tool.config import ShotConfig


def read_syntheyes_tracks(
    native_text: str,
    shot_config: ShotConfig,
) -> list[Track]:
    tracks_by_name: dict[str, Track] = {}
    seen_frames_by_name: dict[str, set[int]] = {}

    for line in native_text.splitlines():
        fields = line.split()

        if len(fields) != 5:
            raise ValueError(
                "SynthEyes row must contain exactly 5 fields"
            )

        tracker_name, frame_text, u_text, v_text, _outcome_text = fields
        try:
            outcome = int(_outcome_text)
        except ValueError as exc:
            raise ValueError(
                "SynthEyes Outcome must be an integer"
            ) from exc

        try:
            syntheyes_frame = int(frame_text)
        except ValueError as exc:
            raise ValueError(
                "SynthEyes frame must be an integer"
            ) from exc
        try:
            u = float(u_text)
            v = float(v_text)
        except ValueError as exc:
            raise ValueError(
                "SynthEyes U/V must be numeric"
            ) from exc

        if not math.isfinite(u) or not math.isfinite(v):
            raise ValueError(
                "SynthEyes U/V must be finite"
            )

        production_frame = (
            syntheyes_frame
            + shot_config.production_start_frame
        )

        x_pixel = (
            (u + 1.0)
            / 2.0
            * shot_config.image_width
        )

        y_pixel = (
            (1.0 - v)
            / 2.0
            * shot_config.image_height
        )

        if tracker_name not in tracks_by_name:
            tracks_by_name[tracker_name] = Track(
                track_id=f"syntheyes::{tracker_name}",
                track_name=tracker_name,
                observations=[],
            )

            seen_frames_by_name[tracker_name] = set()

        if production_frame in seen_frames_by_name[tracker_name]:
            raise ValueError(
                "SynthEyes track contains duplicate frame observations"
            )

        seen_frames_by_name[tracker_name].add(production_frame)

        tracks_by_name[tracker_name].observations.append(
            Observation(
                production_frame=production_frame,
                x_pixel=x_pixel,
                y_pixel=y_pixel,
            )
        )

    return list(tracks_by_name.values())