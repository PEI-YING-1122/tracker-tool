import pytest

from tracker_tool import contract
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import (
    convert_pftrack_source_set,
    convert_tracks,
)


# The formal Error Contract as listed in docs/INTERCHANGE_MASTER.md
# ("Error Contract"). This literal list is the specification mirror; the
# rest of the code base must use tracker_tool.contract.
SPECIFIED_FORMAL_ERROR_CODES = {
    "MISSING_REQUIRED_SHOT_METADATA",
    "INVALID_SHOT_METADATA",
    "OBSERVATION_OUTSIDE_SHOT_RANGE",
    "CROSS_SOURCE_TRACK_NAME_COLLISION",
    "SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    "UNSUPPORTED_SOURCE_SOFTWARE",
    "UNSUPPORTED_TARGET_SOFTWARE",
}

THREE_DE_TEXT = "1\nA\n0\n2\n1 100.0 200.0\n3 101.0 201.0\n"
PFTRACK_TEXT = '"A"\n1\n1\n1001 100.0 200.0 1.000000\n'


def _cfg(width=1920, start=1001, end=None, source="3DE_R5", target="PFTRACK_2017"):
    return ShotConfig(width, 1080, start, end, source, target)


def test_formal_error_codes_match_the_specification():
    assert contract.FORMAL_ERROR_CODES == SPECIFIED_FORMAL_ERROR_CODES


def test_each_formal_error_code_constant_holds_its_own_name():
    for code in SPECIFIED_FORMAL_ERROR_CODES:
        assert getattr(contract, code) == code


def test_supported_software_ids_are_exactly_the_v1_ids():
    assert contract.SUPPORTED_SOFTWARE == (
        "3DE_R5",
        "PFTRACK_2017",
        "SYNTHEYES_2304",
    )
    assert contract.SOFTWARE_3DE_R5 == "3DE_R5"
    assert contract.SOFTWARE_PFTRACK_2017 == "PFTRACK_2017"
    assert contract.SOFTWARE_SYNTHEYES_2304 == "SYNTHEYES_2304"


def test_pftrack_source_roles_are_exactly_the_v1_roles():
    assert contract.PFTRACK_SOURCE_ROLES == ("AUTOTRACK", "USERTRACK")
    assert contract.PFTRACK_SOURCE_ROLE_AUTOTRACK == "AUTOTRACK"
    assert contract.PFTRACK_SOURCE_ROLE_USERTRACK == "USERTRACK"


RAISING_PATHS = [
    ("MISSING_REQUIRED_SHOT_METADATA", lambda: convert_tracks(THREE_DE_TEXT, _cfg(width=None))),
    ("INVALID_SHOT_METADATA", lambda: convert_tracks(THREE_DE_TEXT, _cfg(width=0))),
    ("OBSERVATION_OUTSIDE_SHOT_RANGE", lambda: convert_tracks(THREE_DE_TEXT, _cfg(end=1001))),
    ("SAME_SOURCE_CONVERSION_NOT_ALLOWED", lambda: convert_tracks(THREE_DE_TEXT, _cfg(target="3DE_R5"))),
    ("UNSUPPORTED_SOURCE_SOFTWARE", lambda: convert_tracks(THREE_DE_TEXT, _cfg(source="3DE"))),
    ("UNSUPPORTED_TARGET_SOFTWARE", lambda: convert_tracks(THREE_DE_TEXT, _cfg(target="PFTRACK"))),
    (
        "CROSS_SOURCE_TRACK_NAME_COLLISION",
        lambda: convert_pftrack_source_set(
            PFTRACK_TEXT,
            PFTRACK_TEXT,
            _cfg(source="PFTRACK_2017", target="3DE_R5"),
        ),
    ),
]


@pytest.mark.parametrize(("code", "raise_it"), RAISING_PATHS)
def test_formal_error_code_identifies_each_code_raised_by_core(code, raise_it):
    with pytest.raises(ValueError) as caught:
        raise_it()

    assert contract.formal_error_code(caught.value) == code


def test_every_formal_code_has_a_raising_path():
    assert {code for code, _ in RAISING_PATHS} == SPECIFIED_FORMAL_ERROR_CODES


@pytest.mark.parametrize(
    "exception",
    [
        ValueError("Canonical track collection must not be empty"),
        ValueError("INVALID_SHOT_METADATA", "extra"),
        ValueError(["INVALID_SHOT_METADATA"]),
        ValueError(),
        IndexError("INVALID_SHOT_METADATA"),
        OSError("INVALID_SHOT_METADATA"),
        RuntimeError("UNSUPPORTED_SOURCE_SOFTWARE"),
    ],
)
def test_formal_error_code_returns_none_for_non_contract_errors(exception):
    assert contract.formal_error_code(exception) is None
