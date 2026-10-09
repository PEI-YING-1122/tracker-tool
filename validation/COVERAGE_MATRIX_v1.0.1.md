# Native Import Validation Coverage — v1.0.1 Release Candidate

```text
Candidate : release/1.0.x (branched from v1.0.0 / 79fd42d)
Status    : NOT RELEASED. Release gate open.
Blocker   : CI-13 (SynthEyes "#" row) must be fixed and regression-tested
Pending   : Artist actions A1–A6 (section 5)
```

**Automated test PASS is not Native Import PASS.** This document labels every kind of evidence separately. Only **E-A** and **E-F** are Artist Imports in the real target software.

Production native files used for this review are kept outside this public repository. They are referred to by case ID only.

---

## 1. Evidence Types

| ID | Evidence | Kind |
|---|---|---|
| **E-A** | Artist Import PASS of released-Core output, recorded in `validation/README.md` (2026-09-20). The inputs are **synthetic** goldens. | **Artist Import** |
| **E-B** | `tests/test_release_goldens.py`: the candidate reproduces every E-A output byte-for-byte. | Automated regression |
| **E-C** | The released reader parses **real** native exports offline (production files, not in this repository). | Automated / offline parse |
| **E-D** | Historical real-shot Tests 01–08 (2026-08-29/30), Artist Import PASS per `docs/INTERCHANGE_MASTER.md` §17. They were produced by pre-Core scripts with a different output grammar, and Tests 01–07 renamed tracks. | Supporting only. Not evidence for released code |
| **E-E** | `tests/test_pftrack_source_role_output.py`: PFTrack AUTOTRACK and USERTRACK produce byte-identical output. | **Automated equivalence**, not an import |
| **E-F** | Artist Import of v1.0.1 candidate output generated from **real** native exports (actions A1–A4). | **Artist Import**, pending |

### Traceability of E-A

- **Recorded:**
  - input and output files are in this repository;
  - E-B reproduces the outputs exactly;
  - a per-check result exists in `validation/README.md`.
- **Not recorded:**
  - import date;
  - software build numbers;
  - the artist;
  - the **Editability** check required by `docs/VALIDATION_CONTRACT.md` §8.
- **Not recorded at all:** the two `pftrack_usertrack_*` outputs have no entry (DOC-1).
- **Line endings:** Git stores the goldens with LF; the imported files had CRLF (TEST-2). E-B compares content plus the CLI's platform newline.

---

## 2. Coverage Matrix

| # | Path | v1.0.0 Artist Import (E-A) | CI-1 / CI-2 / CI-3 effect | Real exports (E-C) | **v1.0.1 status** | Basis |
|---|---|---|---|---|---|---|
| 1 | 3DE → PFTrack | PASS, Golden 01 | CI-2: failure path only. Success-path code unchanged | 5 of 7 parse; 2 rejected (**CI-12**) | **Previously Verified** | E-A + E-B. Known limitation CI-12 (rejection, no wrong output) |
| 2 | 3DE → SynthEyes | PASS, Golden 01 | same as #1 | same as #1 | **Previously Verified** | E-A + E-B. Known limitation CI-12 |
| 3 | SynthEyes → 3DE | PASS, Golden 03 | CI-3 touches the 3DE writer; SynthEyes names cannot contain whitespace, so output is unchanged | 7 of 7 parse; **5 contain a `#` row that becomes an extra track (CI-13)** | **Previously Verified (format) — BLOCKED by CI-13** | E-A + E-B for the target format. Real-data correctness requires the CI-13 fix |
| 4 | SynthEyes → PFTrack | PASS, Golden 03 | none | same as #3 | **Previously Verified (format) — BLOCKED by CI-13** | same as #3 |
| 5 | PFTrack AutoTrack → 3DE | PASS, Golden 02 (synthetic headerless input) | **CI-1**, CI-2, CI-3 | v1.0.0: 0 of 11 parse; candidate: 11 of 11 | **Revalidation Required** | E-F: **A3** |
| 6 | PFTrack AutoTrack → SynthEyes | PASS, Golden 02 | CI-1, CI-2 | same as #5 | **Revalidation Required** | E-F: **A4** |
| 7 | PFTrack UserTrack → 3DE | **No record** (DOC-1) | CI-1, CI-2, CI-3 | same as #5 | **Not Verified (no Artist Import) — covered by Automated Equivalence** | E-E (automated) + A3 (artist, same output bytes). No separate import |
| 8 | PFTrack UserTrack → SynthEyes | **No record** (DOC-1) | CI-1, CI-2 | same as #5 | **Not Verified (no Artist Import) — covered by Automated Equivalence** | E-E (automated) + A4 (artist) |
| 9 | PFTrack Source Set → 3DE | PASS, Golden 05 (synthetic headerless) | CI-1, CI-2, CI-3 | real Test 08 set parses: 14 / 664 | **Revalidation Required** | E-F: **A1** |
| 10 | PFTrack Source Set → SynthEyes | PASS, Golden 05 | CI-1, CI-2 | same as #9 | **Revalidation Required** | E-F: **A2** |

