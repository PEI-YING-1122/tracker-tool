# Tracker Tool GUI — Development Plan

```text
Status        : APPROVED IN PRINCIPLE (2026-10-09), with the decisions recorded in §1
Core baseline : v1.0.0 tag → 79fd42d (immutable)
Phase         : P2 preparation on gui/develop (GUI skeleton, dependencies, test infrastructure).
                Core integration (P1) waits for v1.0.1.
Companion     : docs/gui/CORE_ISSUES_FROM_GUI_REVIEW.md
```

The GUI makes the released Core usable by artists. It does not change what the Core means or does.

---

## 1. Decisions (2026-10-09)

| # | Decision |
|---|---|
| D1 | Baseline is the `v1.0.0` tag (`79fd42d`). `main` (`f72e44e`) is **not** treated as v1.0.0. Including `f72e44e` requires an explicit decision (§11). |
| D2 | G1 (application boundary), G2 (exported constants), and G5 (GUI dependency and entry point) are approved, subject to the conditions in §9. |
| D3 | CI-1 is a Core issue. The GUI performs no header stripping, preprocessing, or cleanup. Whether it goes into v1.0.1 is evaluated in the Core Issues document §6. |
| D4 | Core issues are tracked separately. P0 before GUI production work: CI-1, CI-2, CI-3. P1: CI-5, CI-7. Validate or define first: CI-4, CI-6. Deferred: CI-8, CI-9, CI-10. |
| D5 | **Analysis is not in GUI v1.** No new Analysis Core feature is added during the GUI phase. |
| D6 | The Target list keeps every software visible but **disables** the entry equal to the Source, with a tooltip. Core `SAME_SOURCE_CONVERSION_NOT_ALLOWED` remains the final authority. |
| D7 | The `pyproject.toml` version mismatch (REL-1) is a separate release issue. It is not bundled with GUI dependency commits. |
| D8 | Strictly sequential: Core `v1.0.1` (CI-1/2/3 + regression tests + Native Import Validation + tag) comes first. GUI work starts only after `v1.0.1`. |
| D9 | GUI branch is created from `v1.0.1`, then `f72e44e` is cherry-picked, then G2 → G1 → G5. `f72e44e` never enters v1.0.1. |
| D10 | CI-11 is decided (each specified source-set member must yield at least 1 track). It is implemented as a separate Core change before P4. The GUI does not pre-check it. |

---

## 2. Current Core Architecture (v1.0.0)

```text
cli.main(argv)                              ← only file-I/O layer
 ├ input/output path collision check (Path.resolve)
 ├ Path.read_text(encoding="utf-8")
 ├ ShotConfig(width, height, start, end, source, target)
 ↓
conversion.convert_tracks(text, cfg, pftrack_source_role=)            pure text → text
conversion.convert_pftrack_source_set(auto_text, user_text, cfg)
 ├ ShotConfig validation        → MISSING_REQUIRED_SHOT_METADATA / INVALID_SHOT_METADATA
 ├ source == target             → SAME_SOURCE_CONVERSION_NOT_ALLOWED
 ├ Reader dispatch by ID        → list[Track]   | UNSUPPORTED_SOURCE_SOFTWARE
 │    source set: CROSS_SOURCE_TRACK_NAME_COLLISION
 ├ validate_canonical_tracks    → descriptive ValueError (not contract)
 ├ observation frame range      → OBSERVATION_OUTSIDE_SHOT_RANGE
 └ Writer dispatch by ID        → str           | UNSUPPORTED_TARGET_SOFTWARE
 ↓
cli: Path.write_text(encoding="utf-8")  only after success
     (newline translation → CRLF on Windows; matches validation/outputs byte-for-byte)
```

Properties that matter for the GUI:

- **Errors:** every error is a `ValueError`. A formal code is the exception message itself.
- **Fail-fast:** only the first error is reported. There are no warnings and no location data (track or line).
- **Missing pieces:** no progress hooks, no Analysis, no service layer.

---

## 3. Integration Boundary

Target dependency direction:

```text
GUI (tracker_tool_gui) ─┐
                        ├─→ tracker_tool.app ─→ tracker_tool.conversion ─→ readers / canonical / writers
CLI (tracker_tool.cli) ─┘          │
                                   └─→ tracker_tool.contract   (formal codes, software IDs, roles)
```

- The GUI calls Core **in-process**, not through a subprocess.
- The GUI may import only `tracker_tool.app`, `tracker_tool.contract`, and `tracker_tool.config`. An architecture test enforces this.
- The GUI never imports `adapters` or `canonical` and never holds Canonical data in v1.

