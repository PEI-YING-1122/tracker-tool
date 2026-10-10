import traceback
from typing import NamedTuple

from tracker_tool.contract import (
    CROSS_SOURCE_TRACK_NAME_COLLISION,
    INVALID_SHOT_METADATA,
    MISSING_REQUIRED_SHOT_METADATA,
    OBSERVATION_OUTSIDE_SHOT_RANGE,
    SAME_SOURCE_CONVERSION_NOT_ALLOWED,
    UNSUPPORTED_SOURCE_SOFTWARE,
    UNSUPPORTED_TARGET_SOFTWARE,
    formal_error_code,
)


# Presentation text for each formal error code. Which condition raises
# which code is decided by Core; this table only explains the code.
FORMAL_ERROR_EXPLANATIONS = {
    MISSING_REQUIRED_SHOT_METADATA: (
        "Required shot metadata is missing. Width, height and start frame "
        "must be provided."
    ),
    INVALID_SHOT_METADATA: (
        "Shot metadata is invalid. Width and height must be greater than "
        "zero, and the end frame must not be earlier than the start frame."
    ),
    OBSERVATION_OUTSIDE_SHOT_RANGE: (
        "The source contains observations outside the shot frame range. "
        "Check the start and end frame."
    ),
    CROSS_SOURCE_TRACK_NAME_COLLISION: (
        "The AutoTrack and UserTrack files contain the same track name. "
        "Tracks are never merged or renamed automatically."
    ),
    SAME_SOURCE_CONVERSION_NOT_ALLOWED: (
        "Source and target must be different software."
    ),
    UNSUPPORTED_SOURCE_SOFTWARE: "The source software is not supported.",
    UNSUPPORTED_TARGET_SOFTWARE: "The target software is not supported.",
}

# Form sections to highlight for each formal error code (presentation only).
FORMAL_ERROR_SECTIONS = {
    MISSING_REQUIRED_SHOT_METADATA: ("Shot",),
    INVALID_SHOT_METADATA: ("Shot",),
    OBSERVATION_OUTSIDE_SHOT_RANGE: ("Shot",),
    CROSS_SOURCE_TRACK_NAME_COLLISION: ("Source",),
    SAME_SOURCE_CONVERSION_NOT_ALLOWED: ("Source", "Target"),
    UNSUPPORTED_SOURCE_SOFTWARE: ("Source",),
    UNSUPPORTED_TARGET_SOFTWARE: ("Target",),
}

NON_CONTRACT_NOTE = "This message is not part of the Error Contract."


class FailurePresentation(NamedTuple):
    heading: str
    message: str
    details: str
    sections: tuple = ()


def describe_failure(exc: BaseException) -> FailurePresentation:
    code = formal_error_code(exc)

    if code is not None:
        return FailurePresentation(
            heading=code,
            message=FORMAL_ERROR_EXPLANATIONS[code],
            details="",
            sections=FORMAL_ERROR_SECTIONS[code],
        )

    if isinstance(exc, ValueError):
        return FailurePresentation(
            heading="Core rejected the input",
            message=f"{exc}\n\n{NON_CONTRACT_NOTE}",
            details="",
        )

    if isinstance(exc, OSError):
        return FailurePresentation(
            heading="File error",
            message=str(exc),
            details="",
        )

    return FailurePresentation(
        heading="Unexpected Core failure",
        message=(
            f"{type(exc).__name__}: {exc}\n\n"
            "Please report this as a Core issue, with the diagnostics."
        ),
        details="".join(
            traceback.format_exception(
                type(exc),
                exc,
                exc.__traceback__,
            )
        ),
    )
