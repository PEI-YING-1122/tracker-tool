import platform
import sys
import traceback
from importlib import metadata
from pathlib import Path

import PySide6
from PySide6.QtCore import qVersion


def _package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "unknown"


BUILD_INFO_NAME = "BUILD_INFO.txt"


def gui_build_lines() -> list[str]:
    """Build information written next to a frozen bundle by packaging."""

    if not getattr(sys, "frozen", False):
        return ["GUI build: source checkout (not a packaged build)"]

    build_info = Path(sys.executable).parent / BUILD_INFO_NAME

    try:
        lines = build_info.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ["GUI build: packaged, build information missing"]

    return [f"GUI build {line}" for line in lines if line]


def environment_lines() -> list[str]:
    return [
        f"tracker-tool: {_package_version('tracker-tool')}",
        f"Python: {sys.version.split()[0]}",
        f"PySide6: {PySide6.__version__} (Qt {qVersion()})",
        f"OS: {platform.platform()}",
        *gui_build_lines(),
    ]


def format_diagnostics(context=(), exception=None) -> str:
    """Build plain-text diagnostics for a bug report.

    context is a sequence of (label, value) pairs describing what the user
    asked for. The exception, if any, is reported as raised: type, message,
    and traceback. Nothing is interpreted or classified here.
    """

    lines = ["Tracker Tool diagnostics", ""]
    lines += environment_lines()

    if context:
        lines.append("")
        lines += [f"{label}: {value}" for label, value in context]

    if exception is not None:
        lines += [
            "",
            f"Exception type: {type(exception).__module__}.{type(exception).__qualname__}",
            f"Exception message: {exception}",
            "",
            "".join(
                traceback.format_exception(
                    type(exception),
                    exception,
                    exception.__traceback__,
                )
            ).rstrip(),
        ]

    return "\n".join(lines) + "\n"
