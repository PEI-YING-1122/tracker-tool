# Tracker Tool v1.1.1 — Release Notes

```text
Tag            : v1.1.1  (annotated) → bb0c84ea80f374da381ddb963b3a4e58979e743c
Tag message    : Tracker Tool v1.1.1 — Visual C++ runtime no longer bundled
Release title  : Tracker Tool v1.1.1 — Visual C++ runtime no longer bundled
Status         : RELEASED 2026-10-14 — https://github.com/PEI-YING-1122/tracker-tool/releases/tag/v1.1.1
```

The GitHub Release body is the section below. The Windows GUI executable is delivered internally only and is **not** attached to the GitHub Release.

---

Packaging update of the Windows GUI. The Windows bundle no longer includes the Microsoft Visual C++ runtime; workstations use the Microsoft Visual C++ Redistributable instead.

Unchanged from v1.1.0:

- the Core, the Canonical model and ShotConfig
- the GUI
- CLI arguments and output
- the formal Error Contract
- every conversion that produces output

### System requirements (Windows GUI)

- Windows 10 / 11, x64.
- **Microsoft Visual C++ Redistributable (x64) 14.44 or later.** The latest version from Microsoft is recommended: https://aka.ms/vc14/vc_redist.x64.exe
- Machines that do not meet these requirements are outside the validated support range.

### Changes

- **Visual C++ runtime not bundled.**
  - The build removes the `VCRUNTIME140*.dll` / `MSVCP140*.dll` files that Python, PySide6 and shiboken6 place in the bundle.
  - The smoke test fails if any of them is present.
- **Installation guide.** `VC_REDIST_INSTALL.md` (Traditional Chinese) next to `TrackerTool.exe` explains:
  - the pre-delivery check of the Redistributable version;
  - installation.
- **Third-party notices.** The notices now include the full copyright statements of the third-party components inside Qt 6.11.2. The internal delivery package also carries the Qt / PySide6 sources (LGPL-3.0).

### Validation

- **Automated:** 468 tests pass (2 opt-in tests skipped by default), including 102 GUI tests on the native Windows platform. All 10 released golden outputs are byte-identical. The formal Error Contract behaviour is identical to v1.1.0.
- **Bundle:** the Python code inside the executable is identical to v1.1.0.
- **Native import:** output converted by the packaged application from real PFTrack 2017 exports is byte-identical to the files that passed Artist Native Import.
- **Workstation:** a company Windows workstation produced output byte-identical to v1.1.0.
- **Details:** `validation/RELEASE_READINESS_v1.1.1.md`.

### Known limitations

- **Not tested** on machines without the Visual C++ Redistributable, or with a version older than 14.44. Check the version before first use, as described in `VC_REDIST_INSTALL.md`.
- Otherwise unchanged from v1.1.0.
