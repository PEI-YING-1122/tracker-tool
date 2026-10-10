# Third-Party Notices — Tracker Tool (Windows GUI bundle)

> **使用範圍：** 本交付包供 owner 與公司內部 Tracking Artist 使用，不公開散布。
>
> **狀態：** 本文件列出交付包中實際包含的第三方元件、版本、授權與原始碼來源，並附上可取得的授權全文（`THIRD_PARTY_LICENSES/`）。部分義務**尚未經過法律確認**，詳見最後一節「Unconfirmed items」。本文件**不構成**完全合規的聲明。

```text
Inventory date : 2026-10-10
Build basis    : PySide6-Essentials 6.11.2 (Qt 6.11.2), Python 3.11.14 (python-build-standalone via uv),
                 OpenSSL 3.5.5, PyInstaller 6.22.3, Windows x64, one-folder bundle
Exact build    : see BUILD_INFO.txt next to TrackerTool.exe
Verified       : 2026-10-10 by inspecting an actual bundle (PE version resources, imports and
                 embedded identification strings of every .dll / .pyd under _internal/)
```

---

## 1. Components shipped in the bundle

| Component | Version | Location in bundle | License | Full text in `THIRD_PARTY_LICENSES/` | Source code |
|---|---|---|---|---|---|
| Qt for Python — PySide6 (Essentials) | 6.11.2 | `_internal/PySide6/` (`*.pyd`, `pyside6.abi3.dll`) | LGPL-3.0-only (chosen from LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only) | `LGPL-3.0.txt`, `GPL-3.0.txt` | https://code.qt.io/cgit/pyside/pyside-setup.git/ tag `v6.11.2`; PyPI sdist `pyside6-6.11.2` |
| Shiboken6 | 6.11.2 | `_internal/shiboken6/` | LGPL-3.0-only (as above) | `LGPL-3.0.txt`, `GPL-3.0.txt` | same repository and tag |
| Qt 6 modules | 6.11.2 | `_internal/PySide6/Qt6Core.dll`, `Qt6Gui.dll`, `Qt6Widgets.dll`, `Qt6Network.dll`, `Qt6Svg.dll` | LGPL-3.0-only | `LGPL-3.0.txt`, `GPL-3.0.txt` | https://download.qt.io/archive/qt/6.11/6.11.2/single/ |
| Qt 6 plugins | 6.11.2 | `_internal/PySide6/plugins/`: generic (`qtuiotouchplugin`), iconengines (`qsvgicon`), imageformats (`qgif`, `qicns`, `qico`, `qjpeg`, `qsvg`, `qtga`, `qtiff`, `qwbmp`, `qwebp`), networkinformation (`qnetworklistmanager`), platforms (`qwindows`, `qdirect2d`, `qminimal`, `qoffscreen`), styles (`qmodernwindowsstyle`), tls (`qschannelbackend`, `qopensslbackend`, `qcertonlybackend`) | LGPL-3.0-only | as above | as above; Qt Image Formats module: `qtimageformats` in the same archive |
| Qt translations | 6.11.2 | `_internal/PySide6/translations/*.qm` | LGPL-3.0-only | as above | as above (`qttranslations`) |
| Third-party code built into Qt | see §2 | inside the Qt DLLs / plugins | see §2 | partly (see §2) | see §2 |
| Mesa (llvmpipe software OpenGL) | **11.2.2** (identified in the binary) | `_internal/PySide6/opengl32sw.dll` | MIT (Mesa core) | `Mesa-license.rst` | https://gitlab.freedesktop.org/mesa/mesa tag `mesa-11.2.2` |
| LLVM (linked into `opengl32sw.dll`) | version not identified | inside `opengl32sw.dll` | Apache-2.0 WITH LLVM-exception | `LLVM-LICENSE.txt` | https://github.com/llvm/llvm-project |
| Python runtime and standard library | 3.11.14 | `python311.dll`, `python3.dll`, `base_library.zip`, `*.pyd` | PSF-2.0 | `Python-3.11-LICENSE.txt`, `CPython-3.11-incorporated-software.rst` | https://www.python.org/downloads/source/ ; build: https://github.com/astral-sh/python-build-standalone |
| zlib (inside the Python runtime) | 1.3.1 (`zlib.ZLIB_RUNTIME_VERSION`) | `python311.dll` | Zlib | `CPython-3.11-incorporated-software.rst` (section "zlib") | https://zlib.net/ |
| bzip2 | 1.0.8 | `_bz2.pyd` | bzip2 license | `Python-3.11-LICENSE.txt` | https://sourceware.org/bzip2/ |
| liblzma (XZ Utils) | version not identified | `_lzma.pyd` | 0BSD (current XZ Utils) | `xz-COPYING.txt` | https://tukaani.org/xz/ |
| libmpdec | 2.5.1 (`decimal.__libmpdec_version__`) | `_decimal.pyd` | BSD-2-Clause | `CPython-3.11-incorporated-software.rst` (section "libmpdec") | https://www.bytereef.org/mpdecimal/ |
| OpenSSL | 3.5.5 (copy shipped with the Python build; checked by the build script) | `libssl-3-x64.dll`, `libcrypto-3-x64.dll` | Apache-2.0 | `Apache-2.0.txt` | https://www.openssl.org/source/ |
| PyInstaller bootloader | 6.22.3 | embedded in `TrackerTool.exe` | GPL-2.0-or-later **with the PyInstaller Bootloader Exception** (allows distribution of the bundled program under any terms) | `PyInstaller-COPYING.txt` | https://github.com/pyinstaller/pyinstaller tag `v6.22.3` |

