# Tracker Tool v1.1.0 — Release Notes

```text
Tag            : v1.1.0  (annotated) → 437e7e60fdd354120e73360bd39f78c8012cda8b
Tag message    : Tracker Tool v1.1.0 — Windows GUI
Release title  : Tracker Tool v1.1.0 — Windows GUI
Status         : RELEASED 2026-10-10 — https://github.com/PEI-YING-1122/tracker-tool/releases/tag/v1.1.0
```

The GitHub Release body is the section below. The Windows GUI executable is delivered internally only and is **not** attached to the GitHub Release.

---

Adds a Windows desktop GUI to the Artist 2D Track Interchange Core (3DEqualizer R5, PFTrack 2017, SynthEyes 2304).

Unchanged from v1.0.2:

- the Canonical model
- ShotConfig
- CLI arguments and output
- the formal Error Contract
- every conversion that produces output

### New

- **Tracker Tool GUI** (`tracker-tool-gui`, optional extra `gui`).
  - One window: Source → Target → Shot → Output → Convert → Result.
  - The source software, PFTrack role and plate settings are always chosen by the user; nothing is detected from file names or content.
  - The target cannot be the same software as the source.
  - Shot values are not remembered between shots.
  - Results show `PASS`, a formal error code with the related fields highlighted, or a descriptive Core message. `Copy diagnostics` copies version and settings information.
  - Asks before overwriting an existing output file.
- **Shared application API for the CLI and the GUI.**
  - `tracker_tool.contract`: supported software IDs, PFTrack roles and the formal error codes.
  - `tracker_tool.app`: file-level conversion (`convert_file`, `convert_pftrack_source_set_files`).
  - The CLI now uses the same functions. Its behaviour and output are unchanged.

### Validation

- **Automated:** 468 tests pass (2 opt-in tests skipped by default), including 102 GUI tests on the native Windows platform. All 10 released golden outputs are byte-identical. The formal Error Contract behaviour is identical to v1.0.2.
- **Native import:** output produced through the GUI from real PFTrack 2017 exports is byte-identical to the files that passed Artist Native Import for v1.0.1.
- **Artist GUI trial (P6):** passed (Tracking Artist 01, 2026-10-10).
- **Details:** `validation/RELEASE_READINESS_v1.1.0.md`.

### Known limitations

- The interface is in English.
- PySide6 is pinned below 6.12 because of a crash in PySide6 6.12.0 on Linux / Python 3.11.
- Otherwise unchanged from v1.0.2; see the v1.0.1 release notes.
