# Core Issues Found During GUI Architecture Review

Status (2026-10-10):

- **Released in v1.0.1:** CI-1, CI-2, CI-3, CI-12, and CI-13 (option C2, conservative input guard).
  - Release: https://github.com/PEI-YING-1122/tracker-tool/releases/tag/v1.0.1 (tag `v1.0.1` → `ec17fb4`).
  - Release records: `validation/COVERAGE_MATRIX_v1.0.1.md`, `validation/RELEASE_READINESS_v1.0.1.md`.
- **Still open, tracked as GitHub issues:** CI-4 (#4), CI-6 (#5), CI-11 (#3), hardening CI-5 / CI-7 and deferred CI-8 / CI-9 / CI-10 (#6), validation record gaps (#7), SPEC-4 (#9).
- Sections §1–§8 below are the original findings and decisions in chronological order. Status statements inside them reflect the time they were written.

Production files are referred to by case ID only. This repository is public.

```text
Baseline under review : v1.0.0 tag → 79fd42d
How it was verified   : `git archive v1.0.0` exported to a scratch directory and executed in isolation
                        (not the working tree, which is main f72e44e)
Core tests on v1.0.0  : 176 passed
Golden byte parity    : 10/10 validation/outputs/* reproduced byte-for-byte by cli.main on Windows
                        (8 of the 10 have a recorded Artist Import result; see DOC-1)
Review date           : 2026-10-09
```

Rules applied:

- Every issue was reproduced **without any GUI**, by calling Core directly.
- The GUI will **not** compensate for any of these issues. It will not strip headers, preprocess input, rename, trim, or clean up anything.
- Classification follows `docs/CORE_V1_HANDOFF.md` §9–10.

---

## 0. Summary and Priority

The priority below is the project owner's decision of 2026-10-09.

| ID | Priority | Classification | One line |
|---|---|---|---|
| **CI-1** | **P0** | Core defect: implementation ≠ released spec | PFTrack reader rejects every real PFTrack 2017 export |
| **CI-2** | **P0** | Core defect: Error Contract (exception type) | Malformed 3DE / PFTrack input raises `IndexError`, not `ValueError` |
| **CI-3** | **P0** | Core defect: 3DE writer violates the 3DE whitespace contract | 3DE writer emits names with leading/trailing whitespace |
| CI-5 | P1 hardening | Writer guard missing | PFTrack writer emits names containing `"` |
| CI-7 | P1 hardening | Input decoding | UTF-8 BOM input fails with a raw Python message |
| CI-4 | Validate first | Unverified native compatibility | 3DE / PFTrack writers can emit scientific notation |
| CI-6 | Define first | Spec gap | Duplicate track names inside one PFTrack file |
| CI-11 | Define first (new) | Spec gap | PFTrack source set accepts a zero-track AutoTrack or UserTrack file |
| CI-8 | Deferred | CLI leniency | `--pftrack-source-role` is ignored for non-PFTrack sources |
| CI-9 | Deferred | Reader leniency | 3DE reader accepts indented observation rows |
| CI-10 | Deferred | Check order | `FOO→FOO` reports SAME_SOURCE before UNSUPPORTED |

Spec, release, and backlog items that are not code defects are listed in §5.

Probe scripts used for this review: `probe_core.py`, `evidence_v100.py`. They were kept outside the repository and can be added under `tools/` on request.

---

## 1. CI-1 — PFTrack 2017 reader rejects real PFTrack 2017 exports (P0)

### Classification

Core defect: the released implementation does not match the released specification. The specification also under-specifies the exact blank-line layout.

### Specification

- `docs/ADAPTER_PFTRACK_2017.md` §2 documents the verified native grammar **including** the header:
  ```text
  # "Name"
  # clipNumber
  # frameCount
  # frame, xpos, ypos, similarity, zdepth
  ```
- §15: the strict parser must follow the verified native grammar.
- `docs/VALIDATION_CONTRACT.md` §7: native grammar includes the exact whitespace and newline layout.

### Evidence: real PFTrack 2017 exports

Eleven real PFTrack exports were found in the local production test archive, which is not part of this repository. The released reader **rejects all eleven**.

| Export (case ID) | Tracks | Rows |
|---|---|---|
| Test 08 AutoTrack export | 7 | 339 |
| Test 08 UserTrack export | 7 | 325 |
| Test 03 PFTrack export | 9 | 146 |
| Production export P-1 | 32 | 2080 |
| … 7 more (see `PROJECT_DOCUMENT_INDEX.md` §3) | | |

The first two files match the Test 08 counts in `INTERCHANGE_MASTER.md` §17 exactly (AutoTrack 7 / 339, UserTrack 7 / 325). They are the Test 08 source files.

Layout observed in **all** eleven files:

```text
line 1-4   "#" header. Line 4 has two variants:
             "# frame, xpos, ypos, similarity, zdepth"   (10 files)
             "# frame, xpos, ypos, similarity"           (1 file: Test 08 AutoTrack/UserTrack set)
then       exactly one blank line before EVERY track block, including the first
           (number of blank lines == number of tracks; no blank line anywhere else)
rows       always 4 numeric columns (frame xpos ypos similarity), even when the header mentions zdepth
newline    CRLF
encoding   no BOM
EOF        no trailing blank line
```

### Evidence gap: Test 08 was not run with the released reader

The Test 08 PFTrack-source evidence was produced by the historical script `convert_test08.py`, kept outside this repository. That script:

- reads with `utf-8-sig`
- skips lines starting with `#`
- skips blank lines
- strips each line

The released `read_pftrack_tracks` has **never** read a real PFTrack export. The PFTrack goldens in `validation/inputs/` are synthetic, headerless, and have no blank lines.

The PFTrack **writer** is not affected: its output passed real PFTrack 2017 import (`validation/README.md`).

### Minimal reproduction

```python
from tracker_tool.adapters.pftrack import read_pftrack_tracks

real_layout = (
    '# "Name"\n# clipNumber\n# frameCount\n'
    '# frame, xpos, ypos, similarity, zdepth\n'
    '\n'
    '"Tracker0001"\n1\n1\n1001 1500.250000 1200.500000 1.000000\n'
    '\n'
    '"Tracker0002"\n1\n1\n1001 10.0 20.0 1.000000\n'
)
read_pftrack_tracks(real_layout, "AUTOTRACK")
# v1.0.0 → ValueError: Invalid PFTrack track name
```

Real file through the CLI:

```powershell
uv run tracker-tool convert --source PFTRACK_2017 --target 3DE_R5 `
  --input <Test 08 AutoTrack export> `
  --output out_3de.txt --width 3424 --height 2202 --start-frame 1001 --pftrack-source-role AUTOTRACK
# v1.0.0 → ValueError: Invalid PFTrack track name   (no output written)
```

Removing only the header is **not** enough. Diagnostic only, not a proposed workaround: with the 4 header lines and the first blank line removed, 10 of 11 files still fail with the same error at the blank line before the second track block.

### Actual vs expected

| | v1.0.0 actual | Expected (pending spec confirmation) |
|---|---|---|
| Real export with header + blank-line separators | `ValueError: Invalid PFTrack track name` | Parsed. Canonical result is identical to the same tracks written without header and blank lines |
| Header content | n/a | Not promoted to Canonical; not used to infer anything |
| Header line-4 variants | n/a | Both observed variants accepted. Any other header text: **open question** |
| Blank lines | Rejected everywhere | Accepted exactly as observed (one before each block). Blank lines elsewhere (inside a block, between rows, multiple in a row): **open question**. Recommendation: reject, per VALIDATION_CONTRACT §7 "no normalization then PASS" |
| Headerless, blank-line-free input (current goldens) | Accepted | Still accepted, with byte-identical conversion output |
| Invented flat-row grammar (ADAPTER_PFTRACK §3) | Rejected | Still rejected |
| BOM | Rejected (CI-7) | Unchanged by CI-1. No observed export has a BOM |

### Affected paths

| Path | Affected |
|---|---|
| `convert` PFTRACK_2017 (AUTOTRACK / USERTRACK) → 3DE_R5 | **Yes** |
| `convert` PFTRACK_2017 (AUTOTRACK / USERTRACK) → SYNTHEYES_2304 | **Yes** |
| `convert-pftrack-source-set` → 3DE_R5 / SYNTHEYES_2304 | **Yes** (both inputs) |
| Round-trip validation with PFTrack as the real-software export (VALIDATION_CONTRACT §9) | **Yes**: the reader cannot read the real export |
| Any path with PFTrack as **target** (writer) | No |
| 3DE / SynthEyes source paths | No |

**4 of the 8 released conversion paths (2 single-source PFTrack directions × both roles, plus both source-set directions) are unusable on real data.**

### GUI impact

PFTrack-source workflows in the GUI will show the Core error unchanged until CI-1 is fixed. The GUI will not strip headers.

### Fix scope note (for the Core decision, not executed)

- Reader-only change: `src/tracker_tool/adapters/pftrack/reader.py`. No change to the writer, Canonical, conversion orchestration, or Error Contract.
- Regression requirement: the 10 existing golden outputs must stay byte-identical, and all 176 tests must pass.
- New evidence:
  - the Test 08 real exports become reader goldens (expected 7 / 339 and 7 / 325; source set 14 / 664);
  - outputs generated from them by the fixed Core need **real 3DE R5 and SynthEyes 2304 Artist Import** before being recorded in `validation/README.md`.

---

## 2. CI-2 — Malformed native input raises non-`ValueError` exceptions (P0)

### Classification

Core defect against the Error Contract.

`INTERCHANGE_MASTER.md` § "Error Contract" says internal reader, writer, and canonical errors use descriptive `ValueError` messages. The tests and the CLI contract (`pytest.raises(ValueError)`) rely on that type. Some malformed inputs instead raise `IndexError`. Any caller that follows the documented contract and catches `ValueError` will crash.

### Minimal reproduction

```python
from tracker_tool.config import ShotConfig
from tracker_tool.conversion import convert_tracks

cfg = lambda s, t: ShotConfig(1920, 1080, 1001, None, s, t)

convert_tracks("", cfg("3DE_R5", "PFTRACK_2017"))
# → IndexError: list index out of range

convert_tracks("2\nA\n0\n1\n1 1 1\n", cfg("3DE_R5", "PFTRACK_2017"))     # 2nd track missing
# → IndexError: list index out of range

convert_tracks('"A"\n', cfg("PFTRACK_2017", "3DE_R5"), pftrack_source_role="AUTOTRACK")   # clip line missing
# → IndexError: list index out of range
```

Truncation fuzz: every line-prefix of each golden input was parsed.

| Reader | IndexError | Descriptive ValueError | Accepted (valid shorter file) |
|---|---|---|---|
| 3DE_R5 | **7** | 7 | 0 |
| PFTRACK_2017 | **4** | 7 | 2 |
| SYNTHEYES_2304 | 0 | 0 | 7 |

### Secondary: CI-2b, message quality only

These raise the correct type (`ValueError`), but the message is Python-internal. Message wording is **not** part of the v1 contract, so CI-2b is not a contract violation. It is recorded because artists will see these messages in the GUI.

| Input | Message |
|---|---|
| 3DE row with 2 fields | `not enough values to unpack (expected 3, got 2)` |
| 3DE non-integer track count | `invalid literal for int() with base 10: 'x'` |
| 3DE non-numeric X | `could not convert string to float: 'a'` |
| PFTrack row with 3 fields | `not enough values to unpack (expected 4, got 3)` |
| PFTrack non-integer frame count | `invalid literal for int() with base 10: 'x'` |

### Actual vs expected

| | v1.0.0 actual | Expected |
|---|---|---|
| Truncated / empty 3DE input | `IndexError` | `ValueError` with descriptive message |
| Truncated PFTrack block | `IndexError` | `ValueError` with descriptive message |
| No new formal error code | — | Correct: these remain non-contract descriptive messages |
| Valid inputs | Accepted | Unchanged, byte-identical output |
| Output file on failure | Not written (exception raised before write) | Unchanged |

### Affected paths

- All `3DE_R5` source paths.
- All `PFTRACK_2017` source paths, single and source set.
- `SYNTHEYES_2304` reader is not affected.

### GUI impact

The GUI catches all exceptions and shows a non-`ValueError` as "Unexpected Core failure", with a traceback for reporting. That is presentation only, not compensation.

---

## 3. CI-3 — 3DE writer emits track names that violate the 3DE whitespace contract (P0)

### Classification

Core defect: the target writer produces native output that violates the verified target grammar and reports success.

### Specification

- `ADAPTER_3DE_R5.md` §3 forbids leading or trailing spaces on structural lines. The name line is a structural line, and the released 3DE reader enforces this.
- `ADAPTER_3DE_R5.md` §8 requires exact preservation of the name.
- `INTERCHANGE_MASTER.md` §14 forbids automatic whitespace normalization.

Preservation and validity cannot both be met for such names. The writer must therefore **reject**, as the SynthEyes writer already does for whitespace.

### Minimal reproduction

```python
pf = '" Point"\n1\n1\n1001 1 2 1.000000\n'          # PFTrack name with a leading space
out = convert_tracks(pf, cfg("PFTRACK_2017", "3DE_R5"), pftrack_source_role="USERTRACK")
# v1.0.0 → succeeds; out == '1\n Point\n0\n1\n1 1.0 2.0\n'

from tracker_tool.adapters.threed import read_3de_tracks
read_3de_tracks(out, cfg("3DE_R5", "PFTRACK_2017"))
# → ValueError: 3DE native structural line has leading or trailing whitespace
```

| Canonical `track_name` (from PFTrack) | → 3DE_R5 v1.0.0 | Core's own 3DE reader on that output | → SYNTHEYES_2304 v1.0.0 |
|---|---|---|---|
| `" Point"` | success, line `' Point'` | rejects | rejects (correct) |
| `"Point "` | success, line `'Point '` | rejects | rejects (correct) |
| `"  "` | success, line `'  '` | rejects | rejects (correct) |
| `"\tPoint"` | success, line `'\tPoint'` | rejects | rejects (correct) |
| `"Point 001"` (control) | success | accepts | rejects (correct) |

### Actual vs expected

| | v1.0.0 actual | Expected |
|---|---|---|
| Name with leading or trailing whitespace → 3DE_R5 | Success; output violates the 3DE contract | Descriptive `ValueError` from the 3DE writer; no trim or rename; no output written |
| Name with internal whitespace (`Point 001`) → 3DE_R5 | Success | **Unchanged by CI-3.** Real 3DE R5 acceptance of internal spaces is unverified; add to the CI-4 validation list |

### Affected paths

- PFTRACK_2017 → 3DE_R5, both roles.
- PFTrack source set → 3DE_R5.
- 3DE and SynthEyes sources cannot produce such names: their readers reject or split them.

---

## 4. Lower-priority issues

### CI-5 — PFTrack writer does not guard `"` in track names (P1)

```python
convert_tracks('1\nA"B\n0\n1\n1 1 2\n', cfg("3DE_R5", "PFTRACK_2017"))
# → '"A"B"\n1\n1\n1001 1.0 2.0 1.000000\n'
```

The quoting grammar for embedded `"` is unverified in PFTrack 2017.

Expected: reject with a descriptive error, unless real PFTrack import proves an escaping rule.

Affected: 3DE_R5 → PFTRACK_2017 and SYNTHEYES_2304 → PFTRACK_2017. SynthEyes names can contain `"`, since only whitespace splits them.

### CI-7 — UTF-8 BOM input fails with a raw Python message (P1)

The CLI reads with `encoding="utf-8"`, so a BOM stays in the text.

```text
3DE file starting with EF BB BF → ValueError: invalid literal for int() with base 10: '\ufeff1'
```

None of the 11 real PFTrack exports has a BOM. The historical Test 08 script used `utf-8-sig`. The behavior must be decided: accept a BOM as an encoding artifact, or reject it with a descriptive message.

This lives in file I/O (`cli.py`, or `app.py` after G1), not in a reader.

### CI-4 — Scientific notation in 3DE / PFTrack writer output (validate first)

The writers format floats with Python `str(float)`:

```text
SYNTHEYES_2304 u=-0.99999999, W=1920 → x = 9.600000048237689e-06
  3DE row:     "1 9.600000048237689e-06 540.0"
  PFTrack row: "1001 9.600000048237689e-06 540.0 1.000000"
```

This triggers for |x| < 1e-4 (non-zero) or |x| ≥ 1e16. Whether 3DE R5 and PFTrack 2017 accept it is **unverified**. Do not classify it as a bug until a Native Import Validation answers that.

Proposed validation set:
- tiny positive and negative values
- `-0.0`
- internal-space names for 3DE (from CI-3)

### CI-6 — Duplicate track names inside one PFTrack file (define first)

```text
'"A"…"A"…' in one AUTOTRACK file → ValueError: Canonical track_id must be unique
```

This happens because the PFTrack `track_id` is `role::name`. 3DE explicitly allows same-name tracks and makes them unique by block index. PFTrack semantics are undefined.

### CI-11 — PFTrack source set accepts a zero-track input (define first, new)

```python
convert_pftrack_source_set("", '"A"\n1\n1\n1001 1 2 1.0\n', cfg("PFTRACK_2017", "3DE_R5"))
# → succeeds; output contains only the UserTrack tracks
```

A single-source conversion of an empty file fails ("Canonical track collection must not be empty"). The source set accepts an empty member and converts only the other one.

`ADAPTER_PFTRACK_2017.md` §10 requires each member to "PASS independently" but does not define whether zero tracks is a PASS. Production risk: an artist picks a wrong or empty AutoTrack file and gets partial output with no warning.

**Recommendation:** decide this before GUI P4 (the source-set workflow).

### Deferred

| ID | Reproduction | Note |
|---|---|---|
| CI-8 | `convert --source 3DE_R5 … --pftrack-source-role BOGUS` → exit 0 | GUI shows the role only for PFTrack, so the GUI does not hit this |
| CI-9 | `"1\nA\n0\n1\n   1 1 2\n"` accepted | Reader leniency only; no effect on output |
| CI-10 | `ShotConfig(..., "FOO", "FOO")` → `SAME_SOURCE_CONVERSION_NOT_ALLOWED` | GUI offers only valid IDs |

---

## 5. Spec, release, and backlog items (not code defects)

| ID | Item |
|---|---|
| SPEC-1 | `PROJECT_GOAL.md` §3.2 and `AGENTS.md` §10 list Read-only Analysis as v1 scope; released Core has none. **Decision 2026-10-09: Analysis is not in GUI v1; kept as backlog.** |
| SPEC-2 | `VALIDATION_CONTRACT.md` §13 lists hard-failure codes that Core does not emit. `INTERCHANGE_MASTER.md` "Error Contract" (7 codes) governs Core. The relationship should be stated explicitly. |
| SPEC-3 | `ADAPTER_PFTRACK_2017.md` §2 should state the observed blank-line layout and both header variants (input to CI-1). |
| REL-1 | `pyproject.toml` version `0.1.0` ≠ tag `v1.0.0`. Separate release/versioning issue; **not** bundled with GUI commits. |
| REL-2 | `main` has one local, unpushed commit `f72e44e` (non-semantic refactor of `conversion.py`); `origin/main` = `v1.0.0`. Needs an explicit decision (see the GUI plan §11). |
| DOC-1 | `validation/outputs/pftrack_usertrack_to_{3de,syntheyes}_golden_01.txt` and their input exist, but `validation/README.md` has no entry for them (no "Golden 04"). Their Artist Import status is undocumented. Only 8 of the 10 golden outputs have a recorded import result. |
| TEST-1 | No automated test references `validation/`. Golden byte parity is not enforced by the suite. It will be added with G1. |

---

## 6. v1.0.1 Recommendation

**Recommendation: yes, release v1.0.1 = CI-1 + CI-2 + CI-3.**

### Why a bugfix release is warranted

- CI-1 makes every PFTrack-source direction unusable on real exports. That is half of the released conversion matrix, and it contradicts the released adapter spec.
- CI-3 reports success while writing a 3DE file that violates the verified 3DE grammar.
- CI-2 breaks the documented exception contract that every caller, including the GUI and the CLI, relies on.

### Why it qualifies as a patch release

- All three changes are adapter-local:
  - `adapters/pftrack/reader.py`
  - `adapters/threed/reader.py`
  - `adapters/threed/writer.py`
- No change to the Canonical model, `conversion.py`, ShotConfig, the 7 formal error codes, CLI arguments, or any writer output for input that v1.0.0 accepted **and** that satisfies the spec.
- Behavior changes are limited to:
  - (a) accepting spec-documented input that was wrongly rejected (CI-1);
  - (b) a different exception type on input that already failed (CI-2);
  - (c) rejecting output that already violated the spec (CI-3).

### Not included in v1.0.1

- CI-4, CI-6, CI-11: need validation or definition first.
- CI-5, CI-7: P1. They can join v1.0.1 if decided in time; they are not required.
- `f72e44e`: a refactor, not a fix. Keep the bugfix diff minimal.
- G1 / G2 / G5: new public API, so they belong to v1.1.0.
- REL-1: can be handled together with the v1.0.1 tag, as its own commit.

### Proposed procedure

1. Create branch `release/1.0.x` from tag `v1.0.0`.
2. Add one commit per issue, each with tests written first.
3. Add a golden byte-parity test (TEST-1) as the first commit, so that all three fixes are checked against the 10 golden outputs.
4. Release gate:
   - all 176 existing tests pass;
   - new tests pass;
   - 10/10 golden outputs are byte-identical;
   - for CI-1, Artist Import in real 3DE R5 and SynthEyes 2304 of outputs converted from the Test 08 real PFTrack exports, recorded in `validation/README.md`.
5. Tag `v1.0.1`. `v1.0.0` stays immutable.
6. Merge `release/1.0.x` into the development line.

---

## 7. Decisions and Status (2026-10-09, second review)

### Decisions

| Item | Decision |
|---|---|
| Order | Sequential: `v1.0.0` → `release/1.0.x` → CI-1/2/3 → regression and golden tests → Native Import Validation → tag `v1.0.1` → GUI development. No GUI work in parallel with the Core bugfix. |
| v1.0.1 scope | CI-1, CI-2, CI-3 only. Pure bugfix release. |
| `f72e44e` | Not in v1.0.1. Cherry-picked onto the GUI branch (created from `v1.0.1`) before G2. |
| CI-1 grammar | Both verified header variants are supported. Allowed blank lines: the separator after the verified header, and separators between track blocks. A trailing blank line would be allowed only if real exports produced one; none do. Rejected: blank lines that break a block, unknown headers, headers in the middle of the file, any other unverified structure. Comment and blank lines are not skipped generically. |
| CI-5, CI-7 | Not in v1.0.1. Hardening backlog. Re-prioritize only if production native files are found to be affected. |
| CI-11 | **Core contract decision:** in a PFTrack source set, each explicitly specified member file must yield at least 1 track. Single source with 0 tracks → FAIL (already the case). AutoTrack with 0 tracks → FAIL. UserTrack with 0 tracks → FAIL. A 0-track member is never silently ignored. **Not in v1.0.1.** To be implemented as its own Core change before GUI P4. `ADAPTER_PFTRACK_2017.md` §10 will be updated together with that implementation, so the spec never describes behavior the released code does not have. |
| Regression tests | Part of v1.0.1 itself, written before the fixes. |

### Status on `release/1.0.x` (from `v1.0.0`, not pushed, not tagged)

| Commit | Content |
|---|---|
| `657817d` | Released golden regression: 10 goldens, conversion text and CLI bytes. Passes on unmodified v1.0.0. |
| `75e969a` | CI-2 fix + truncation regression (every line and every character prefix of each golden input). |
| `ebbc975` | CI-1 fix + PFTrack native export regression (accepted layouts, 16 rejected layouts, CRLF CLI path, opt-in real-export test) + ADAPTER_PFTRACK_2017 §2 layout contract. |
| `6657822` | CI-3 fix + name regression (rejection, round-trip of accepted names, CLI writes no output) + ADAPTER_3DE_R5 §8 representability rule. |

Verification:

- 267 passed, 1 skipped (the opt-in real-export test). Same result in a fresh clone with `core.autocrlf=false`.
- The opt-in real-export test passes on all 11 real PFTrack 2017 exports.
- 10/10 released goldens are byte-identical.
- Source diff `v1.0.0..release/1.0.x` is limited to `adapters/pftrack/reader.py`, `adapters/threed/reader.py`, and `adapters/threed/writer.py`.

Each fix was written test-first. The new tests failed before the fix:

| Issue | Failed before fix | Passed before fix |
|---|---|---|
| CI-2 | 19 | 2 (SynthEyes) |
| CI-1 | 13 accept tests | 16 reject tests (guards against a permissive parser) |
| CI-3 | 17 | 4 round-trip controls |

**Release gate still open:** Artist Import in 3DE R5 and SynthEyes 2304 of outputs converted from real PFTrack 2017 exports. The candidate package is kept in a local validation package. It is kept outside the repository because the repository is public and the files contain production data.

### Found during v1.0.1 work

| ID | Item |
|---|---|
| TEST-2 | Goldens are stored with LF in Git and checked out as CRLF only through the system `core.autocrlf=true`. There is no `.gitattributes`. The bytes that passed Artist Import (CRLF) are therefore not the bytes stored in Git. The new golden test compares content plus the CLI's platform newline, so it does not depend on checkout settings. A `.gitattributes` policy for `validation/` is a separate decision. |

---

## 8. Found During the Native Import Coverage Review (2026-10-09)

Both defects are present in v1.0.0 and in `release/1.0.x`. Neither is fixed. Native semantics are **not** guessed; artist evidence is requested first (Coverage Matrix A5, A6).

### CI-12 — 3DE reader rejects real 3DE R5 exports with a non-zero field after the track name

- **Specification:** `ADAPTER_3DE_R5.md` §4 verifies the value `0` and leaves the meaning unconfirmed. §10 says the reader checks the "Static Field".
- **Evidence:** 7 real 3DE exports were checked. Two of them contain `3`:
  - one production export: 15 of 43 points have `3`, the rest `0`;
  - Test 04 3DE round-trip export: 9 of 9 points have `3`.
- **Reproduction:**
  ```python
  convert_tracks("1\nTracker0001\n3\n1\n1 1500.25 1200.5\n",
                 ShotConfig(4608, 1757, 1001, None, "3DE_R5", "PFTRACK_2017"))
  # → ValueError: Unexpected 3DE static field
  ```
- **Affected paths:** 3DE_R5 → PFTRACK_2017 and 3DE_R5 → SYNTHEYES_2304.
- **Damage:** rejection only; never wrong output.
- **Open question (A5):** what the field means in 3DE R5 (point colour is suspected but **not verified**), and therefore which values the reader may accept. The value would stay out of Canonical either way (Color is v1-excluded), and the writer keeps emitting `0`.

### CI-13 — SynthEyes reader turns the `#` first row of real exports into a track

- **Specification:** `ADAPTER_SYNTHEYES_2304.md` §8 and §10. "Tracker name valid" is not defined for `#`.
- **Evidence:** 5 of 7 real SynthEyes exports start with `# 0 0.000000 0.000000 15`.
  - All 5 are SynthEyes re-exports, including the Test 02, 04, 07, and 08 round-trip exports.
  - The 2 files without it are copies of one original artist export.
  - Historical scripts skipped `#` lines. The released reader does not.
- **Reproduction:**
  ```python
  convert_tracks("# 0 0.000000 0.000000 15\nTracker0001 0 -0.250000000 -0.500000000 15\n",
                 ShotConfig(4608, 1757, 1001, None, "SYNTHEYES_2304", "3DE_R5"))
  # → '2\n#\n0\n1\n1 2304.0 878.5\nTracker0001\n...'   (extra point "#" at image centre)
  ```
- **Affected paths:** SYNTHEYES_2304 → 3DE_R5 and SYNTHEYES_2304 → PFTRACK_2017.
- **Round-trip validation (VALIDATION_CONTRACT §9) is also affected:** reading the Test 08 SynthEyes round-trip export gives 15 tracks / 665 obs instead of 14 / 664.
- **Damage:** silent wrong output. An extra track is created, which contradicts 100% PRESERVE and "no fabricated observation".
- **Open question (A6):** what the row is. It might be a real tracker named `#`, or an exporter artifact. The answer decides the fix: **reject** an unverified structure, or **recognize** a verified non-track row. It must not be skipped generically as a comment.

### Recommendation for v1.0.1 scope (decision pending)

- **CI-13: block v1.0.1.** It produces wrong target data silently on two officially supported paths, and the release is meant to be the first one usable on real exports.
- **CI-12: include in v1.0.1 if A5 resolves the semantics quickly.** Otherwise ship it as a documented known limitation and fix it in v1.0.2. It never produces wrong output.

### Also found

- **TEST-3:** E-A records (`validation/README.md`) lack import dates, software build numbers, the artist, and the Editability check (VALIDATION_CONTRACT §8).