### Why #1–#4 need no new import

Between v1.0.0 and the candidate:

- the only change on any success path is in the PFTrack reader;
- the 3DE reader change (CI-2) only affects input that already failed;
- the 3DE writer change (CI-3) only rejects names that no 3DE or SynthEyes source can produce;
- E-B confirms identical output bytes for every verified input.

The CI-13 fix will change the SynthEyes reader. Once it lands, #3 and #4 will be re-assessed in this matrix.

### Why #5, #6, #9, #10 need a new import even though the writers did not change

The reader now accepts the real PFTrack export layout, which released code never processed. No released-code output generated from a real PFTrack export has been imported yet. This is the CI-1 release gate.

### Supporting evidence (E-D, not counted as verification)

The candidate's output for the real inputs of historical Test 03 (PFTrack → 3DE) and Test 08 (Source Set → 3DE) equals the historically imported outputs in track names, frame sets, and coordinates (maximum difference 0.0 px). Number formatting differs, so the files are not byte-identical.

---

## 3. Prepared Artist Import Cases (E-F)

The files are kept in the validation package outside the repository (production data). Conversion was done with the candidate CLI.

| Action | Paths | Source | Header variant | Shot | Target | Expected |
|---|---|---|---|---|---|---|
| **A1** | #9 (+ UserTrack data, #7) | Test 08 AutoTrack + UserTrack exports | without zdepth | 3424×2202, start 1001 | 3DEqualizer R5 | 14 tracks / 664 observations |
| **A2** | #10 (+ #8) | same | without zdepth | same | SynthEyes 2304 | 14 tracks / 664 observations |
| **A3** | #5, #7 | Test 03 PFTrack export | with zdepth | 4608×1757, start 1001 | 3DEqualizer R5 | 9 tracks / 146 observations |
| **A4** | #6, #8 | same | with zdepth | same | SynthEyes 2304 | 9 tracks / 146 observations |

---

## 4. Core Defects Affecting Supported Paths

Both are present in v1.0.0 and in the candidate. Native semantics are not guessed; artist evidence comes first.

| ID | Paths | Problem | Damage | Release decision |
|---|---|---|---|---|
| **CI-13** | #3, #4 | Real SynthEyes 2304 re-exports can begin with `# 0 0.000000 0.000000 15`. The reader turns it into a Canonical track named `#`. | **Silent wrong output:** an extra point `#` at image centre | **v1.0.1 Release Blocker.** Fix after A6. Lines starting with `#` must not be ignored generically |
| **CI-12** | #1, #2 | The 3DE reader accepts only `0` in the field after the track name. Real 3DE R5 exports contain `3`. | Rejection only | Fix in v1.0.1 only if A5 shows it can be done without changing conversion semantics; otherwise Known Limitation with a risk assessment |

---

## 5. Artist Actions and Records

| ID | Software | Task |
|---|---|---|
| A1–A4 | 3DEqualizer R5 / SynthEyes 2304 | Import the prepared file and complete the record below |
| **A5** | 3DEqualizer R5 | Create 2D points that differ in one setting at a time (e.g. point colour), export 2D tracks with the production exporter, and report which setting changes the number after the point name and which values occur |
| **A6** | SynthEyes 2304 | Export Tracker 2-D Paths and report whether the scene contains a tracker named `#`, which exporter and options produce the `# 0 … 15` first row, and whether it appears in every export |

### Native Import record (to be completed by the artist)

| Case | Date | Software + build | Artist | Track count expected / observed | Observation count expected / observed | File Import | Track Identity | Frame Mapping | Point Position | Natural Gap | Editability | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | | 3DEqualizer R5 build: | | 14 / | 664 / | | | | | | | |
| A2 | | SynthEyes 2304 build: | | 14 / | 664 / | | | | | | | |
| A3 | | 3DEqualizer R5 build: | | 9 / | 146 / | | | | | | | |
| A4 | | SynthEyes 2304 build: | | 9 / | 146 / | | | | | | | |

### Evidence record for A5 / A6

| Case | Date | Software + build | Artist | Finding |
|---|---|---|---|---|
| A5 | | 3DEqualizer R5 build: | | |
| A6 | | SynthEyes 2304 build: | | |

---

## 6. Release Gate for v1.0.1

v1.0.1 may be tagged only when **all** of the following hold:

1. CI-13 is fixed and regression-tested, based on the A6 evidence.
2. CI-12 is either fixed (based on A5) or documented as a Known Limitation with a risk assessment.
3. The full test suite passes locally and in GitHub Actions (Windows and Linux).
4. A1–A4 are recorded as PASS in the table above.
5. If CI-13 changes SynthEyes reader output, the affected SynthEyes-source paths (#3, #4) are re-assessed here, and any required Artist Import is recorded.
6. `validation/README.md` gains the v1.0.1 Native Import records.
