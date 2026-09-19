import math
from .models import Track


def validate_canonical_tracks(
    tracks: list[Track],
) -> None:
    seen_track_ids: set[str] = set()

    for track in tracks:
        if not isinstance(track.track_id, str):
            raise ValueError(
                "Canonical track_id must be a string"
            )

        if track.track_id in seen_track_ids:
            raise ValueError(
                "Canonical track_id must be unique"
            )

        seen_track_ids.add(track.track_id)

        if not isinstance(track.track_name, str):
            raise ValueError(
                "Canonical track_name must be a string"
            )

        seen_frames: set[int] = set()

        for observation in track.observations:
            if observation.production_frame in seen_frames:
                raise ValueError(
                    "Canonical track contains duplicate frame observations"
                )

            seen_frames.add(observation.production_frame)
            
            if not isinstance(
                observation.x_pixel,
                (int, float),
            ) or not isinstance(
                observation.y_pixel,
                (int, float),
            ):
                raise ValueError(
                    "Canonical coordinates must be numeric"
                )

            if not math.isfinite(
                observation.x_pixel
            ) or not math.isfinite(
                observation.y_pixel
            ):
                raise ValueError(
                    "Canonical coordinates must be finite"
                )