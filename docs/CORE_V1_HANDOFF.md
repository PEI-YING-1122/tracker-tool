# Tracker Tool Core v1.0.0 — GUI Handoff

## 1. Handoff Purpose

This document defines the boundary between the released **Tracker Tool Core v1.0.0** and the upcoming GUI development phase.

The GUI phase begins from an already completed Core.

The GUI is not a redesign of the conversion system.

---

## 2. Release Status

```text
Product: Tracker Tool Core
Version: v1.0.0
Status: RELEASED
Core semantics: FROZEN BASELINE
Next phase: GUI
```

The v1.0.0 Core should be treated as the production baseline for GUI development.

---

## 3. Supported Production Targets

The current released scope is:

- **3DEqualizer R5**
- **PFTrack 2017**
- **SynthEyes 2304**

GUI development must preserve compatibility with these exact production targets unless the project explicitly approves a future version change.

Do not assume behavior from newer software versions.

---

## 4. Existing Core Scope

The released Core currently includes the following established areas:

- Canonical 2D Track Core
- Source handling
- Target handling
- ShotConfig
- CLI conversion
- Validation
- Error Contract
- target-specific conversion / output behavior
- Native Import Validation

The exact module names, file paths, public functions, classes, and CLI commands must be discovered from the repository rather than assumed by this handoff document.

---

## 5. Architectural Principle

The shared Canonical 2D Track representation is the center of the conversion architecture.

Conceptually:

```text
Source
  ↓
Source interpretation
  ↓
Canonical 2D Track Core
  ↓
Validation
  ↓
Target conversion / adapter
  ↓
Target-native output
```

The GUI must sit above this architecture.

Conceptually:

```text
User
  ↓
GUI
  ↓
Existing Core boundary
  ↓
Existing v1.0.0 conversion pipeline
```

The GUI must not introduce a second semantic path.

---

## 6. Core Ownership

Core owns the meaning and behavior of conversion.

This includes, where applicable in the existing implementation:

- source interpretation
- canonical track representation
- coordinate interpretation
- frame interpretation
- ShotConfig interpretation
- conversion rules
- target-specific serialization / formatting
- validation rules
- error classification / contract
- output expectations

The GUI should collect and present information required by these systems, not reinterpret them.

---

## 7. GUI Ownership

The GUI may own presentation and orchestration concerns such as:

- source file selection
- target selection
- ShotConfig input controls
- configuration editing UX
- validation result display
- error display
- progress / busy state
- conversion trigger
- result summary
- output location selection
- logs / diagnostics presentation
- user-facing settings
- safe persistence of GUI-only preferences

GUI-owned state must not silently alter Core conversion meaning.

---

## 8. Frozen Semantics

The following classes of behavior are not to be changed merely for GUI convenience:

- conversion semantics
- canonical track semantics
- coordinate semantics
- frame semantics
- target formatting semantics
- validation semantics
- Error Contract semantics
- Source / Target meaning
- ShotConfig meaning
- native import expectations

If the GUI cannot integrate cleanly without changing one of these, treat it as an architecture issue and report it.

---

## 9. Core Change Classification

During GUI development, a requested or discovered change should be classified before implementation.

### A. GUI-only change

Examples:

- button layout
- window structure
- validation visualization
- error message presentation
- GUI state handling

These may proceed normally.

### B. Integration change with no semantic change

Possible examples:

- exposing an existing Core function through a stable interface
- adding progress callbacks
- import cleanup
- packaging cleanup
- non-semantic refactoring

These require a proposal before touching released Core code.

### C. Core semantic change

Examples:

- changing how tracks are interpreted
- changing conversion rules
- changing filtering behavior
- changing frame interpretation
- changing target output meaning
- changing validation logic
- redefining Error Contract behavior

These are outside normal GUI work.

They require a separate Core issue / decision.

---

## 10. Core Bug Handling

If a possible Core bug is found:

```text
GUI observation
    ↓
Reproduce without GUI
    ↓
Check correct Core usage
    ↓
Classify issue
    ├─ GUI bug
    ├─ integration issue
    ├─ documentation issue
    └─ Core defect
```

If it is an actual Core defect:

- document it independently
- include a minimal reproduction
- identify affected target / path
- identify expected vs actual behavior
- do not conceal it with GUI-only behavior
- do not silently patch Core as part of unrelated GUI work

---

## 11. Error Contract Rule

The released Error Contract belongs to Core.

The GUI may:

- map existing errors to user-readable presentation
- group information visually
- provide details / expandable diagnostics
- highlight actionable input problems

The GUI must not:

- redefine which condition counts as which Core error
- convert a failure into success
- suppress a Core error in order to continue with altered behavior
- create alternative conversion semantics behind the UI

---

## 12. Validation Rule

Validation remains a Core responsibility.

The GUI may present validation:

```text
PASS
WARNING
FAIL
```

or another presentation appropriate to the existing Core contract, but it must derive its meaning from the actual released validation behavior.

Do not duplicate validation logic in the UI unless the logic is purely GUI input validation and clearly separate from Core validation.

---

## 13. CLI Relationship

The current Core includes CLI conversion.

Claude Code must inspect whether:

- the CLI is the intended stable public boundary
- the CLI delegates to reusable Python / application services
- the GUI can call reusable Core functions directly
- subprocess invocation would create unnecessary coupling
- an existing service / facade layer already exists

Do not assume that "GUI should call CLI" or "GUI should import internal modules" before repository review.

The integration method should be selected after identifying the actual Core architecture.

---

## 14. First GUI Milestone

Before implementation, Claude Code should produce an architecture proposal containing:

### Core integration

- discovered Core entry points
- recommended integration boundary
- data flow
- ownership of state
- error propagation
- validation propagation

### GUI

- recommended framework
- screen / page structure
- primary conversion workflow
- configuration UX
- result / validation UX
- error UX
- logging / progress strategy

### Engineering

- new package / module layout
- test strategy
- dependency impact
- packaging impact
- migration risk
- Core-touching changes, if any

---

## 15. Initial GUI Workflow — Do Not Prescribe Before Inspection

The GUI will likely need to expose some combination of:

- Source
- Target
- ShotConfig
- Validation
- Conversion
- Result / Error information

However, this handoff intentionally does **not** prescribe the final UI sequence or page layout.

Claude Code should derive the workflow from the actual Core contracts and user task flow.

---

## 16. Authority Rule

For released behavior, use this order of authority:

```text
Released Core implementation
        ↓
Passing Core tests / release validation
        ↓
Authoritative v1.0.0 specifications
        ↓
Target adapter specifications
        ↓
Historical development material
```

If documentation and current implementation disagree, do not silently choose one.

Report the mismatch.

---

## 17. Final Constraint

The GUI phase succeeds when:

> An artist can use the released Tracker Tool Core through a GUI while receiving the same conversion semantics, validation behavior, target behavior, and errors that v1.0.0 already defines.

The GUI must improve usability without changing the meaning of the tool.
