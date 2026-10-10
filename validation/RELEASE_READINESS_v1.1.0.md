# Tracker Tool v1.1.0（GUI）— Release Readiness Report

```text
Released      : v1.1.0（annotated tag）→ 437e7e60fdd354120e73360bd39f78c8012cda8b
GitHub Release: https://github.com/PEI-YING-1122/tracker-tool/releases/tag/v1.1.0
                published 2026-10-10T08:15:06Z；not draft、not prerelease；latest；無附件
Base          : v1.0.2（tag → 998ba70，未變更）
Package       : tracker-tool 1.1.0
Report date   : 2026-10-10（本報告於發布前撰寫；發布狀態於發布後補記）
Status        : RELEASED（owner 於 2026-10-10 批准）
Not done      : 合併至 main（PR #8 仍為 Draft）；內部正式交付（見 §6）
```

---

## 1. 範圍

| 項目 | 內容 |
|---|---|
| GUI | `tracker_tool_gui`（PySide6 / Qt Widgets），P6 Artist 驗收通過的設計，**沒有新增功能** |
| Core public API | `tracker_tool.contract`、`tracker_tool.app`；CLI 改用相同函式 |
| Core 轉換行為 | 與 v1.0.2 相同（含 CI-11） |
| 打包 | Windows one-folder bundle（PyInstaller），附 `BUILD_INFO.txt`、第三方聲明與授權全文、使用說明 |
| 版本 | `pyproject.toml` 1.1.0（獨立 commit） |

v1.0.2 之後，`release/1.1.x` 上的 Core 變更只有：
- `contract.py` / `app.py` 新增；
- `cli.py` / `conversion.py` 重構為共用函式；
- PFTrack 常數改由 `contract` 提供。

`tests/test_cli.py`、golden 輸入與輸出都沒有修改。

---

## 2. 驗證結果（release candidate 上重跑）

| 項目 | 結果 |
|---|---|
| 完整 test suite（offscreen） | 468 passed, 2 skipped |
| GUI tests（Windows native platform） | 102 passed |
| 10 組 released golden | 全部 byte-identical |
| Error Contract：20 個情境 | 與 v1.0.2 逐字相同；**沒有新增 formal error code** |
| A1–A4：以 GUI 視窗轉換真實 PFTrack 2017 export | 4 / 4 與 Artist 已驗收檔案 byte-identical |
| Windows bundle smoke test（RC commit 建置，無未 commit 修改） | PASS：主視窗顯示、正常結束；交付文件與 11 份授權全文齊全 |
| P6 Artist GUI 驗收 | PASS（Tracking Artist 01，2026-10-10，build `fde0c16`） |
| GitHub Actions（`e86b58c`，run 38036003943） | pytest windows-latest / ubuntu-latest、package windows-latest 全部 success；package job 也執行了 OpenSSL 來源檢查 |

P6 之後 GUI 程式只多了 CI-11 錯誤顯示的測試，介面沒有變更。

---

## 3. 第三方授權（實際 bundle 稽核）

對實際 bundle 中每個 `.dll` / `.pyd` 檢查版本資源、imports 與內嵌識別字串，結果記錄在 `packaging/THIRD_PARTY_NOTICES.md`。

**發現並修正的打包缺陷：**
- PyInstaller 從 `PATH` 取到 Git for Windows 的 OpenSSL 3.1.4，而不是 Python 自帶的 3.5.5。
- 已修正：`build_gui.py` 改為優先使用 Python 自帶的 DLL，並在 build 後比對雜湊。
- P6 試用 bundle（`fde0c16`）可能含有該版本 OpenSSL，交付前應以 RC 重新建置。

**新確認並補上條文的元件：**
- Mesa 11.2.2 內含 LLVM；
- Qt Image Formats 內含 libtiff 與 libwebp。

**仍未確認（不宣稱完全合規）：**
- 內部交付是否構成 LGPL 的「conveying」；
- Qt 內部第三方元件的個別版權聲明尚未收錄；
- 部分元件的確切版本（LLVM、libtiff、libwebp、liblzma）；
- MSVC runtime 的可再散布條款尚未審閱；
- 未使用的 Qt 模組（Network、SVG、TLS、image formats）仍隨 PyInstaller hook 打包。

---

## 4. Native Import

