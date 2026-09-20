import math

from .models import Track


def validate_canonical_tracks(
    tracks: list[Track],
) -> None:
    if not tracks:
        raise ValueError(
            "Canonical track collection must not be empty"
        )

    seen_track_ids: set[str] = set()

    for track in tracks:
        if not isinstance(track.track_id, str):
            raise ValueError(
                "Canonical track_id must be a string"
            )

        if track.track_id == "":
            raise ValueError(
                "Canonical track_id must not be empty"
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

        if track.track_name == "":
            raise ValueError(
                "Canonical track_name must not be empty"
            )

        if not track.observations:
            raise ValueError(
                "Canonical track must contain at least one observation"
            )

        seen_frames: set[int] = set()

        for observation in track.observations:
            if (
                not isinstance(
                    observation.production_frame,
                    int,
                )
                or isinstance(
                    observation.production_frame,
                    bool,
                )
            ):
                raise ValueError(
                    "Canonical production_frame must be an integer"
                )

            if observation.production_frame in seen_frames:
                raise ValueError(
                    "Canonical track contains duplicate frame observations"
                )

            seen_frames.add(
                observation.production_frame
            )

            if (
                not isinstance(
                    observation.x_pixel,
                    (int, float),
                )
                or isinstance(
                    observation.x_pixel,
                    bool,
                )
                or not isinstance(
                    observation.y_pixel,
                    (int, float),
                )
                or isinstance(
                    observation.y_pixel,
                    bool,
                )
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