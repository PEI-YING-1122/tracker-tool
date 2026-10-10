# Tracker Tool GUI — Packaging

Status: **Windows one-folder bundle verified** (local build and CI). Not yet a release artifact: the GUI cannot convert until phase P1.

## Approach

**PyInstaller**, one-folder (`--onedir`), windowed. The build runs from the locked uv environment.

| Item | Value |
|---|---|
| Tool | PyInstaller (dependency group `packaging`, locked in `uv.lock`) |
| Entry script | `packaging/launch_gui.py` |
| Build script | `packaging/build_gui.py` |
| Output | `dist/TrackerTool/TrackerTool.exe` plus `_internal/` |
| Size | about 90 MB unpacked (PySide6-Essentials 6.11.2, Python 3.11) |
| Build time | about 25 s locally |
| Package metadata | `--copy-metadata tracker-tool`, so the window shows the Core version |

One-folder was chosen over one-file. It starts faster, does not unpack into a temp directory on every launch, and is less often flagged by antivirus heuristics.

## Commands

```powershell
uv sync --locked --all-extras --group packaging
uv run --group packaging python packaging/build_gui.py
uv run python packaging/smoke_test_frozen.py dist/TrackerTool/TrackerTool.exe
```

## Smoke test

When `TRACKER_TOOL_GUI_SMOKE_TEST` is set, `packaging/launch_gui.py` exits by itself about 2 s after start-up:

- code **0** if the main window is visible;
- code **3** otherwise.

`packaging/smoke_test_frozen.py` requires exit code 0 within a timeout.

This catches failures that a simple "process is still running" check misses. In particular, a bundle without the Qt platform plugin blocks on an error dialog and keeps running. This was verified: a bundle with `PySide6/plugins/platforms` removed **fails** the smoke test, and the intact bundle passes, both with the native Windows platform and with `QT_QPA_PLATFORM=offscreen`.

The hook lives only in the packaging entry script. The `tracker_tool_gui` package contains no test hooks.

## CI

The `package (windows-latest)` job in `.github/workflows/tests.yml` runs after both pytest jobs pass:

1. builds the bundle;
2. runs the smoke test;
3. uploads `dist/TrackerTool` as the artifact `TrackerTool-windows-<sha>`, kept for 14 days.

## Risks still open

| Risk | Status |
|---|---|
| Unsigned executable; antivirus false positives on production workstations | Open. Needs a test on a production workstation image, and a code-signing decision before distribution |
| Clean machine without Python | Covered in principle by the CI runner. Still needs a check on a production workstation |
| Non-ASCII install paths and UNC paths | Open. Test once conversion works (P3) |
| Version shown in the GUI | Shows the bundled `tracker-tool` metadata. `gui/develop` reports 0.1.0 until v1.0.1 is merged in |

## PySide6 version pin

`PySide6-Essentials>=6.8,<6.12` (locked: 6.11.2).

PySide6 6.12.0 (released 2026-10-08) on Linux with Python 3.11 drops references to `None` / `True` on ordinary calls, for example void methods and `Signal().emit()`. After enough calls the interpreter aborts at exit with `Fatal Python error: bool_dealloc` / `none_dealloc`.

How this was established:

- CI probes on `ubuntu-latest` measured `sys.getrefcount` drift per operation.
- The Windows build and PySide6 6.11.2 show no drift.
- With 6.11.2 the full suite passes on Linux.

Before lifting the pin, re-check a newer PySide6 on Linux / Python 3.11 with the same probe.

## Delivery documents in the bundle

`packaging/build_gui.py` copies these next to `TrackerTool.exe`:

- `BUILD_INFO.txt`
- `THIRD_PARTY_NOTICES.md`
- `USER_GUIDE.md`
- `USE_AND_LICENSE.md`
- `THIRD_PARTY_LICENSES/`

`packaging/smoke_test_frozen.py` fails if any of them is missing.

Only Windows is a delivery platform. No Linux executable, public download, code signing, or auto-update is planned for the first release.
