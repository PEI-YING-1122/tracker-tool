# Tracker Tool — Claude Code Project Instructions

## 1. Project Status

Tracker Tool Core **v1.0.0** has been completed, validated, formally released, and is now the baseline for all further development.

Current Core scope includes:

- 3DEqualizer R5
- PFTrack 2017
- SynthEyes 2304
- Canonical 2D Track Core
- CLI conversion
- Validation
- Error Contract
- Native Import Validation

The current development phase is:

> **GUI planning and implementation on top of Core v1.0.0**

---

## 2. Primary Responsibility

Claude Code is responsible for the GUI phase, including:

- inspecting the existing repository and Core architecture
- identifying the existing Core integration boundary
- proposing the GUI architecture
- selecting an appropriate GUI framework / technology
- designing the user workflow
- implementing the GUI layer
- adding GUI-specific tests
- documenting the GUI layer
- identifying integration risks

Do not assume a GUI architecture before inspecting the repository.

Do not begin by rewriting the Core.

---

## 3. Core v1.0.0 Freeze Rule

Core v1.0.0 conversion behavior is considered frozen.

The GUI must be built on top of the existing Core and must not silently redefine or replace existing Core behavior.

The following concepts and contracts must remain compatible with v1.0.0:

- Source
- Target
- Canonical 2D Track Core
- ShotConfig
- Validation
- Error Contract
- CLI conversion behavior
- Native Import expectations

Do not change existing behavior simply because a different behavior would make GUI implementation easier.

---

## 4. What the GUI Must NOT Do

The GUI must not become a second conversion engine.

Do not implement GUI-only versions of:

- source parsing semantics
- canonical track interpretation
- coordinate semantics
- frame semantics
- conversion semantics
- target formatting semantics
- validation rules
- error classification
- target-specific track conversion logic

If equivalent logic already exists in Core, reuse Core.

---

## 5. Intended Architecture

The intended dependency direction is:

```text
User
  ↓
GUI
  ↓
Core integration boundary
  ↓
Existing Core v1.0.0
  ↓
Canonical 2D Track representation
  ↓
Validation / Error Contract
  ↓
Target adapter
  ↓
3DEqualizer / PFTrack / SynthEyes output
```

The GUI is primarily:

- presentation
- orchestration
- user input collection
- progress / status presentation
- validation presentation
- error presentation
- configuration UX

It is not responsible for redefining Core semantics.

---

## 6. Core Bug Rule

If GUI development reveals suspicious or incorrect behavior:

1. Reproduce the behavior against Core independently from the GUI.
2. Determine whether the issue is:
   - incorrect GUI usage
   - integration boundary issue
   - packaging / exposure issue
   - documentation issue
   - actual Core defect
3. Document the finding separately.
4. Do not hide an actual Core defect with GUI-specific workaround logic.
5. Do not alter released Core behavior without explicit approval.

A GUI workaround that changes effective conversion behavior is not an acceptable fix.

---

## 7. Allowed Discussion Around the Frozen Core

"Frozen" means released **conversion semantics and contracts** must not be casually changed.

It does not mean every source file is permanently untouchable.

During GUI integration, Claude Code may identify the need for changes such as:

- API exposure
- cleaner integration boundary
- packaging changes
- dependency injection
- import organization
- non-semantic refactoring
- progress reporting hooks
- typing / interface improvements

However:

> Propose these changes first. Do not implement them automatically if they touch the existing Core.

Any proposed change must explicitly explain why Core behavior remains semantically identical.

---

## 8. Source of Truth

Do not infer project behavior from filenames alone.

Use the following priority when determining existing v1.0.0 behavior:

1. released Core implementation
2. passing Core tests / release validation
3. authoritative v1.0.0 project documentation
4. adapter specifications
5. historical development notes / old issues / old prompts

Historical material must not override released Core behavior.

If sources conflict, report the conflict before changing anything.

---

## 9. First Assignment — Repository Architecture Review

Before writing production GUI code, inspect the repository.

Review at minimum:

- source tree
- Core modules
- canonical data model
- Source / Target handling
- ShotConfig
- validation
- Error Contract
- adapters
- CLI entry points
- tests
- packaging / dependencies
- release / native import validation material
- existing documentation

Then produce a **GUI Development Plan**.

The plan must answer:

1. What is the current Core architecture?
2. What are the existing public or practical Core entry points?
3. How should the GUI invoke Core?
4. Which functionality must be reused directly rather than reimplemented?
5. Is there already a clean GUI integration boundary?
6. If not, what is missing?
7. Which GUI framework do you recommend, and why?
8. What should the first GUI workflow expose?
9. How should ShotConfig be represented in the GUI?
10. How should Validation be presented?
11. How should the existing Error Contract be presented?
12. How should conversion progress / completion be represented?
13. What GUI-specific state should exist?
14. What state must remain owned by Core?
15. What tests should be added for the GUI layer?
16. What packaging / deployment risks exist?
17. Does any proposed GUI requirement appear to require a Core change?
18. What implementation phases do you recommend?

---

## 10. First Assignment Constraints

For the initial architecture review:

- do not modify production code
- do not implement the GUI yet
- do not redesign Core semantics
- do not create UI-layer conversion logic
- do not silently "fix" Core behavior
- do not assume the newest 3DE / PFTrack / SynthEyes behavior applies to the production versions

Production targets are specifically:

- **3DEqualizer R5**
- **PFTrack 2017**
- **SynthEyes 2304**

Version-specific behavior matters.

---

## 11. GUI Design Freedom

Within the Core boundary, Claude Code has freedom to propose:

- GUI framework
- visual hierarchy
- window / page organization
- source selection UX
- target selection UX
- ShotConfig UX
- validation UX
- error UX
- conversion workflow
- progress display
- logging presentation
- result summary
- settings organization
- packaging approach

The design should follow the actual Core workflow discovered from the repository rather than inventing a parallel workflow.

---

## 12. Decision Rule

Before making a GUI architecture decision, ask:

> Does this merely present / orchestrate existing Core behavior, or does it redefine Core behavior?

If it redefines Core behavior, stop and raise it as a Core-level decision.

---

## 13. Project Goal

The goal of the GUI phase is not to redesign Tracker Tool.

The goal is:

> **Make the released Tracker Tool Core v1.0.0 accessible through a reliable GUI without changing what the Core means or does.**