Tracker Tool itself uses only the Qt modules **QtCore, QtGui and QtWidgets**. Qt6Network, Qt6Svg and the network / SVG related plugins are included automatically by the PyInstaller PySide6 hooks.

---

## 2. Third-party components inside Qt 6.11.2 (Qt Core, Qt GUI, Qt Network, Qt SVG)

Source of this list: https://doc.qt.io/qt-6.11/licenses-used-in-qt.html (documents Qt 6.11.2). Qt Widgets lists no third-party components.

Some entries apply only to other platforms (for example the macOS Cocoa plugin, Android style, X11 / XCB helpers, forkfd). Whether each one is compiled into the Windows binaries of PySide6-Essentials 6.11.2 has **not** been verified item by item.

| Qt module | Component (version) | License |
|---|---|---|
| Core | Apache Tika MimeType Definitions | Apache-2.0 |
| Core | BLAKE2 reference implementation | CC0-1.0 or Apache-2.0 |
| Core | zlib 1.3.2 | Zlib |
| Core | Double-conversion 3.4.0 | BSD-3-Clause |
| Core | Easing Equations (Robert Penner) | BSD-3-Clause |
| Core | MD4, MD5, SHA-1 | Public Domain |
| Core | PCRE2 10.47 (+ SLJIT) | BSD-3-Clause with PCRE2 binary-like Packages Exception (SLJIT: BSD-2-Clause) |
| Core | SHA-3 Keccak 3.2 / brg_endian 1.0.0 | CC0-1.0 / BSD-2-Clause |
| Core | SHA-384 / SHA-512 (RFC 6234) | BSD-3-Clause |
| Core | SipHash, tl::expected | CC0-1.0 |
| Core | TinyCBOR 7.0, forkfd | MIT |
| Core | Unicode Character Database 36 / CLDR v48.2 | Unicode License Agreement (2016) / Unicode License v3 |
| GUI | FreeType 2.14.3 (and anti-aliasing rasterizer) | FreeType Project License (FTL) or GPL-2.0-only |
| GUI | FreeType BDF / PCF / zlib parts | MIT / MIT Open Group / Zlib |
| GUI | HarfBuzz-NG 14.3.0 | MIT |
| GUI | libjpeg-turbo 3.2.0 | IJG License and BSD-3-Clause |
| GUI | libpng 1.6.58 | libpng License / PNG Reference Library v2 |
| GUI | MD4C 0.5.3, Pixman 0.17.12, OpenGL / OpenGL ES headers, D3D12 Memory Allocator, D3D12 mipmap generator, Vulkan Memory Allocator 3.2.1, WebGradients, XCB-XInput | MIT |
| GUI | Vulkan API Registry 1.4.308 | Apache-2.0 or MIT |
| GUI | Emoji Segmenter 0.4.0, Native Style for Android | Apache-2.0 |
| GUI | Adobe Glyph List 1.7 | BSD-3-Clause |
| GUI | Smooth Scaling Algorithm | BSD-2-Clause and Imlib2 License |
| GUI | DejaVu Fonts 2.37 | Bitstream Vera Font License |
| GUI | Wintab API | LCS-Telegraphics License |
| GUI | sRGB color profile ICC file | International Color Consortium License |
| GUI | X Server helper, Cocoa platform plugin | X11 / HPND; BSD-3-Clause |
| Network | Public Suffix List (data), libpsl | MPL-2.0; BSD-3-Clause |
| SVG | XSVG | Historical Permission Notice and Disclaimer (sell variant) |