**不需要新的 Artist Import。** 所有會產生輸出的輸入都與 v1.0.2 逐 byte 相同：10 組 golden，以及 GUI 產生的 A1–A4。

---

## 5. Release Gate

| # | 條件 | 狀態 |
|---|---|---|
| 1 | v1.0.2 已發布並整合 | **完成** |
| 2 | RC 上的 regression、golden、Error Contract、A1–A4 | **完成**（§2） |
| 3 | Windows bundle 建置與 smoke test | **完成** |
| 4 | 第三方聲明依實際 bundle 更新 | **完成**；未確認項目見 §3 |
| 5 | GitHub Actions（Windows / Linux / package） | **完成**（run 38036003943） |
| 6 | Owner 批准 tag `v1.1.0` 與 GitHub Release | **完成**（2026-10-10 批准並發布） |
| 7 | 以正式 tag 重新建置 Windows bundle | **完成**（§6） |

發布程序（已完成）：
1. 在 `release/1.1.x` 建立 annotated tag `v1.1.0`。
2. 以 `validation/RELEASE_NOTES_v1.1.0.md` 建立 GitHub Release，**不附 GUI 執行檔**。
3. 由該 tag 建置交付 bundle，內部交付。

PR #8（合併 main）維持 Draft。

---

## 6. 內部正式交付（發布後補記）

### Windows bundle（由正式 tag 建置）

從 GitHub 重新 clone `v1.1.0`，以 `uv sync --locked` 建置。

| 檢查 | 結果 |
|---|---|
| `BUILD_INFO.txt` | commit `437e7e6…`、uncommitted changes: no、tracker-tool 1.1.0、PySide6 6.11.2 |
| Smoke test | PASS |
| OpenSSL DLL 雜湊 | `libcrypto-3-x64.dll`、`libssl-3-x64.dll` 與 Python build 的版本逐 byte 相同（3.5.5） |
| Bundle 稽核 | 與 RC 稽核結果相同；沒有 msvcrt / mingw 連結的 DLL |
| `TrackerTool.exe` SHA-256 | `6fa6ee8606c4528916cd9d3e0e7e36b889fe369e3a9d9d9575c6884adf717ce7` |

### 交付包（`packaging/assemble_delivery.py`）

- `TrackerTool/`：上述 bundle，未修改（與 tag bundle 逐檔雜湊相同）。
- `LICENSE_SUPPLEMENT/`：
  - 授權補充說明；
  - Qt 6.11.2 第三方元件完整聲明（46 個元件）。
- `LGPL_SOURCES/`：
  - Qt 6.11.2 官方原始碼：qtbase、qtsvg、qtimageformats、qttranslations，md5 與 Qt 公布值相符；
  - PySide6 6.11.2 原始碼；
  - Tracker Tool v1.1.0 原始碼。
- `DELIVERY_MANIFEST.txt`：全部檔案的 SHA-256。

驗證：
- 交付包內的程式 smoke test PASS。
- 以 `LGPL_SOURCES/tracker-tool-v1.1.0-src.zip` 重新建置成功，smoke test PASS。這證明 PySide6 的 Python 部分（打包在 exe 內）可以替換。

### 狀態

交付包已完成，授權義務的處理見 `packaging/delivery/LICENSE_SUPPLEMENT.md`。

**保存位置：** `E:_projectAI_Tracking_workTrackerTool_Releases1.1.0`（本機，不在 repository 中）。
- 186 個檔案，全部符合 `DELIVERY_MANIFEST.txt`；
- `LGPL_SOURCES/SHA256SUMS.txt` 校驗通過，Qt 原始碼符合官方 md5；
- `TrackerTool/` 與 v1.1.0 tag build 逐檔相同；
- 在保存位置執行 smoke test PASS，執行後檔案未變動。

**Microsoft VC++ runtime：** 證據見 `docs/gui/MSVC_RUNTIME_LICENSE_EVIDENCE.md`。
- 依 Microsoft 文件，隨附這些 DLL 的權利限於擁有有效 Visual Studio 授權的使用者。
- Python 與 PySide6 都沒有另外授予轉散布的權利。
- 建置機沒有安裝 Visual Studio。

因此**無法確認**目前的隨附方式符合條款。替代方案（A：確認授權事實；B：改用 Microsoft 官方 Redistributable）與必要測試見該文件。

解決前，**不標記為「內部正式交付完成」**。
