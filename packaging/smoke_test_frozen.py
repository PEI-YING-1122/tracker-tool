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
import re
import subprocess
import sys
from pathlib import Path


SMOKE_TEST_ENV = "TRACKER_TOOL_GUI_SMOKE_TEST"
# Same pattern as build_gui.MSVC_RUNTIME_DLL: these must not be bundled.
MSVC_RUNTIME_DLL = re.compile(r"(vcruntime|msvcp|concrt|vccorlib)\d+(_\w+)?\.dll", re.IGNORECASE)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args(argv)

    if not args.executable.is_file():
        print(f"FAIL: executable not found: {args.executable}")
        return 1

    required = [
        "BUILD_INFO.txt",
        "THIRD_PARTY_NOTICES.md",
        "USER_GUIDE.md",
        "USE_AND_LICENSE.md",
        "THIRD_PARTY_LICENSES/LGPL-3.0.txt",
        "THIRD_PARTY_LICENSES/GPL-3.0.txt",
    ]
    missing = [
        name
        for name in required
        if not (args.executable.parent / name).is_file()
    ]

    if missing:
        print(f"FAIL: delivery files missing: {', '.join(missing)}")
        return 1

    msvc_runtime = sorted(
        str(path.relative_to(args.executable.parent))
        for path in args.executable.parent.rglob("*.dll")
        if MSVC_RUNTIME_DLL.fullmatch(path.name)
    )

    if msvc_runtime:
        print(f"FAIL: Microsoft Visual C++ runtime DLLs bundled: {', '.join(msvc_runtime)}")
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
