# Native Import Validation Coverage — v1.0.1 Release Candidate

```text
Candidate : release/1.0.x (branched from v1.0.0 / 79fd42d)
Status    : NOT RELEASED. Release gate open.
Pending   : Artist Native Import A1–A4 (section 5)
            Owner confirmation of the CI-13 reclassification (section 4)
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
| **E-D** | Historical real-shot Tests 01–08 (2026-08-29/30), Artist Import and round-trip PASS per `docs/INTERCHANGE_MASTER.md` §17. They were produced by pre-Core scripts with a different output grammar, and Tests 01–07 renamed tracks. | Supporting only. Not evidence for released code |
| **E-E** | Automated equivalence proofs: PFTrack AUTOTRACK and USERTRACK give byte-identical output (`tests/test_pftrack_source_role_output.py`); 3DE static field `0` and `3` give byte-identical output (`tests/test_3de_static_field.py`, also checked on real exports). | **Automated equivalence**, not an import |
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

| # | Path | v1.0.0 Artist Import (E-A) | Candidate changes on this path | Real exports (E-C) | **v1.0.1 status** | Basis |
|---|---|---|---|---|---|---|
| 1 | 3DE → PFTrack | PASS, Golden 01 | CI-2 (failure path only). **CI-12:** the reader now also accepts the verified static field value `3` | v1.0.0: 4 of 6 parse. Candidate: 6 of 6 parse (see SPEC-4 for one file that still cannot convert, by specification) | **Previously Verified** | E-A + E-B. E-E: a `3` input converts byte-identically to the same data with `0`, on synthetic and real data. No new import |
| 2 | 3DE → SynthEyes | PASS, Golden 01 | same as #1 | same as #1 | **Previously Verified** | same as #1 |
| 3 | SynthEyes → 3DE | PASS, Golden 03 | None on the success path. CI-3 rejects only names a SynthEyes source cannot produce | 7 of 7 parse. 5 contain a real tracker named `#` (see CI-13; not a defect) | **Previously Verified** | E-A + E-B |
| 4 | SynthEyes → PFTrack | PASS, Golden 03 | none | same as #3 | **Previously Verified** | E-A + E-B |
| 5 | PFTrack AutoTrack → 3DE | PASS, Golden 02 (synthetic headerless input) | **CI-1**, CI-2, CI-3 | v1.0.0: 0 of 11 parse. Candidate: 11 of 11 | **Revalidation Required** | E-F: **A3** |
| 6 | PFTrack AutoTrack → SynthEyes | PASS, Golden 02 | CI-1, CI-2 | same as #5 | **Revalidation Required** | E-F: **A4** |
| 7 | PFTrack UserTrack → 3DE | **No record** (DOC-1) | CI-1, CI-2, CI-3 | same as #5 | **Not Verified (no Artist Import) — covered by Automated Equivalence** | E-E (automated) + A3 (artist, same output bytes). No separate import |
| 8 | PFTrack UserTrack → SynthEyes | **No record** (DOC-1) | CI-1, CI-2 | same as #5 | **Not Verified (no Artist Import) — covered by Automated Equivalence** | E-E (automated) + A4 (artist) |
| 9 | PFTrack Source Set → 3DE | PASS, Golden 05 (synthetic headerless) | CI-1, CI-2, CI-3 | real Test 08 set parses: 14 / 664 | **Revalidation Required** | E-F: **A1** |
| 10 | PFTrack Source Set → SynthEyes | PASS, Golden 05 | CI-1, CI-2 | same as #9 | **Revalidation Required** | E-F: **A2** |

### Why #1–#4 need no new import

- For every input v1.0.0 accepted, the candidate produces byte-identical output (E-B).
- CI-12 adds acceptance of one verified value of a field that is not Canonical data. The output for such input equals the output for the same data with `0` (E-E), which is the format E-A verified.
- CI-3 only rejects names that no 3DE or SynthEyes source can produce.

### Why #5, #6, #9, #10 need a new import even though the writers did not change

The PFTrack reader now accepts the real PFTrack export layout, which released code never processed. No released-code output generated from a real PFTrack export has been imported yet. This is the CI-1 release gate.

### Supporting evidence (E-D, not counted as verification)

The candidate's output for the real inputs of historical Test 03 (PFTrack → 3DE) and Test 08 (Source Set → 3DE) equals the historically imported outputs in track names, frame sets, and coordinates (maximum difference 0.0 px). Number formatting differs, so the files are not byte-identical.

---

## 3. Prepared Artist Import Cases (E-F)

The files are kept in the validation package outside the repository (production data). Conversion was done with the candidate CLI. CI-12 does not touch the PFTrack paths, so the prepared files remain valid.

| Action | Paths | Source | Header variant | Shot | Target | Expected |
|---|---|---|---|---|---|---|
| **A1** | #9 (+ UserTrack data, #7) | Test 08 AutoTrack + UserTrack exports | without zdepth | 3424×2202, start 1001 | 3DEqualizer R5 | 14 tracks / 664 observations |
| **A2** | #10 (+ #8) | same | without zdepth | same | SynthEyes 2304 | 14 tracks / 664 observations |
| **A3** | #5, #7 | Test 03 PFTrack export | with zdepth | 4608×1757, start 1001 | 3DEqualizer R5 | 9 tracks / 146 observations |
| **A4** | #6, #8 | same | with zdepth | same | SynthEyes 2304 | 9 tracks / 146 observations |

---

## 4. Native Format Findings (specification and evidence review, 2026-10-09)

Each finding was checked against the released specifications, the released implementation and tests, and the original exports and historical test records, **before** asking for any artist action.

### CI-12 — 3DE static field `3` → **FIXED** on release/1.0.x

