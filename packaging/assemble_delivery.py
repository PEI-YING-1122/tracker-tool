"""Assemble the internal delivery package around a built GUI bundle.

Usage (from the repository root):

    uv run python packaging/assemble_delivery.py \\
        --bundle <dist>/TrackerTool --tag v1.1.0 --out <delivery dir>

Layout of <delivery dir>:

    TrackerTool/            the bundle, copied unchanged
    LICENSE_SUPPLEMENT/     LICENSE_SUPPLEMENT.md, Qt third-party attributions
    LGPL_SOURCES/           Qt / PySide6 source archives, Tracker Tool source,
                            SHA256SUMS.txt
    DELIVERY_MANIFEST.txt   SHA-256 of every file in the package

The Qt archives are checked against the md5sums.txt published by Qt. The
bundle must have been built from --tag (checked through BUILD_INFO.txt).
"""

import argparse
import hashlib
import shutil
import subprocess
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QT_VERSION = "6.11.2"
QT_SUBMODULES_URL = f"https://download.qt.io/official_releases/qt/6.11/{QT_VERSION}/submodules"
QT_ARCHIVES = tuple(
    f"{module}-everywhere-src-{QT_VERSION}.tar.xz"
    for module in ("qtbase", "qtsvg", "qtimageformats", "qttranslations")
)
PYSIDE_URL = (
    "https://download.qt.io/official_releases/QtForPython/pyside6/"
    f"PySide6-{QT_VERSION}-src/pyside-setup-everywhere-src-{QT_VERSION}.tar.xz"
)
SUPPLEMENT_FILES = (
    ROOT / "packaging" / "delivery" / "LICENSE_SUPPLEMENT.md",
    ROOT / "packaging" / "licenses" / f"Qt-{QT_VERSION}-third-party-attributions.txt",
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--downloads",
        type=Path,
        help="directory with already downloaded archives (reused if present)",
    )
    args = parser.parse_args(argv)

    check_bundle_commit(args.bundle, args.tag)
    if args.out.exists():
        raise SystemExit(f"{args.out} already exists")

    shutil.copytree(args.bundle, args.out / "TrackerTool")

    supplement = args.out / "LICENSE_SUPPLEMENT"
    supplement.mkdir()
    for source in SUPPLEMENT_FILES:
        shutil.copy2(source, supplement / source.name)

    sources = args.out / "LGPL_SOURCES"
    sources.mkdir()
    downloads = args.downloads or sources
    md5sums = parse_md5sums(fetch(f"{QT_SUBMODULES_URL}/md5sums.txt", downloads))
    for name in QT_ARCHIVES:
        archive = fetch(f"{QT_SUBMODULES_URL}/{name}", downloads)
        if _digest(archive, "md5") != md5sums[name]:
            raise SystemExit(f"{name} does not match Qt's md5sums.txt")
        _place(archive, sources)
    _place(fetch(PYSIDE_URL, downloads), sources)
    git_archive(args.tag, sources / f"tracker-tool-{args.tag}-src.zip")
    write_sums(sources, sources / "SHA256SUMS.txt")

    write_sums(args.out, args.out / "DELIVERY_MANIFEST.txt")
    print(f"delivery package: {args.out}")
    return 0


def check_bundle_commit(bundle: Path, tag: str) -> None:
    info = (bundle / "BUILD_INFO.txt").read_text(encoding="utf-8")
    commit = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{tag}^{{commit}}"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if f"commit: {commit}" not in info or "uncommitted changes: no" not in info:
        raise SystemExit(f"{bundle} was not built from a clean checkout of {tag}")


def fetch(url: str, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / url.rsplit("/", 1)[1]
    if not target.is_file():
        with urllib.request.urlopen(url) as response, open(target, "wb") as out:
            shutil.copyfileobj(response, out)
    return target


def parse_md5sums(path: Path) -> dict[str, str]:
    sums = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            sums[name.lstrip("*")] = digest
    return sums


def git_archive(tag: str, target: Path) -> None:
    subprocess.run(
        ["git", "-C", str(ROOT), "archive", "--format=zip",
         f"--prefix=tracker-tool-{tag}/", "-o", str(target), tag],
        check=True,
    )


def write_sums(directory: Path, target: Path) -> None:
    lines = [
        f"{_digest(path, 'sha256')}  {path.relative_to(directory).as_posix()}"
        for path in sorted(directory.rglob("*"))
        if path.is_file() and path != target
    ]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _place(path: Path, directory: Path) -> None:
    if path.parent.resolve() != directory.resolve():
        shutil.copy2(path, directory / path.name)


def _digest(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
