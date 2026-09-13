# Tracker Tool — Project Goal

## 1. Project Purpose

This project builds a standalone desktop tool for analyzing and interchanging artist-created 2D tracking data between:

* 3DEqualizer R5
* PFTrack 2017
* SynthEyes 2304

The tool must allow an artist to move existing 2D tracking data between supported applications without manually retracking the shot.

The project is intended to become a practical production utility rather than a one-off conversion script.

---

## 2. Core Goal

The core architecture must be:

```text
3DE / PFTrack / SynthEyes
        ↓
Native Reader
        ↓
Canonical 2D Track Core
        ↓
Validation / Read-only Analysis
        ↓
Native Writer
        ↓
3DE / PFTrack / SynthEyes
```

All supported software must communicate through the same software-independent Canonical 2D Track Core.

The project must not implement dedicated pairwise converters such as:

```text
3DE → PFTrack
3DE → SynthEyes
PFTrack → 3DE
PFTrack → SynthEyes
SynthEyes → 3DE
SynthEyes → PFTrack
```

Target Writers must depend only on Canonical data and required shot metadata, not on the original source software.

---

## 3. v1 Scope

Version 1 focuses on two primary functions:

### 3.1 2D Track Interchange

Read artist-created native 2D tracking data from:

* 3DEqualizer R5
* PFTrack 2017
* SynthEyes 2304

Convert the data into the Canonical 2D Track Core.

Write the Canonical data back into the verified native format of any supported target application.

The interchange process must preserve existing artist tracking measurements as faithfully as possible.

### 3.2 Read-only Track Analysis

The tool may analyze imported Canonical track data and report information such as:

* Track count
* Observation count
* Frame range
* Per-track frame coverage
* Track length
* Natural gaps
* Per-frame point count
* Duplicate or conflicting track names
* Invalid or out-of-range observations
* Validation warnings and errors

Analysis in v1 is read-only.

The Analysis layer must not modify Canonical track data.

Charts, graphs, track-distribution visualizations, and other analysis visualization features are not required for v1.

They may be added later as GUI enhancements without changing the Analysis core.

---

## 4. v1 Out of Scope

Version 1 must not automatically:

* Delete tracks
* Select tracks
* Filter tracks
* Rank tracks
* Prune tracks
* Merge tracks
* Deduplicate tracks
* Interpolate missing observations
* Fill natural gaps
* Extend tracks
* Generate new tracking observations
* Correct track positions
* Perform automatic cleanup

Terminology clarification:

Track Merge means combining two or more distinct Tracks into a single Track identity and is forbidden in v1.

Source-set Aggregation means combining independently parsed and validated source Track collections into one Canonical collection while preserving every Track identity and observation unchanged.

Source-set Aggregation is not Track Merge.

Version 1 also does not include:

* Camera Solve
* Focal Length conversion
* Filmback conversion
* Lens Distortion conversion
* Survey data
* 3D Points
* Coordinate system / orientation / scale
* Object Track
* Camera Constraints
* Track Groups
* Track Colors
* Tracking Weights
* Native tracking quality metadata as Canonical semantics

These features may be considered in future versions, but they must not change the behavior of v1.

---

## 5. Data Preservation Principle

Artist-created 2D tracking data is production evidence.

The default behavior of the interchange system is:

```text
100% PRESERVE
```

The tool must not silently:

* Remove observations
* Add observations
* Rename tracks
* Merge tracks
* Fill gaps
* Correct frame offsets
* Flip coordinates
* Scale coordinates
* Clamp coordinates

If the tool detects a problem, it should report the problem rather than silently modify the data.

---

## 6. Canonical Layer Principle

The Canonical 2D Track Core is the shared internal representation used by all supported applications.

Its purpose is to separate:

```text
Software-specific native representation
```

from:

```text
Software-independent 2D tracking meaning
```

The Canonical layer represents only the shared 2D Track Core required by v1, including:

* Internal track identity
* Artist-visible track name
* Production frame
* Pixel-space X position
* Pixel-space Y position
* Natural observation gaps

Software-specific metadata must remain inside the relevant Adapter unless explicitly promoted into the Canonical specification.

---

## 7. Adapter Responsibility

Each supported tracking application has its own Adapter.

Each Adapter contains software-specific behavior such as:

* Native file parsing
* Native file writing
* Frame mapping
* Coordinate conversion
* Native grammar
* Required application-specific fields
* Native format validation

Adapters must not contain source-to-target pairwise conversion logic.

Example:

```text
PFTrack Reader
→ Canonical
→ 3DE Writer
```

not:

```text
PFTrack-to-3DE Converter
```

---

## 8. Validation Principle

Validation must remain separate from conversion.

A parser accepting a file does not prove that the real tracking software will accept the generated native file.

The project must distinguish between:

```text
Parser Validation
Software Import Validation
Round-trip Validation
```

Real 3DE, PFTrack, and SynthEyes behavior remains the final authority for native compatibility.

---

## 9. GUI Principle

The production application will use PySide6 as its desktop GUI framework.

The GUI is responsible for:

* User input
* Source / target selection
* File selection
* Shot metadata input
* Displaying analysis results
* Displaying validation results
* Starting application-level operations

The GUI must not contain native parsing, coordinate conversion, frame mapping, analysis rules, or source-to-target conversion logic.

The GUI must call the application/core layers.

---

## 10. Project Technology

Primary development stack:

```text
Python
PySide6
uv
pytest
Git
GitHub
VS Code
Codex
```

Project dependencies must be managed through `uv`.

Git and GitHub are used for:

* Source control
* Change history
* Issue tracking
* Regression evidence
* Versioning
* Release distribution

---

## 11. Development Principle

The project should be developed incrementally.

Large features should be split into small independently verifiable behaviors.

Where appropriate, implementation should use Test-Driven Development.

Tests should verify public behavior and known production expectations rather than implementation details.

Previously validated real-software behavior should be reused as regression evidence whenever possible.

---

## 12. Success Definition

Tracker Tool v1 is successful when an artist can:

```text
Import supported native 2D tracking data
        ↓
Convert it into Canonical data
        ↓
Inspect read-only analysis and validation results
        ↓
Export it into another supported native format
        ↓
Import the result into the real target tracking software
```

without:

* Retracking the shot
* Losing artist-created observations
* Filling natural gaps
* Introducing silent frame offsets
* Introducing silent coordinate changes
* Depending on pairwise conversion code

The tool should make 2D tracking interchange deterministic, inspectable, and reusable across 3DEqualizer R5, PFTrack 2017, and SynthEyes 2304.

---

## 13. Source of Truth

This file defines the high-level project direction only.

Detailed behavior is defined by the project specifications, including:

```text
INTERCHANGE_MASTER.md
CANONICAL_2D_TRACK_CORE.md
VALIDATION_CONTRACT.md
ADAPTER_3DE_R5.md
ADAPTER_PFTRACK_2017.md
ADAPTER_SYNTHEYES_2304.md
```

When implementation details conflict with these specifications, the verified specification and real-software validation evidence take precedence.
