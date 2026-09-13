# Tracker Tool — Codex Project Rules

## 1. Read Project Direction First

Before implementing or modifying project behavior, read:

```text
PROJECT_GOAL.md
```

When working on a software-specific adapter or validation behavior, also read the relevant specification under `docs/` when available.

Do not invent missing production behavior.

If required behavior is not defined or cannot be verified, report the uncertainty instead of silently choosing an interpretation.

---

## 2. Preserve the Core Architecture

The required architecture is:

```text
Native Reader
→ Canonical 2D Track Core
→ Validation / Read-only Analysis
→ Native Writer
```

Do not implement dedicated source-to-target pairwise converters.

Forbidden examples:

```text
PFTrack → 3DE dedicated converter
3DE → SynthEyes dedicated converter
SynthEyes → PFTrack dedicated converter
```

Target Writers must not depend on the original Source Software.

---

## 3. Keep Responsibilities Separate

### Reader

A Reader converts native source data into Canonical data.

### Canonical

Canonical represents software-independent v1 2D track meaning.

### Validation

Validation detects specification violations and reports them.

Validation must not silently repair data.

### Analysis

Analysis is read-only in v1.

Analysis must not modify Canonical track data.

### Writer

A Writer converts Canonical data plus required shot configuration into verified target-native data.

### GUI

The GUI handles user interaction and presentation.

The GUI must not contain:

* Native parsing logic
* Frame conversion logic
* Coordinate conversion logic
* Canonical transformation logic
* Analysis rules
* Pairwise conversion logic

The GUI must call application/core functionality instead.

---

## 4. Preserve Artist Tracking Data

### Track Merge vs Source-set Aggregation

Do not confuse Track Merge with Source-set Aggregation.

Do not merge tracks. Track Merge means combining two or more distinct Track identities into one Track and is forbidden in v1.

Source-set Aggregation means combining independently parsed and validated Track collections into one Canonical collection while preserving every Track identity and observation unchanged. Source-set Aggregation is not Track Merge.

Source-set Aggregation must not:

- combine observations across different Track identities
- deduplicate Tracks
- silently rename Tracks
- resolve identity by coordinate proximity
- resolve identity by frame overlap
- resolve identity by Track order
- resolve identity by source role
- resolve identity by visible Track Name

Artist-created 2D track data defaults to:

```text
100% PRESERVE
```

Do not silently:

* Delete observations
* Create observations
* Interpolate observations
* Fill natural gaps
* Rename tracks
* Merge tracks
* Deduplicate tracks
* Correct frame offsets
* Flip coordinates
* Scale coordinates
* Clamp coordinates

When a conflict or invalid condition is detected:

```text
Preserve Evidence
Report the Problem
Stop or Reject the Affected Operation When Required
```

Do not silently fix production data.

---

## 5. Do Not Guess Native Formats

3DEqualizer, PFTrack, and SynthEyes native grammar must follow verified project specifications.

Do not invent:

* Headers
* Fields
* Field order
* Blank lines
* Separators
* Metadata semantics
* Coordinate conventions
* Frame conventions

A format accepted by the project's own parser is not sufficient evidence of real software compatibility.

Real target-software validation remains authoritative.

---

## 6. Development Scope

Implement only the behavior required by the current task.

Do not add future features merely because they may be useful later.

Do not make unrelated refactors while implementing a scoped behavior unless they are required for correctness.

Do not introduce unnecessary architectural layers or dependencies.

---

## 7. Testing

For conversion and domain behavior:

* Prefer tests against public module behavior.
* Prefer known-good examples and verified production evidence.
* Do not make tests depend unnecessarily on private implementation details.
* Do not reproduce the implementation algorithm inside the test as the sole source of expected truth.

When the TDD Skill is requested, follow the project-local TDD Skill workflow.

A passing unit test does not replace real-software import or round-trip validation where those are required.

---

## 8. Dependency Management

Use `uv` for Python dependency and environment management.

Do not introduce alternate Python environment-management workflows unless explicitly required.

New runtime dependencies must have a clear project need.

---

## 9. Change Discipline

Before modifying established behavior:

1. Identify the relevant specification.
2. Identify the affected public behavior.
3. Make the smallest scoped change.
4. Run the relevant tests.
5. Report what changed and what was validated.

Do not report a validation level that was not actually performed.

Examples:

```text
Unit Test PASS
!=
Real Software Import PASS
```

and:

```text
Parser PASS
!=
Round-trip PASS
```

---

## 10. v1 Boundary

Tracker Tool v1 provides:

```text
2D Track Interchange
+
Read-only Analysis
+
Validation / Diagnostics
```

v1 does not provide automatic Track cleanup, selection, filtering, ranking, modification, or visualization as a required feature.

Do not expand v1 scope without an explicit project decision.
