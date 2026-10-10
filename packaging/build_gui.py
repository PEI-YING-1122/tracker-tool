"""Build the Tracker Tool GUI as a PyInstaller one-folder bundle.

Usage (from the repository root):

    uv run --group packaging python packaging/build_gui.py

The bundle is written to dist/TrackerTool/ unless --dist is given.
"""

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "TrackerTool"
BUILD_INFO_NAME = "BUILD_INFO.txt"


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
        write_build_info(args.dist / APP_NAME / BUILD_INFO_NAME)

    return result


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