Before G1 lands, the GUI must not exist in production form. Phases are ordered so the GUI is built only after `app.py` exists (§10).

---

## 4. Responsibilities

### Must be reused from Core — never reimplemented in the GUI

- native parsing
- frame mapping
- coordinate conversion
- Canonical validation
- ShotConfig validation, including value ranges and `bool` rejection
- the same-source rule (the GUI only *presents* it, D6)
- source-set aggregation and collision detection
- native writing
- the path-collision check
- success-only writing, file encoding, and newline behavior
- formal error classification (`contract.formal_error_code`, G2)

### GUI-only

- type-level input checks (is the field an integer, is it empty)
- presentation, busy state, and preferences

### State ownership

| Owner | State |
|---|---|
| GUI | Raw form text, mode (single / source set), selected IDs, paths, busy flag, last result or error, preferences (last directories, window geometry) |
| Core | ShotConfig validity, Canonical tracks, output text, error classification, file-write semantics |

**ShotConfig values are not persisted between sessions.** Re-using one shot's resolution or start frame on another shot is a silent geometry or frame error.

---

## 5. Framework

**PySide6 with Qt Widgets** (not QML).

- `PROJECT_GOAL.md` §9 already names PySide6.
- It is a native Windows desktop toolkit, LGPL-licensed, and supports Python 3.11.
- Widgets can be tested headlessly with pytest-qt (`QT_QPA_PLATFORM=offscreen`).
- The dependency is `PySide6-Essentials`, without WebEngine, installed as an optional extra. Core stays dependency-free.

---

## 6. Workflow and Layout (GUI v1)

One window, one form, top to bottom:

```text
┌ Tracker Tool ──────────────────────────────────────────────┐
│ Source software  [ 3DEqualizer R5 (3DE_R5)            ▾ ]  │
│   PFTrack only:  (•) Single file   Role [ Select…     ▾ ]  │   no default role
│                  ( ) Source set (AutoTrack + UserTrack)    │
│ Input            [ ............................ ] [Browse]  │   two inputs in source-set mode
│ Target software  [ Select…                            ▾ ]  │   entry equal to Source disabled (D6)
│ ── Shot ─────────────────────────────────────────────────  │
│ Width [     ]   Height [     ]   Start frame [     ]       │
│ End frame [     ]   ☐ Unknown                              │
│ Output           [ ............................ ] [Save…]   │
│                                              [ Convert ]   │
│ ── Result ───────────────────────────────────────────────  │
│ PASS — written to …            Artist Import: NOT VERIFIED │
│ ▸ Details   [Copy diagnostics]   [Open folder]             │
└────────────────────────────────────────────────────────────┘
```

### Source and Target

- Each combo item shows the product name together with the formal ID. Items come from `contract.SUPPORTED_SOFTWARE`.
- No auto-detection from file name or content.
- When the Source changes so that it equals the current Target, the Target resets to "Select…". The GUI never picks a different target automatically.
- In source-set mode the Source is fixed to PFTRACK_2017, so the PFTRACK_2017 target is disabled.

### PFTrack role

- Required in single-file mode, with no default. Choices come from `contract.PFTRACK_SOURCE_ROLES`.
- Source-set mode has two labelled inputs, AutoTrack and UserTrack, and no role selector, matching the CLI.

### ShotConfig fields

- Integer-only text fields. The GUI checks only "is this an integer".
- An empty field is passed as `None`, and Core then reports `MISSING_REQUIRED_SHOT_METADATA`.
- The GUI does **not** enforce `width > 0` or `end ≥ start`. Core reports `INVALID_SHOT_METADATA`.
- End frame "Unknown" means `production_end_frame=None`.

### Output path

- Chosen with a Save dialog. The OS overwrite confirmation is acceptable.
- The input/output collision check is performed by `app`.

### Out of scope for GUI v1

Analysis (D5), batch conversion, drag and drop, presets, track preview.

---

## 7. Validation and Error Presentation

Core produces PASS or FAIL only. **The GUI does not invent WARNING.** Classification is by exception identity, through `contract.formal_error_code(exc)`. Conditions are never re-interpreted.