Qt Image Formats (plugins `qtiff`, `qwebp`, `qicns`, `qtga`, `qwbmp`) is a separate Qt module and is not covered by the table above:

| Qt module | Component | License | Full text in `THIRD_PARTY_LICENSES/` |
|---|---|---|---|
| Image Formats | libtiff (in `qtiff.dll`) | libtiff License (BSD-like) | `libtiff-LICENSE.md` |
| Image Formats | libwebp (in `qwebp.dll`) | BSD-3-Clause | `libwebp-COPYING.txt` |

### What the binaries show (2026-10-10 bundle inspection)

| Binary | Identified inside |
|---|---|
| `Qt6Core.dll` | PCRE2, TinyCBOR. Imports `icuuc.dll` from Windows (system ICU, **not** shipped) |
| `Qt6Gui.dll` | FreeType, HarfBuzz |
| `qjpeg.dll` | libjpeg-turbo |
| `qtiff.dll`, `qwebp.dll` | libtiff, libwebp |
| platform plugins | FreeType |
| `opengl32sw.dll` | Mesa 11.2.2, LLVM |

String matching cannot prove absence, so the other §2 entries (for example zlib and libpng inside Qt) are neither confirmed nor excluded.

The complete copyright statements of the §2 components are published on the Qt page above (one sub-page per component). They are **not** reproduced in this bundle (see Unconfirmed items).

---

## 3. LGPL-3.0: source code and replacing the Qt / PySide6 libraries

- **Source code:** the exact versions are listed in §1 (Qt 6.11.2, PySide6 / Shiboken6 6.11.2). They are available from the URLs above. Tracker Tool does not modify Qt, PySide6 or Shiboken6.
- **Replacement:** the bundle is a PyInstaller *one-folder* build. Qt, PySide6 and Shiboken6 are separate files under `_internal/` (`Qt6*.dll`, `plugins/`, `pyside6.abi3.dll`, `PySide6/*.pyd`, `shiboken6/`) and are loaded dynamically at start-up. A user can replace them with modified builds of the same versions, or ABI-compatible ones, by overwriting those files.
- **No restriction:** the delivery terms of Tracker Tool do not prohibit modifying these libraries, or reverse engineering for debugging such modifications (LGPL-3.0 §4).

---

## 4. Not shipped

The following development, test and build tools are not part of the bundle:

pytest, pytest-qt, pluggy, iniconfig, packaging, pygments, colorama, typing-extensions, PyInstaller (Python package), pyinstaller-hooks-contrib, altgraph, pefile, pywin32-ctypes, setuptools, uv / uv_build.

The Tracker Tool Core has no third-party runtime dependencies.

---

## 5. Unconfirmed items

These have **not** been confirmed. They should be reviewed before any distribution beyond internal use.

1. **Whether internal delivery is "conveying."** The Free Software Foundation's FAQ treats copies made within one organisation as not distributed to "others". This depends on how the company and its staff are organised, and has not been confirmed for this case. The notices are shipped regardless.
2. **Full copyright statements of the third-party components inside Qt (§2).** Only the component list and license names are included; the per-component copyright texts are not reproduced. Some components are confirmed in the binaries (§2, "What the binaries show"); the rest are neither confirmed nor excluded.
3. **Mesa `opengl32sw.dll`.** Mesa 11.2.2 and LLVM are confirmed in the binary, and the LLVM license is included. The LLVM version and any other statically linked components are not known; the exact build configuration used by the PySide6 project has not been obtained.
4. **libtiff / libwebp versions** inside the Qt Image Formats plugins, and the **liblzma** version inside `_lzma.pyd`, are not identified. The license texts included are the current upstream ones.
5. **Microsoft Visual C++ runtime: not shipped.** The `VCRUNTIME140*.dll` / `MSVCP140*.dll` files that Python, PySide6 and shiboken6 provide are removed from the bundle. Each workstation needs the Microsoft Visual C++ Redistributable (x64) 14.44 or later, installed from Microsoft (see VC_REDIST_INSTALL.md next to TrackerTool.exe).
6. **Unused Qt parts are shipped.** The PyInstaller PySide6 hooks add Qt Network, Qt SVG, TLS / network-information plugins and the image-format plugins although Tracker Tool does not use them. Excluding them would reduce the notices, but it changes the bundle that passed the Artist trial and has not been done.
7. **Tracker Tool's own license:** not chosen (see `USE_AND_LICENSE.md`).

Resolved on 2026-10-10: earlier builds could pick up a different OpenSSL (3.1.4, from Git for Windows on `PATH`). The build script now puts the Python build's own `DLLs` folder first and fails if the bundled OpenSSL / libffi DLLs differ from it.
