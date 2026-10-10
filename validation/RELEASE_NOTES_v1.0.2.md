# Tracker Tool v1.0.2 — Release Notes

```text
Tag            : v1.0.2  (annotated) → 998ba70eb3e0256229c73bcd9fe7191c5f58d7a1
Tag message    : Artist 2D Track Interchange v1.0.2
Release title  : Tracker Tool v1.0.2 — PFTrack source-set integrity fix
Status         : RELEASED 2026-10-10 — https://github.com/PEI-YING-1122/tracker-tool/releases/tag/v1.0.2
```

The GitHub Release body is the section below.

---

Bugfix release of the Artist 2D Track Interchange Core (3DEqualizer R5, PFTrack 2017, SynthEyes 2304).

Unchanged from v1.0.1:

- the Canonical model
- conversion orchestration
- ShotConfig
- CLI arguments
- the formal Error Contract
- every conversion that produces output

### Fix

- **PFTrack source set with an empty member (CI-11).** Each file given to `convert-pftrack-source-set` (AutoTrack and UserTrack) must now contain at least one track.
  - If either file has none (an empty file, or an export with only the header), the conversion stops and names the empty file.
  - Previously the empty file was ignored and only the other file was converted, which could hide a wrong file or a failed export.
  - No new formal error code.

### Validation

- **Automated:** 316 tests pass (2 opt-in tests skipped by default). All 10 released golden outputs are byte-identical. The formal Error Contract behaviour is identical to v1.0.1.
- **Native import:** output converted from real PFTrack 2017 exports is byte-identical to the files that passed Artist Native Import for v1.0.1, so no new import was required.
- **Details:** `validation/RELEASE_READINESS_v1.0.2.md`.

### Known limitations

Unchanged from v1.0.1; see the v1.0.1 release notes.