| Core outcome | GUI presentation |
|---|---|
| Success | **PASS** plus output path. Always shown alongside: "Core conversion PASS ≠ Artist Import PASS in the target software" (VALIDATION_CONTRACT §2, §8) |
| `ValueError` that is a formal code | **FAIL — `<CODE>`**, a fixed one-line explanation per code, and highlighting of the related input (e.g. Shot fields for `INVALID_SHOT_METADATA`) |
| Other `ValueError` | **FAIL — Core rejected the input**, the raw message shown verbatim, marked "message is not part of the Error Contract" |
| Any other exception (e.g. CI-2 `IndexError`) | **FAIL — Unexpected Core failure**, traceback in Details, "please report as a Core issue" |
| `OSError` (read or write) | **FAIL — File error** (GUI domain) |

"Copy diagnostics" copies the following text:
- software IDs, role, ShotConfig values, input and output paths;
- the exception type and message;
- the Core version and the GUI version.

---

## 8. Progress, Busy State, and Completion

- Conversion runs in a `QThreadPool` worker so the UI stays responsive on large files and network paths.
- While busy: Convert is disabled, the form is read-only, and the status bar shows an indeterminate state.
- There is no percentage progress. Core has no hooks, and none are proposed: measured conversions take milliseconds.
- On completion, the Result panel updates. The form keeps its values for corrections.

---

## 9. G1 / G2 / G5 — File-level Change Plan (NOT YET EXECUTED)

All three apply to a branch based on the agreed baseline (§11). Each item lists the files touched, the exact change, why semantics are unchanged, and how that is proven.

### 9.0 First commit: regression net before touching Core

New tests that pass **on the unmodified baseline**, so that the later moves are measured against them:

| File | Content |
|---|---|
| `tests/test_golden_parity.py` (new) | Parametrized over all 10 input/output pairs in `validation/`: the 8 documented in `validation/README.md` (Golden 01, 02, 03, 05) plus the 2 undocumented `pftrack_usertrack_*` outputs (see DOC-1 in the Core Issues document). Runs `cli.main` into `tmp_path`. Asserts the output bytes equal `validation/outputs/<golden>` byte-for-byte on Windows. On other platforms it compares after newline normalization and records the platform. Closes TEST-1. |
| `tests/test_app.py` (new; first version targets `cli.main`) | The file-level contract as executable checks: success-only write; no output created on failure; existing output byte-identical after failure, for each failure class (formal code, reader error, CI-2 `IndexError`); collision rejected for input, autotrack, and usertrack, including different spellings of the same path (relative vs absolute, `.\x` vs `x`); a non-ASCII track name preserved through UTF-8; output newline bytes equal to `Path.write_text` of the same string (CRLF on Windows). |

### 9.1 G2 — `tracker_tool.contract`: single source of the contract constants

| File | Change |
|---|---|
| `src/tracker_tool/contract.py` (new) | `SOFTWARE_3DE_R5 = "3DE_R5"`, `SOFTWARE_PFTRACK_2017`, `SOFTWARE_SYNTHEYES_2304`, `SUPPORTED_SOFTWARE` (tuple, display order). `PFTRACK_SOURCE_ROLE_AUTOTRACK`, `…_USERTRACK`, `PFTRACK_SOURCE_ROLES`. One constant per formal code (7) and `FORMAL_ERROR_CODES: frozenset`. `formal_error_code(exc) -> str \| None`: returns the code only when `exc` is a `ValueError` whose sole argument is a member of `FORMAL_ERROR_CODES`. No imports from other `tracker_tool` modules, so there are no import cycles. |
| `src/tracker_tool/conversion.py` | Replace every contract string literal with the constant of the same value: raise sites and ID comparisons. On the v1.0.0 tag this is 27 literal occurrences; with `f72e44e`, 21. |
| `src/tracker_tool/adapters/pftrack/reader.py` | Role literals `"AUTOTRACK"` / `"USERTRACK"` and `CROSS_SOURCE_TRACK_NAME_COLLISION` → constants. |
| `src/tracker_tool/cli.py` | `source_software="PFTRACK_2017"` → constant. |
| `tests/test_contract.py` (new) | `FORMAL_ERROR_CODES` equals the 7 codes in `INTERCHANGE_MASTER.md` "Error Contract" (literal list in the test as the spec mirror). Each code is actually raised by a minimal Core input, and `formal_error_code` returns it. Descriptive `ValueError` → `None`. `IndexError` → `None`. `SUPPORTED_SOFTWARE` contains exactly the 3 IDs and no aliases. |

**Why semantics are unchanged:**
- Each constant has the identical string value, so `ValueError(CONST).args` and every `==` comparison are identical.
- The exception type stays `ValueError`. No custom exception class is introduced.
- Writers and the Canonical module are untouched.

