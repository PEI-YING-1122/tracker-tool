# Tracker Tool v1.1.0（GUI）— Release Readiness Report

```text
Candidate     : release/1.1.x（由 gui/develop 建立）
Base          : v1.0.2（tag → 998ba70，未變更）
Package       : tracker-tool 1.1.0
Report date   : 2026-10-10
Status        : RELEASE CANDIDATE — 尚未建立 tag 或 GitHub Release
Not done      : tag v1.1.0、GitHub Release、合併至 main（PR #8 仍為 Draft）
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
| 6 | Owner 批准 tag `v1.1.0` 與 GitHub Release | **待決定** |
| 7 | 以 RC 重新建置內部交付 bundle | 批准後進行 |

批准後的程序：
1. 在 `release/1.1.x` 建立 annotated tag `v1.1.0`。
2. 以 `validation/RELEASE_NOTES_v1.1.0.md` 建立 GitHub Release，**不附 GUI 執行檔**。
3. 由該 tag 建置交付 bundle，內部交付。

PR #8（合併 main）維持 Draft。
