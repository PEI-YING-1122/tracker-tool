import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTICES = ROOT / "packaging" / "THIRD_PARTY_NOTICES.md"
LICENSES_DIR = ROOT / "packaging" / "licenses"

# Files named in the notices that are not license texts.
NOT_LICENSE_TEXTS = {"BUILD_INFO.txt", "USE_AND_LICENSE.md"}


def referenced_license_texts() -> set[str]:
    names = re.findall(r"`([\w.-]+\.(?:txt|rst|md))`", NOTICES.read_text(encoding="utf-8"))
    return set(names) - NOT_LICENSE_TEXTS


def test_every_license_text_named_in_the_notices_is_shipped():
    referenced = referenced_license_texts()

    assert referenced
    missing = sorted(name for name in referenced if not (LICENSES_DIR / name).is_file())
    assert missing == []


def test_every_shipped_license_text_is_named_in_the_notices():
    shipped = {path.name for path in LICENSES_DIR.iterdir()}

    assert sorted(shipped - referenced_license_texts()) == []
