"""Tracker Tool v1 contract identifiers.

Single source for the formal error codes (docs/INTERCHANGE_MASTER.md,
"Error Contract"), the supported software IDs, and the PFTrack source
roles. Core, CLI and GUI import these names instead of repeating the
strings.
"""

SOFTWARE_3DE_R5 = "3DE_R5"
SOFTWARE_PFTRACK_2017 = "PFTRACK_2017"
SOFTWARE_SYNTHEYES_2304 = "SYNTHEYES_2304"

SUPPORTED_SOFTWARE = (
    SOFTWARE_3DE_R5,
    SOFTWARE_PFTRACK_2017,
    SOFTWARE_SYNTHEYES_2304,
)

PFTRACK_SOURCE_ROLE_AUTOTRACK = "AUTOTRACK"
PFTRACK_SOURCE_ROLE_USERTRACK = "USERTRACK"

PFTRACK_SOURCE_ROLES = (
    PFTRACK_SOURCE_ROLE_AUTOTRACK,
    PFTRACK_SOURCE_ROLE_USERTRACK,
)

MISSING_REQUIRED_SHOT_METADATA = "MISSING_REQUIRED_SHOT_METADATA"
INVALID_SHOT_METADATA = "INVALID_SHOT_METADATA"
OBSERVATION_OUTSIDE_SHOT_RANGE = "OBSERVATION_OUTSIDE_SHOT_RANGE"
CROSS_SOURCE_TRACK_NAME_COLLISION = "CROSS_SOURCE_TRACK_NAME_COLLISION"
SAME_SOURCE_CONVERSION_NOT_ALLOWED = "SAME_SOURCE_CONVERSION_NOT_ALLOWED"
UNSUPPORTED_SOURCE_SOFTWARE = "UNSUPPORTED_SOURCE_SOFTWARE"
UNSUPPORTED_TARGET_SOFTWARE = "UNSUPPORTED_TARGET_SOFTWARE"

FORMAL_ERROR_CODES = frozenset(
    {
        MISSING_REQUIRED_SHOT_METADATA,
        INVALID_SHOT_METADATA,
        OBSERVATION_OUTSIDE_SHOT_RANGE,
        CROSS_SOURCE_TRACK_NAME_COLLISION,
        SAME_SOURCE_CONVERSION_NOT_ALLOWED,
        UNSUPPORTED_SOURCE_SOFTWARE,
        UNSUPPORTED_TARGET_SOFTWARE,
    }
)


def formal_error_code(exc: BaseException) -> str | None:
    """Return the formal error code carried by exc, or None.

    Core raises a formal error as ValueError(<code>). Any other exception,
    including a ValueError with a descriptive message, is not part of the
    Error Contract.
    """

    if not isinstance(exc, ValueError) or len(exc.args) != 1:
        return None

    code = exc.args[0]

    if isinstance(code, str) and code in FORMAL_ERROR_CODES:
        return code

    return None
