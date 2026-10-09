# Tracker Tool — Project Document Index

## Purpose

This index tells future contributors and Claude Code which project materials are authoritative and which are historical context.

Paths below were taken from the repository at the GUI architecture review (2026-10-09). Paths are relative to the repository root unless stated otherwise.

---

# 0. Release Baseline

```text
Release tag:      v1.0.0  → commit 79fd42d "freeze artist 2D track interchange v1 release candidate"
                  (v1.0.0-rc.1 points to the same commit)
Current main:     f72e44e "refactor shared conversion validation"  (one commit after v1.0.0)
pyproject.toml:   version = "0.1.0"  (does not match the v1.0.0 tag)
Python:           >=3.11 (.python-version: 3.11)
Runtime deps:     none
Dev deps:         pytest
Test suite:       176 tests, all passing on f72e44e

Branches (2026-10-09):
  release/1.0.x   v1.0.1 release candidate (CI-1/2/3, regression tests, version 1.0.1).
                  Pushed; NOT released. Status: validation/COVERAGE_MATRIX_v1.0.1.md
  gui/develop     GUI phase. Core code identical to v1.0.0 until v1.0.1 is merged in.
CI:               .github/workflows/tests.yml (pytest on Windows and Linux, uv --locked)
```

`f72e44e` only extracts `_validate_shot_config` and `_validate_observation_frame_ranges` in `conversion.py` from duplicated inline code. The validation order and error codes are unchanged, and all tests pass. It is a non-semantic refactor, but it is **not** the tagged release.

---

# 1. Authority Levels

## Level A — Released Implementation / Tests

Highest authority for v1.0.0 behavior.

### Core source

```text
src/tracker_tool/__init__.py                 package entry; re-exports cli.main
src/tracker_tool/config.py                   ShotConfig (dataclass; no self-validation)
src/tracker_tool/conversion.py               Orchestration + ShotConfig validation + frame-range validation
                                             + formal Error Contract raise sites
                                             public: convert_tracks(), convert_pftrack_source_set()
src/tracker_tool/canonical/models.py         Canonical model: Track, Observation
src/tracker_tool/canonical/validation.py     Canonical validation: validate_canonical_tracks()
```

### Source / Target adapters

```text
src/tracker_tool/adapters/threed/reader.py      3DE_R5 reader     read_3de_tracks(text, shot_config)
src/tracker_tool/adapters/threed/writer.py      3DE_R5 writer     write_3de_tracks(tracks, shot_config)
src/tracker_tool/adapters/pftrack/reader.py     PFTRACK_2017 reader
                                                read_pftrack_tracks(text, source_role)
                                                read_pftrack_source_set(autotrack_text, usertrack_text)
                                                (raises CROSS_SOURCE_TRACK_NAME_COLLISION)
src/tracker_tool/adapters/pftrack/writer.py     PFTRACK_2017 writer  write_pftrack_tracks(tracks)
src/tracker_tool/adapters/syntheyes/reader.py   SYNTHEYES_2304 reader read_syntheyes_tracks(text, shot_config)
src/tracker_tool/adapters/syntheyes/writer.py   SYNTHEYES_2304 writer write_syntheyes_tracks(tracks, shot_config)
```

### Error Contract implementation

There is no dedicated error module. Formal codes are raised as `ValueError(<CODE>)` with the code as the message:

```text
src/tracker_tool/conversion.py           MISSING_REQUIRED_SHOT_METADATA, INVALID_SHOT_METADATA,
                                         OBSERVATION_OUTSIDE_SHOT_RANGE, SAME_SOURCE_CONVERSION_NOT_ALLOWED,
                                         UNSUPPORTED_SOURCE_SOFTWARE, UNSUPPORTED_TARGET_SOFTWARE
src/tracker_tool/adapters/pftrack/reader.py  CROSS_SOURCE_TRACK_NAME_COLLISION
```

All other reader, writer, and canonical failures raise `ValueError` with descriptive text, which is not part of the contract. Some malformed inputs raise other exception types. See the GUI architecture review for details.

### CLI entry point

```text
pyproject.toml  [project.scripts] tracker-tool = "tracker_tool:main"
src/tracker_tool/cli.py   build_parser(), main(argv)
                          subcommands: convert, convert-pftrack-source-set
                          owns file I/O: read_text(utf-8), input/output path-collision check,
                          write_text(utf-8) only after successful conversion
```

### Core automated tests

```text
tests/test_canonical_track.py
tests/test_canonical_validation.py
tests/test_shot_config.py
tests/test_3de_reader.py        tests/test_3de_writer.py
tests/test_pftrack_reader.py    tests/test_pftrack_writer.py
tests/test_syntheyes_reader.py  tests/test_syntheyes_writer.py
tests/test_conversion.py        orchestration + Error Contract
tests/test_cli.py               CLI contract (output preservation, path safety)
```

Run with `uv run pytest -v`.

### Native Import Validation (release validation assets)

```text
validation/README.md     Artist import results per golden (all PASS)
validation/inputs/       golden native sources (3DE, PFTrack AutoTrack/UserTrack/source-set, SynthEyes)
validation/outputs/      golden target outputs that were imported into real 3DE R5 / PFTrack 2017 / SynthEyes 2304
```

Golden files are stored with CRLF line endings, which match the Windows output of `cli.main` (`Path.write_text` newline translation).

---

# 2. Level B — Authoritative v1.0.0 Specifications

