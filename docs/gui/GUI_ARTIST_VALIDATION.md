# Tracker Tool GUI — Artist Validation Record

## P6 — First Artist Trial

```text
Date      : 2026-10-10
Artist    : Tracking Artist 01
Build     : GUI trial fde0c161be71987474d85accb31e673c91e40fc4
            (BUILD_INFO.txt: uncommitted changes: no; tracker-tool 1.0.1; PySide6 6.11.2)
Platform  : Windows (frozen one-folder bundle, PyInstaller)
Guide     : docs/gui/GUI_TRIAL_GUIDE.md
Result    : PASS
```

| # | Check | Result |
|---|---|---|
| 1 | GUI starts normally | PASS |
| 2 | Tracking point conversion runs normally | PASS |
| 3 | Source, Target, PFTrack Role, resolution and frame inputs are clear and work | PASS |
| 4 | Error messages and highlighting of the related input sections | PASS |
| 5 | Overwrite confirmation; cancelling leaves the existing file untouched | PASS |
| 6 | Overall interface is clear, intuitive and convenient | PASS |

- **Bugs found:** none.
- **Requested changes to workflow or interface design:** none.
- **Owner decision (2026-10-10):** the GUI function and usability are accepted. The GUI design is frozen for the release: no features beyond those validated here. Release preparation may start.

### Evidence boundaries

- **This is an Artist usability validation of the GUI.** It is not a new Native Import validation of the conversion.
- **Conversion correctness rests on separate evidence:**
  - Core v1.0.1 Native Import records (`validation/COVERAGE_MATRIX_v1.0.1.md`);
  - automated proof that GUI output is byte-identical to CLI output, to the 10 released goldens, and to the Artist-validated A1–A4 files.
- **Not exercised in this trial:**
  - production workstation antivirus / code signing (no blocking was reported);
  - UNC network paths.

These remain listed in `docs/gui/GUI_RELEASE_READINESS.md`.