**Single-source rule:** the GUI imports these constants. It defines no codes, IDs, or roles of its own. A GUI test asserts that the GUI module source contains none of these literals.

### 9.2 G1 — `tracker_tool.app`: shared file-level conversion

| File | Change |
|---|---|
| `src/tracker_tool/app.py` (new) | `convert_file(input_path, output_path, shot_config, *, pftrack_source_role=None) -> None` and `convert_pftrack_source_set_files(autotrack_path, usertrack_path, output_path, shot_config) -> None`. Bodies are a **verbatim move** of `cli.py` lines 116–146 and 151–196: same `Path.resolve()` comparison, same `ValueError("Input and output paths must be different")`, same read order (autotrack, then usertrack), `read_text(encoding="utf-8")`, the same `conversion` call, then `write_text(encoding="utf-8")` only after it returns. Accepts `str \| os.PathLike`. |
| `src/tracker_tool/cli.py` | `main()` keeps argparse unchanged. It builds `ShotConfig` exactly as today and calls the `app` functions. `build_parser()` is unchanged. |
| `tests/test_app.py` | Switched from `cli.main` to `app.*`. The same assertions as §9.0 must pass unmodified. |
| `tests/test_golden_parity.py` | Extended: for each golden, `cli.main` bytes == `app` bytes == golden bytes. |

**Why semantics are unchanged:**
- The code is moved, not rewritten: the same statements run in the same order, with the same arguments to `read_text` and `write_text` (so encoding and newline translation are identical).
- `test_cli.py` is unmodified.
- §9.0 tests written against the old CLI pass against `app`.
- Golden bytes are identical through both paths.

**Not changed by G1:**
- BOM handling (CI-7)
- atomic write (the CLI uses a plain `write_text`; no temp-file + replace is introduced)
- any error type or message

### 9.3 G5 — GUI dependency and entry point

Lands **together with the GUI skeleton** (phase P2), so the entry point resolves to real code.

| File | Change |
|---|---|
| `pyproject.toml` | **Done on `gui/develop`.** `[project.optional-dependencies] gui = ["PySide6-Essentials>=6.8,<7"]` (locked: 6.12.0). `[project.gui-scripts] tracker-tool-gui = "tracker_tool_gui.__main__:main"` (no console window on Windows). `[dependency-groups] dev` gains `pytest-qt` **and** `PySide6-Essentials`, because pytest-qt fails at startup without a Qt binding; this affects only development environments. `qt_api = "pyside6"` in pytest options. **`version` is not touched** (REL-1 lives on `release/1.0.x`). |
| `[tool.uv.build-backend]` | **Verified:** `module-name = ["tracker_tool", "tracker_tool_gui"]` works with the pinned `uv_build`. The wheel contains both packages plus the console and GUI entry points. |
| `uv.lock` | Regenerated by `uv lock`. **Merge rehearsal (2026-10-09):** merging `release/1.0.x` into `gui/develop` in a scratch clone produced no conflicts. The result had version 1.0.1, `uv lock --check` passed, and the suite gave 286 passed, 1 skipped. Run `uv lock --check` again at the real merge. |
| GUI tests | `tests/gui/`. Qt tests call `pytest.importorskip("PySide6")`. Architecture tests are pure AST checks and run everywhere. |

**Why Core semantics are unchanged:** this is packaging metadata only. Core imports nothing from the GUI and gains no runtime dependency.

---

## 10. Implementation Phases

| Phase | Content | Exit criteria |
|---|---|---|
| **C1** | v1.0.1 Core bugfix: CI-1, CI-2, CI-3 on `release/1.0.x` (Core Issues doc §6) | 176 + new tests pass; 10/10 golden bytes identical; CI-1 Artist Import evidence recorded |
| **P1** | §9.0 regression net → G2 → G1 (Core integration, no GUI yet) | All Core tests unchanged and passing; `test_app`, `test_contract`, `test_golden_parity` pass; byte parity CLI == app == golden |
| **P2** | G5 + GUI skeleton (`tracker_tool_gui`), offscreen test harness, architecture import test | `tracker-tool-gui` launches; architecture test passes |
| **P3** | Single-source workflow (§6, §7, §8) | GUI tests (§12) pass; GUI output byte-equal to the CLI for every golden |
| **P4** | PFTrack source-set workflow | Same as P3; CI-11 decided beforehand |
| **P5** | Error and validation UX polish, Copy diagnostics, preferences | — |
| **P6** | Artist smoke test of GUI-produced files in real 3DE R5 / PFTrack 2017 / SynthEyes 2304 | Recorded as Artist Import evidence, not as a GUI test result |
| **P7** | Packaging (§13) on a clean Windows machine without Python | — |

