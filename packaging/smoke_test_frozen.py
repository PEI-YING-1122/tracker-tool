"""Smoke-test a frozen Tracker Tool GUI bundle.

Runs the executable in smoke-test mode (see packaging/launch_gui.py). The
bundle passes only if the application starts, shows its main window, and
exits by itself with code 0. A crash, a missing Qt plugin (which blocks
on an error dialog), or a missing window fails the test.

Usage:

    python packaging/smoke_test_frozen.py dist/TrackerTool/TrackerTool.exe
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


SMOKE_TEST_ENV = "TRACKER_TOOL_GUI_SMOKE_TEST"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args(argv)

    if not args.executable.is_file():
        print(f"FAIL: executable not found: {args.executable}")
        return 1

    environment = dict(os.environ)
    environment[SMOKE_TEST_ENV] = "1"

    process = subprocess.Popen(
        [str(args.executable)],
        env=environment,
    )

    try:
        exit_code = process.wait(timeout=args.timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=30)
        print(f"FAIL: did not exit within {args.timeout:g} s")
        return 1

    if exit_code != 0:
        print(f"FAIL: exit code {exit_code}")
        return 1

    print("PASS: main window shown, clean exit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
