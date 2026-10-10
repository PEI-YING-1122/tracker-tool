"""Build the Tracker Tool GUI as a PyInstaller one-folder bundle.

Usage (from the repository root):

    uv run --group packaging python packaging/build_gui.py

The bundle is written to dist/TrackerTool/ unless --dist is given.
"""

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "TrackerTool"
BUILD_INFO_NAME = "BUILD_INFO.txt"

# Delivery documents copied next to TrackerTool.exe (internal delivery).
PACKAGING_DIR = ROOT / "packaging"
DELIVERY_FILES = (
    PACKAGING_DIR / "THIRD_PARTY_NOTICES.md",
    PACKAGING_DIR / "delivery" / "USER_GUIDE.md",
    PACKAGING_DIR / "delivery" / "USE_AND_LICENSE.md",
)
LICENSE_TEXTS_DIR = PACKAGING_DIR / "licenses"
LICENSE_TEXTS_TARGET = "THIRD_PARTY_LICENSES"


def build_command(dist_dir: Path, work_dir: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        # importlib.metadata.version("tracker-tool") is shown in the GUI.
        "--copy-metadata",
        "tracker-tool",
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(work_dir),
        str(ROOT / "packaging" / "launch_gui.py"),
    ]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument(
        "--work",
        type=Path,
        default=ROOT / "build" / "pyinstaller",
    )
    args = parser.parse_args(argv)

    result = subprocess.call(build_command(args.dist, args.work))

    if result == 0:
        bundle = args.dist / APP_NAME
        write_build_info(bundle / BUILD_INFO_NAME)
        copy_delivery_documents(bundle)

    return result


def copy_delivery_documents(bundle: Path) -> None:
    for source in DELIVERY_FILES:
        shutil.copy2(source, bundle / source.name)

    target = bundle / LICENSE_TEXTS_TARGET
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(LICENSE_TEXTS_DIR, target)


def _git(*args) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(ROOT), *args],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def write_build_info(path: Path) -> None:
    """Record what the bundle was built from, for bug reports."""

    from importlib import metadata

    commit = _git("rev-parse", "HEAD") or "unknown"
    dirty = "yes" if _git("status", "--porcelain", "--untracked-files=no") else "no"

    lines = [
        f"commit: {commit}",
        f"uncommitted changes: {dirty}",
        f"built: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"tracker-tool: {metadata.version('tracker-tool')}",
        f"PySide6: {metadata.version('PySide6-Essentials')}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