C1 and P1 run strictly in sequence (D8): **C1 → tag v1.0.1 → P1**.

---

## 11. Branch and Baseline Handling

```text
v1.0.0 (79fd42d, immutable)
 ├── release/1.0.x   CI-1/2/3, regression tests, REL-1, CI workflow, coverage matrix
 │                   → (CI-13 fix, A1–A6) → tag v1.0.1      [pushed; not released]
 ├── gui/develop     GUI handoff docs, CI workflow (cherry-picked), GUI skeleton (P2 prep)
 │                   Core code identical to v1.0.0
 └── main            local f72e44e (not pushed; origin/main = 79fd42d)
```

### Integration order (D8, D9)

1. While v1.0.1 is open, `gui/develop` holds only GUI preparation work. It does not touch Core code, so Core is identical to `v1.0.0`.
2. After `v1.0.1` is tagged, **merge** the tag into `gui/develop`. This is a normal merge, with no rebase of published history. The CI workflow commit was cherry-picked with identical content, so it merges cleanly.
3. Cherry-pick `f72e44e` onto `gui/develop` as its own commit.
4. Then G2 → G1 (P1), and wire the GUI to `tracker_tool.app` / `tracker_tool.contract`.

Until step 2, the GUI's Core baseline is `v1.0.0`. It is never described as v1.0.1.

### `f72e44e` (local refactor on `main`)

- It deduplicates the ShotConfig and frame-range validation blocks in `conversion.py`.
- Same validation order and same error codes; 176 tests pass on both commits.
- **Decision (2026-10-09):** not part of v1.0.1. It is cherry-picked onto the GUI branch before G2, after v1.0.1 is merged in. Without it, G2 would have to replace duplicated formal-code literals in two copies of the same block (27 occurrences instead of 21).

---

## 12. GUI Test Plan (summary)

pytest-qt with `QT_QPA_PLATFORM=offscreen`:

1. **Golden parity through the GUI:** each golden run via the GUI worker produces bytes equal to the CLI output and to `validation/outputs`.
2. **Formal codes:** each formal code reachable from the GUI is shown as **FAIL — `<CODE>`**. `SAME_SOURCE` is covered by Core and app tests, because the GUI disables that target.
3. **Non-contract errors:** a non-contract `ValueError` is shown verbatim. A non-`ValueError` is shown as "Unexpected Core failure".
4. **Failure leaves output untouched:** an existing output file is byte-identical after a failed GUI conversion.
5. **Field mapping:** empty field → `None`; non-integer text cannot be submitted; "Unknown" end frame → `None`.
6. **Target disabling:** the Target entry equal to the Source is disabled; changing the Source resets a now-invalid Target to "Select…"; in source-set mode the PFTRACK_2017 target is disabled.
7. **PFTrack role:** with no role selected, Convert is disabled; there is no default role.
8. **Architecture:** `tracker_tool_gui` imports only `tracker_tool.app`, `tracker_tool.contract`, and `tracker_tool.config`, and contains no contract string literals.
9. **Worker lifecycle:** busy state set and cleared; the form is re-enabled after both success and failure.
10. **Preferences:** ShotConfig values are not restored from preferences.

---

## 13. Packaging and Deployment Risks

| Risk | Mitigation |
|---|---|
| Artists have no Python or uv | PyInstaller one-folder build (~150 MB) from the locked environment |
| Antivirus false positives on PyInstaller output; unsigned executable | Code signing; test on a production workstation image |
| Missing Qt platform plugin in the bundle | Smoke-launch the frozen build in CI and on a clean machine |
| Non-ASCII paths (e.g. Chinese directory names) and UNC / network drives | Explicit tests; check how `Path.resolve()` behaves for the collision check on mapped drives |
| Newline and encoding drift if anything other than `app` writes files | Only `app` writes; parity tests enforce it |
| PySide6 version drift | Pin a floor in the extra and lock in `uv.lock` |
| GUI version vs Core version display | Depends on REL-1 being resolved |

---

## 14. Open Decisions Needed Before Execution

1. Execution order: C1 (v1.0.1) then P1 (recommended), or in parallel.
2. `f72e44e`: cherry-pick before G2 (recommended), or drop.
3. CI-1 grammar details (header variants, blank-line strictness) — Core Issues §1.
4. Whether CI-5 and CI-7 join v1.0.1.
5. CI-11 definition (required before P4).
