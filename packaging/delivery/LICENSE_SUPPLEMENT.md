# Tracker Tool — 第三方授權補充說明（內部交付包）

```text
適用版本 : Tracker Tool v1.1.0（TrackerTool/BUILD_INFO.txt 中的 commit 為 437e7e6）
日期     : 2026-10-10
```

本文件補充 `TrackerTool/THIRD_PARTY_NOTICES.md`。該檔案隨 v1.1.0 tag 建置，內容固定；它 §5「Unconfirmed items」中的項目，以本文件的狀態為準。

本文件整理的是事實與作法，**不是法律意見**。

---

## 1. 交付包內容

| 資料夾 / 檔案 | 內容 |
|---|---|
| `TrackerTool/` | GUI 程式，由 v1.1.0 tag 建置，未經修改 |
| `LICENSE_SUPPLEMENT/` | 本文件；`Qt-6.11.2-third-party-attributions.txt` |
| `LGPL_SOURCES/` | Qt、PySide6 與 Tracker Tool 的原始碼，以及 `SHA256SUMS.txt` |
| `DELIVERY_MANIFEST.txt` | 交付包中每個檔案的 SHA-256 |

複製或轉交時，請整個交付包一起，不要只複製 `TrackerTool/`。

---

## 2. Qt / PySide6（LGPL-3.0）

### 原始碼

`LGPL_SOURCES/` 附有與程式中的 Qt / PySide6 完全對應的官方原始碼：

| 檔案 | 對應 bundle 中的 |
|---|---|
| `qtbase-everywhere-src-6.11.2.tar.xz` | `Qt6Core`、`Qt6Gui`、`Qt6Widgets`、`Qt6Network` 與 platforms / styles / tls / generic / networkinformation / 多數 imageformats plugins |
| `qtsvg-everywhere-src-6.11.2.tar.xz` | `Qt6Svg`、`qsvg`、`qsvgicon` |
| `qtimageformats-everywhere-src-6.11.2.tar.xz` | `qtiff`、`qwebp`、`qicns`、`qtga`、`qwbmp` |
| `qttranslations-everywhere-src-6.11.2.tar.xz` | `PySide6/translations/` |
| `pyside-setup-everywhere-src-6.11.2.tar.xz` | PySide6、Shiboken6 |
| `tracker-tool-v1.1.0-src.zip` | Tracker Tool 本身（含建置腳本與鎖定的依賴版本 `uv.lock`） |

- Qt 的原始碼檔案已用 Qt 官方公布的 `md5sums.txt` 驗證。
- PySide6 原始碼取自 Qt 官方下載站（官方未公布 checksum）。

### 替換函式庫

- **Qt 與 PySide6 的二進位檔**（`TrackerTool/_internal/PySide6/`、`_internal/shiboken6/` 下的 `.dll` / `.pyd` 與 `plugins/`）是獨立檔案，直接覆蓋即可換成修改過、或相容的版本。
- **PySide6 / Shiboken6 的 Python 部分**（`__init__.py` 等）被打包進 `TrackerTool.exe`。要替換這部分，請用 `tracker-tool-v1.1.0-src.zip` 重新建置：
  1. 安裝修改過的 PySide6；
  2. 執行 `packaging/build_gui.py`。

  步驟見 `docs/gui/GUI_PACKAGING.md`。
- Tracker Tool 不禁止上述修改，也不禁止為了除錯這些修改而進行的逆向工程。

### 執行時的版權顯示

Tracker Tool 執行時不顯示任何版權聲明，因此不需要另外在程式內顯示 Qt 的聲明（LGPL-3.0 §4(c)）。

---

## 3. §5 未確認項目的目前狀態

| # | 項目 | 狀態 |
|---|---|---|
| 1 | 內部交付是否算「conveying」 | **不再影響交付**：本交付包已依「視為散布」的標準提供原始碼、聲明與替換方式 |
| 2 | Qt 內部第三方元件的版權聲明 | **已補齊**：`Qt-6.11.2-third-party-attributions.txt`（46 個元件，含版權聲明與授權全文，取自 Qt 6.11.2 原始碼中的 `qt_attribution.json`）。只排除其他平台與未打包模組的元件 |
| 3 | Mesa `opengl32sw.dll` | Mesa 11.2.2 與 LLVM 已確認，授權全文已附。LLVM 確切版本無法辨識；附上的 LLVM 授權條文適用於目前的 LLVM 版本 |
| 4 | 元件版本 | libtiff **4.7.2**、libwebp **1.6.0**（取自 Qt 原始碼）。liblzma 版本仍無法辨識；其授權（0BSD 或早期的 public domain）都沒有附加義務 |
| 5 | Microsoft Visual C++ runtime | **待 owner 確認**，見 §4 |
| 6 | 隨附未使用的 Qt 模組 | 已涵蓋在聲明與原始碼中，不影響授權義務 |
| 7 | Tracker Tool 本身的授權 | 不新增開源授權；使用範圍見 `TrackerTool/USE_AND_LICENSE.md` |

---

## 4. 待確認：Microsoft Visual C++ runtime

`VCRUNTIME140*.dll`、`MSVCP140*.dll`（14.44.35211.0）隨 PySide6 與 Python 一起放在程式資料夾內。

- Microsoft 允許應用程式隨附這些檔案（「app-local」部署），條件規定在 Visual Studio 授權條款的「Distributable Code」一節。
- 這些檔案並不是本專案用 Visual Studio 編譯時加入的，而是來自 PySide6 與 Python 的官方發行檔。
- 在公司內部使用的情境下，風險很低。但本專案是否適用該條款，**尚未經法務或 owner 確認**。