```text
Shared Core specification:
- docs/INTERCHANGE_MASTER.md          formal v1 technical specification (architecture, ShotConfig,
                                      coordinate/frame semantics, CLI contract, Error Contract)
- docs/CANONICAL_2D_TRACK_CORE.md     Canonical model semantics (canonical_2d_track_core_v01)
- AGENTS.md                           shared project rules (architecture, preservation, GUI must-nots)
- PROJECT_GOAL.md                     high-level direction (see conflict note C-1)

3DEqualizer R5 adapter:
- docs/ADAPTER_3DE_R5.md

PFTrack 2017 adapter:
- docs/ADAPTER_PFTRACK_2017.md        (see conflict note C-2)

SynthEyes 2304 adapter:
- docs/ADAPTER_SYNTHEYES_2304.md

Error Contract:
- docs/INTERCHANGE_MASTER.md § "Error Contract"   ← the 7 formal codes (authoritative)
- docs/VALIDATION_CONTRACT.md § 13                ← validation-pipeline failure codes (see conflict note C-3)

Validation:
- docs/VALIDATION_CONTRACT.md         validation stages, artist import / round-trip boundary, precision classes

ShotConfig:
- docs/INTERCHANGE_MASTER.md § 6 and § "Shot Metadata Validity / Type Validity"
  (no separate ShotConfig document)

Release / validation:
- validation/README.md
- docs/INTERCHANGE_MASTER.md § 17–18  (Test 01–08 production evidence)

User-facing usage:
- README.md                           CLI usage, metadata rules, failure behavior
```

### GUI phase handoff (current)

```text
CLAUDE.md
docs/CORE_V1_HANDOFF.md
docs/PROJECT_DOCUMENT_INDEX.md   (this file)
```

---

# 3. Level C — Historical / Development Reference

Inside the repository:

```text
CLAUDE_FIRST_GUI_PROMPT.md   first GUI task prompt (one-off instruction, not a specification)
README_HANDOFF.txt           instructions for installing the GUI handoff package
```

Outside the repository (local only, never published):

- a manual copy of the repository
- an early project-initialization copy
- local notes
- pre-Core test runs (2026-08-29/30) with handoff diagnostics, historical conversion scripts, and real-software exports

None of these is part of v1.0.0, and none may be used as specification.

Real-software exports from those test runs are **evidence**, not specification. They contain production data, so they are
referred to in this repository by case ID only (e.g. "Test 08 AutoTrack export"), never by local path or shot name.

---

# 4. Known Conflicts Between Sources

These were reported during the GUI architecture review and remain **unresolved**. Do not resolve any of them by editing behavior without a project decision.

```text
C-1  PROJECT_GOAL.md §3.2 / AGENTS.md §10 list "Read-only Analysis" as v1 scope.
     Released Core contains no analysis module or API.

C-2  ADAPTER_PFTRACK_2017.md §2 documents the verified native grammar as including the
     "# ..." header lines. The released PFTrack reader rejects any file that starts with them
     ("Invalid PFTrack track name"), including a real PFTrack 2017 export.

C-3  VALIDATION_CONTRACT.md §13 lists hard-failure codes (e.g. PFTRACK_SOURCE_ROLE_UNRESOLVED,
     3DE_NATIVE_WHITESPACE_MISMATCH, PFTRACK_NATIVE_FORMAT_MISMATCH, SAME_TRACK_FRAME_CONFLICT)
     that Core does not emit. INTERCHANGE_MASTER.md "Error Contract" defines only 7 formal codes
     and states that other messages are not contractual.

C-4  The v1.0.0 tag (79fd42d) and main (f72e44e) differ by one non-semantic refactor commit.
     f72e44e is local only (origin/main = 79fd42d). pyproject.toml version is 0.1.0.
     Decision 2026-10-09: v1.0.0 tag is the baseline; main is not treated as v1.0.0.

C-5  INTERCHANGE_MASTER.md §17 Test 08 (PFTrack source) evidence was produced with the historical
     script convert_test08.py (kept outside the repository),
     not with the released PFTrack reader (see CI-1).

C-6  validation/README.md documents 8 golden outputs. The 2 pftrack_usertrack_* outputs in
     validation/outputs have no README entry (DOC-1).
```

Details, reproductions, and priorities: `docs/gui/CORE_ISSUES_FROM_GUI_REVIEW.md`.

---

# 5. Conflict Rule

If two sources disagree, use the following decision path:

```text
Is released Core behavior covered by passing tests?
    │
    ├─ Yes → treat tested released behavior as current baseline
    │
    └─ No
        ↓
Check authoritative v1.0.0 specification
        ↓
Report ambiguity before modifying behavior
```

Do not use an old prompt, old issue, or superseded specification to silently change released behavior.

---

# 6. GUI Documents

The GUI phase starts after Core v1.0.0.

Current GUI documentation:

```text
docs/gui/GUI_DEVELOPMENT_PLAN.md          approved in principle 2026-10-09; decisions D1–D7,
                                          G1/G2/G5 file-level change plan, phases, branch handling
docs/gui/CORE_ISSUES_FROM_GUI_REVIEW.md   Core issues CI-1…CI-11 with reproductions,
                                          spec/release items, v1.0.1 recommendation
```

Possible later split-outs, created only when needed:

```text
docs/gui/GUI_TEST_PLAN.md
docs/gui/GUI_PACKAGING.md
```

---

# 7. Definition of "Authoritative"

A document should only be marked authoritative if it describes the released v1.0.0 behavior currently expected by the project.

A document is not authoritative merely because:

- it is newer by file modification date
- it has a polished name
- it was used during development
- it contains more detail
- it was generated by an AI tool

Released behavior and validated contracts are the baseline.