| Question | Answer |
|---|---|
| Does the spec define the field and its legal values? | Partly. `ADAPTER_3DE_R5.md` §4 verified `0` for the writer, left the meaning unconfirmed, and did not list the values the reader may accept. §10 says only that the reader checks the field. **Specification gap.** |
| Does the released implementation violate the spec? | Not literally; it took the strictest reading (`== "0"`). That rejected genuine 3DE R5 output. |
| Is there enough evidence? | **Yes.** Real 3DE R5 exports contain `0` and `3`. Decisive: Test 04 and Test 06 both imported a file with `0` into 3DE R5 and re-exported it. Test 04 came back with `3` on every point, with identical names and frame sets and a coordinate difference ≤ 4.6e-13 px (historical round-trip: PRACTICALLY_LOSSLESS). Test 06 came back with `0`. The value is therefore a 3DE point attribute that does not affect observations. |
| Historical specification | The pre-Core 3DE exporter specification (2026-08-23, outside this repository) named the field `<POINT_COLOR_INTEGER>` and required only "color parses as integer". That supports the point-attribute reading, but it ranks below the released `ADAPTER_3DE_R5.md`, which deliberately calls it a static field of unconfirmed meaning. The same document's example also showed blank lines that later failed real 3DE import. So the reader accepts only the values with real-export evidence (`0`, `3`). Accepting any integer would be a Core semantics decision. |
| Classification | Native value needing explicit support (specification gap) |
| Safe without changing conversion semantics? | **Yes.** The reader accepts exactly `0` and `3`; any other value stays rejected until real-export evidence exists. The value is not Canonical (CANONICAL §14), the writer still emits `0`, and output for `3` input is byte-identical to output for `0` input. |

### CI-13 — SynthEyes `# 0 0.000000 0.000000 15` → **NOT A CORE DEFECT** (reclassification proposed)

| Question | Answer |
|---|---|
| Does the spec define the format? | **Yes.** `ADAPTER_SYNTHEYES_2304.md` §2 and §8: every row is `<TRACKER_NAME> <FRAME> <U> <V> <OUTCOME>`, grouped by exact tracker name. The grammar has no header or comment rows, and `#` is a valid tracker name (no whitespace). |
| Does the released implementation violate the spec? | **No.** It reads the row as a tracker named `#`, exactly as specified. |
| Is there enough evidence? | **Yes.** Every SynthEyes scene that produced the row (5 of 5) had imported a historical pre-Core generated file whose **first line was a `# ...` comment** (Tests 01D, 03, 07, 08). The original artist export, which never imported a generated file, has no such row (0 of 2 copies). The row has the same shape in all five files. So SynthEyes created a real tracker named `#` from the comment line when it imported those files. It is not part of the export format. |
| Classification | **Not a Core defect.** Contamination of historical test scenes by pre-Core generator output. The v1.0.0 writer emits tracker rows only, so released-tool round trips cannot create it. |
| Fix | None. Skipping `#` rows would invent a comment syntax the verified grammar does not have, and would silently delete a tracker that exists in the scene. Regression tests now pin the specified behaviour (`tests/test_syntheyes_hash_tracker_name.py`), and the adapter spec documents it. |
| Impact on past evidence | The historical Test 04 / 07 / 08 SynthEyes round-trip PASS results were produced by scripts that skipped `#` lines, so they hid this tracker. The released reader reports it. |

**Release decision needed (owner):** remove CI-13 from the v1.0.1 release blockers on the basis of this evidence.

### SPEC-4 — 3DE export with zero-sample points (new; not in v1.0.1)

One real 3DE R5 production export (P-1, 43 points) contains 3 points with sample count `0`. The specification requires at least one observation per track (`INTERCHANGE_MASTER.md` §10, Canonical Observation Requirement), so converting that file fails by design and nothing is dropped silently. The Core behaves as specified. Whether v1 should support exports that contain empty points is a **product and specification question**, tracked separately.

---

## 5. Artist Actions and Records

### Re-evaluated need for A5 / A6

| Action | Status | Reason |
|---|---|---|
| **A5** (3DE field meaning) | **No longer required** | CI-12 is resolved from existing evidence. Its meaning (likely point colour) is not needed, because the value is not Canonical and is proven not to affect observations. If an export with another value appears, the reader rejects it with a clear message, and that file becomes the evidence. |
| **A6** (SynthEyes `#` row) | **No longer required** for the fix. **Optional, about 1 minute** | Lineage evidence settles it. Optional confirmation: open one affected SynthEyes scene (e.g. the Test 08 import scene) and check that the tracker list contains a tracker named `#`. No export is needed. |
| **A1–A4** | **Required** | CI-1 release gate (section 3) |

### Native Import record (to be completed by the artist)

| Case | Date | Software + build | Artist | Track count expected / observed | Observation count expected / observed | File Import | Track Identity | Frame Mapping | Point Position | Natural Gap | Editability | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | | 3DEqualizer R5 build: | | 14 / | 664 / | | | | | | | |
| A2 | | SynthEyes 2304 build: | | 14 / | 664 / | | | | | | | |
| A3 | | 3DEqualizer R5 build: | | 9 / | 146 / | | | | | | | |
| A4 | | SynthEyes 2304 build: | | 9 / | 146 / | | | | | | | |

---

## 6. Release Gate for v1.0.1

v1.0.1 may be tagged only when **all** of the following hold:

1. ~~CI-13 fixed~~ → the owner confirms the CI-13 reclassification (section 4).
2. CI-12 is fixed and regression-tested. **Done.**
3. The full test suite passes locally and in GitHub Actions (Windows and Linux).
4. A1–A4 are recorded as PASS in the table above.
5. `validation/README.md` gains the v1.0.1 Native Import records.
