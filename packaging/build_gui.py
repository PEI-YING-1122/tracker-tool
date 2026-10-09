"""Build the Tracker Tool GUI as a PyInstaller one-folder bundle.

Usage (from the repository root):

    uv run --group packaging python packaging/build_gui.py

The bundle is written to dist/TrackerTool/ unless --dist is given.
"""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "TrackerTool"


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

    return subprocess.call(build_command(args.dist, args.work))


if __name__ == "__main__":
    raise SystemExit(main())
