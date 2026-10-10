# Tracker Tool v1.0.1 — Release Notes (draft, not released)

```text
Tag (proposed) : v1.0.1  (annotated, on release/1.0.x)
Tag message    : Artist 2D Track Interchange v1.0.1
Release title  : Tracker Tool v1.0.1 — Artist 2D Track Interchange bugfix release
Status         : DRAFT. Not tagged, not released. Awaiting owner approval.
```

The GitHub Release body is the section below.

---

Bugfix release of the Artist 2D Track Interchange Core (3DEqualizer R5, PFTrack 2017, SynthEyes 2304). It makes the Core usable with real native exports.

Unchanged from v1.0.0:

- the Canonical model
- conversion orchestration
- ShotConfig
- CLI arguments
- the formal Error Contract

### Fixes

- **PFTrack 2017 export layout (CI-1).** Real PFTrack 2017 exports are now read: both verified header variants (with or without `zdepth`) and one blank separator line before each track block. Unverified layouts are still rejected. Comment and blank lines are not skipped generically.
- **Truncated input (CI-2).** Truncated or empty 3DE and PFTrack input now fails with a descriptive `ValueError` instead of `IndexError`.
- **3DE target track names (CI-3).** A track name with leading or trailing whitespace cannot be written to 3DE without changing it, so conversion now stops instead of writing an invalid file. Names are never trimmed or renamed.
- **3DE point field (CI-12).** The value `3` on the line after the point name, which real 3DEqualizer R5 exports contain, is now accepted together with `0`. Other values are still rejected. The value does not affect observations, and the writer still emits `0`.
- **SynthEyes tracker named `#` (CI-13).** This is a conservative input guard. A SynthEyes source containing a tracker named exactly `#` now stops with an explanation, instead of carrying the tracker into the target. In all verified cases the tracker came from importing a file with a `#` comment line. Check it in SynthEyes, delete it if it is not tracking data or rename it, then export again. Nothing is deleted or skipped automatically. Other names such as `#1` are unaffected.

### Other changes

- The package version is now `1.0.1`; v1.0.0 declared `0.1.0`.
- Regression coverage:
  - byte-for-byte comparison with all released golden outputs
  - truncation fuzzing
  - native export layouts
  - name round-trips
  - output-equivalence checks
  - opt-in tests against real production exports, which are not stored in this repository
- GitHub Actions runs the full test suite on Windows and Linux.

### Validation

- **Automated:** 304 tests pass (2 opt-in tests skipped by default). All 10 released golden outputs are byte-identical. Formal Error Contract behaviour is identical to v1.0.0.
- **Artist Native Import (2026-10-10):** output converted from real PFTrack 2017 exports imported successfully into 3DEqualizer R5 and SynthEyes 2304 (4 cases, all PASS).
  - A SynthEyes re-export round-trip gave a maximum error of 0.001018 px (ACCEPTABLE_SERIALIZATION).
  - Details: `validation/COVERAGE_MATRIX_v1.0.1.md`, `validation/README.md`.

Automated test results are not a substitute for import into the real target software.

### Known limitations

- 3DE exports containing a point with no samples cannot be converted, as specified (each track needs at least one observation).
- Coordinates smaller than 1e-4 or at least 1e16 in magnitude are written in scientific notation. Whether 3DE R5 and PFTrack 2017 accept that is not yet verified.
- The target plate in 3DE or SynthEyes must cover the full production frame range and use the conversion resolution.
