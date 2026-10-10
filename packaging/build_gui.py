"""Build the Tracker Tool GUI as a PyInstaller one-folder bundle.

Usage (from the repository root):

    uv run --group packaging python packaging/build_gui.py

The bundle is written to dist/TrackerTool/ unless --dist is given.
"""

import argparse
import hashlib
import os
import re
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
    PACKAGING_DIR / "delivery" / "VC_REDIST_INSTALL.md",
)
LICENSE_TEXTS_DIR = PACKAGING_DIR / "licenses"
LICENSE_TEXTS_TARGET = "THIRD_PARTY_LICENSES"

# DLLs the Python build ships next to its extension modules. PyInstaller
# resolves them through PATH, so another copy on PATH (for example Git for
# Windows' OpenSSL) could otherwise end up in the bundle.
PYTHON_DLLS_DIR = Path(sys.base_prefix) / "DLLs"
PYTHON_RUNTIME_DLLS = ("libcrypto-3-x64.dll", "libssl-3-x64.dll", "libffi-8.dll")

# Microsoft Visual C++ runtime DLLs that Python, PySide6 and shiboken6 put
# next to their binaries. They are not shipped: workstations use the
# Microsoft Visual C++ Redistributable instead.
MSVC_RUNTIME_DLL = re.compile(r"(vcruntime|msvcp|concrt|vccorlib)\d+(_\w+)?\.dll", re.IGNORECASE)


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

    result = subprocess.call(build_command(args.dist, args.work), env=build_env())

    if result == 0:
        bundle = args.dist / APP_NAME
        check_python_runtime_dlls(bundle)
        for path in remove_msvc_runtime_dlls(bundle):
            print(f"removed {path.relative_to(bundle)}")
        write_build_info(bundle / BUILD_INFO_NAME)
        copy_delivery_documents(bundle)

    return result


def build_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PATH"] = os.pathsep.join([str(PYTHON_DLLS_DIR), env.get("PATH", "")])
    return env


def check_python_runtime_dlls(bundle: Path) -> None:
    """Fail the build if a bundled runtime DLL is not the Python build's copy."""
    for name in PYTHON_RUNTIME_DLLS:
        expected = PYTHON_DLLS_DIR / name
        bundled = bundle / "_internal" / name
        if not expected.is_file() or not bundled.is_file():
            continue
        if _sha256(bundled) != _sha256(expected):
            raise SystemExit(
                f"{bundled} does not match {expected}; "
                "a different copy was picked up from PATH"
            )


def remove_msvc_runtime_dlls(bundle: Path) -> list[Path]:
    removed = sorted(
        path for path in bundle.rglob("*.dll") if MSVC_RUNTIME_DLL.fullmatch(path.name)
    )
    for path in removed:
        path.unlink()
    return removed


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
