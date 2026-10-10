# Third-Party Notices — Tracker Tool GUI (Windows bundle)

> **DRAFT — NOT REVIEWED. NOT A STATEMENT OF COMPLIANCE.**
> This file lists the third-party components found in the Windows GUI bundle (PyInstaller one-folder build) and their declared licenses, as an input for the project's licensing decision.
> - The obligations have **not** been confirmed by legal review.
> - This file and the texts in `packaging/licenses/` are **not yet included** in the bundle.
> - Tracker Tool's own license has not been chosen yet.

Inventory date: 2026-10-10. Source build: `gui/develop`, PySide6-Essentials 6.11.2, Python 3.11 (python-build-standalone, via uv), PyInstaller 6.22.3.

## Components distributed in the bundle

| Component | Version | Files in bundle | Declared license | License text available here | Source |
|---|---|---|---|---|---|
| Qt for Python — PySide6 (Essentials) | 6.11.2 | `_internal/PySide6/` (Python modules, `pyside6.abi3.dll`) | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only (or commercial) | `licenses/LGPL-3.0.txt`, `licenses/GPL-3.0.txt` | https://code.qt.io/cgit/pyside/pyside-setup.git/ (tag v6.11.2) |
| Shiboken6 | 6.11.2 | `_internal/shiboken6/` | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only | same as above | same repository |
| Qt 6 libraries | 6.11.x (shipped in PySide6-Essentials) | `Qt6Core.dll`, `Qt6Gui.dll`, `Qt6Widgets.dll`, `Qt6Network.dll`, `Qt6Svg.dll`, `PySide6/plugins/` (generic, iconengines, imageformats, networkinformation, platforms, styles, tls) | LGPL-3.0 (open-source use) | `licenses/LGPL-3.0.txt`, `licenses/GPL-3.0.txt` | https://download.qt.io/official_releases/qt/ |
| Third-party code inside Qt (e.g. image format, font and text libraries) | per Qt build | inside the Qt DLLs / plugins | various (see "Licenses Used in Qt") | **not collected yet** | https://doc.qt.io/qt-6/licenses-used-in-qt.html |
| Mesa llvmpipe software OpenGL (`opengl32sw.dll`) | shipped with PySide6 | `PySide6/opengl32sw.dll` | MIT-style (Mesa) | **not collected yet** | https://www.mesa3d.org/ |
| Python runtime and standard library | 3.11.14 | `python311.dll`, `python3.dll`, `base_library.zip`, `*.pyd` | PSF-2.0 | `licenses/Python-3.11-LICENSE.txt` (also covers bzip2 and the Tcl/Tk notice) | https://www.python.org/downloads/source/ |
| OpenSSL | 3.5.5 | `libssl-3-x64.dll`, `libcrypto-3-x64.dll` | Apache-2.0 | `licenses/Apache-2.0.txt` | https://www.openssl.org/source/ |
| xz / liblzma (`_lzma.pyd`) | per Python build | `_lzma.pyd` | 0BSD / public domain (per version) | **not collected yet** | https://tukaani.org/xz/ |
| libmpdec (`_decimal.pyd`) | per Python build | `_decimal.pyd` | BSD-2-Clause | **not collected yet** | https://www.bytereef.org/mpdecimal/ |
| Microsoft Visual C++ runtime | 14.x | `VCRUNTIME140*.dll`, `MSVCP140*.dll` | Microsoft redistributable terms | not applicable (redistribution terms) | Microsoft Visual C++ Redistributable |
| PyInstaller bootloader | 6.22.3 | embedded in `TrackerTool.exe` | GPL-2.0-or-later with the PyInstaller bootloader exception | **not collected yet** | https://github.com/pyinstaller/pyinstaller |

## Not distributed (development, test and build tools only)

pytest (MIT), pytest-qt (MIT), pluggy (MIT), iniconfig (MIT), packaging (Apache-2.0 OR BSD-2-Clause), pygments (BSD-2-Clause), colorama (BSD), typing-extensions (PSF-2.0), PyInstaller (GPL-2.0-or-later with exception), pyinstaller-hooks-contrib (GPL-2.0 / Apache-2.0), altgraph (MIT), pefile (MIT), pywin32-ctypes (BSD-3-Clause), setuptools (MIT), uv / uv_build.

## Open points before this can become a final notice

1. Collect the missing texts marked **not collected yet**.
2. Confirm the LGPL-3.0 obligations for Qt / PySide6:
   - provide the license texts;
   - give a source location for the exact versions;
   - keep the Qt libraries replaceable (they are separate DLLs in the one-folder bundle);
   - ensure the project's own license terms do not forbid modifying or reverse-engineering for debugging such modifications (LGPL-3.0 §4).
3. Confirm the Microsoft runtime redistribution terms for this build.
4. Decide how the notice and texts are shipped (e.g. copied next to `TrackerTool.exe` by `packaging/build_gui.py`).
