# Tracker Tool v1.1.1 — Release Readiness Report

```text
Released      : v1.1.1（annotated tag）→ bb0c84ea80f374da381ddb963b3a4e58979e743c
GitHub Release: https://github.com/PEI-YING-1122/tracker-tool/releases/tag/v1.1.1
                published 2026-10-13T19:03:02Z（UTC；台灣時間 2026-10-14 03:03）；not draft、not prerelease；latest；無附件
Candidate     : release/1.1.x
                RC bundle 建置自 b327f91；之後的 commit 只新增 validation/ 下的 release 文件，不進入 bundle
Base          : v1.1.0（tag → 437e7e6，未變更）
Package       : tracker-tool 1.1.1
Report date   : 2026-10-14（本報告於發布前撰寫；發布狀態與交付驗證於發布後補記，見 §7）
Status        : RELEASED（owner 於 2026-10-14 批准）
Not done      : 合併至 main（PR #8 仍為 Draft）
```

---

## 1. 範圍

owner 於 2026-10-14 核准採用方案 B，並准備 v1.1.1 RC。v1.1.1 是**只有打包與文件的 patch**。

| 項目 | 內容 |
|---|---|
| 打包 | 不隨附 Microsoft Visual C++ runtime DLL：建置時移除，smoke test 檢查 |
| 系統需求 | Windows x64；Microsoft Visual C++ Redistributable (x64) 14.44 或更新，建議官方最新相容版本；不符合需求的工作站不在已驗證的支援範圍內 |
| 文件 | 新增 `VC_REDIST_INSTALL.md`；更新 `USER_GUIDE.md`、`THIRD_PARTY_NOTICES.md`、`LICENSE_SUPPLEMENT.md`、授權盤點與打包文件；加入方案 B 測試紀錄 |
| 版本 | `pyproject.toml` 1.1.1（獨立 commit） |

v1.1.0 之後 `src/`、`tests/` **沒有任何變更**：Core、GUI、Canonical Model、Conversion、CLI / GUI App、Error Contract 都相同。

`release/1.1.x` 在 v1.1.0 之後原有的交付補充也包含在 v1.1.1 中：
- 交付包組裝腳本；
- Qt 第三方元件聲明；
- 授權補充文件。

### 整合方式

方案 B 從 `test/no-msvc-runtime` 整合。`THIRD_PARTY_NOTICES.md` §5 有一處衝突，依 v1.1.1 實際交付內容解決：
- liblzma 與未使用 Qt 模組兩項，保留 release 分支的較新內容；
- VC++ runtime 一項改為「v1.1.1 起不隨附」。

---

## 2. 驗證結果

| 項目 | 結果 |
|---|---|
| 完整 test suite（offscreen） | 468 passed, 2 skipped |
| GUI tests（Windows native platform） | 102 passed |
| 10 組 released golden | 20 / 20 PASS（轉換文字與 CLI bytes） |
| Error Contract：20 個情境 | 與 v1.1.0 逐字相同；沒有新增 formal error code |
| Windows bundle smoke test（`b327f91` 乾淨 clone 建置） | PASS；移除 10 個 runtime DLL，bundle 中沒有任何 `vcruntime` / `msvcp` / `concrt` / `vccorlib` / `ucrtbase` / `api-ms-win` DLL |
| A1–A4（UI Automation 操作打包後的程式） | 4 / 4 與 Artist 已驗收檔案 byte-identical |
| DLL 載入來源 | `VCRUNTIME140*.dll`、`MSVCP140*.dll` 全部從 `C:\WINDOWS\SYSTEM32` 載入（Redistributable 14.51.36247.0），沒有用到 PATH 或其他位置的副本 |
| GitHub Actions | PASS（§6） |
| 敏感資料掃描 | PASS（§6） |

### 與已通過工作站測試的方案 B 測試包比較

逐檔 SHA-256 比對，並比對 exe 與 `base_library.zip` 中的 Python code object：

| 差異 | 說明 |
|---|---|
| Python 程式碼 | **完全相同**（exe 142 項、`base_library.zip` 155 項）；與 v1.1.0 也完全相同 |
| 所有 DLL / `.pyd` / Qt plugins | **逐 byte 相同** |
| `tracker_tool-1.1.0.dist-info` → `1.1.1.dist-info` | 版本號。`METADATA` 只差 `Version` 一行；`INSTALLER`、`REQUESTED`、`WHEEL`、`entry_points.txt`、`uv_build.json` 相同。`RECORD`、`direct_url.json`、`uv_cache.json` 含檔案雜湊、安裝路徑與快取資訊，未比對 |
| 新增 `THIRD_PARTY_LICENSES/Qt-6.11.2-third-party-attributions.txt` | release 分支原有的 Qt 第三方元件聲明 |
| `BUILD_INFO.txt`、`THIRD_PARTY_NOTICES.md`、`USER_GUIDE.md`、`VC_REDIST_INSTALL.md` | 版本與必要文件 |

**結論：** 除版本與必要文件外，沒有非預期差異。因此 #7 公司工作站測試的結果可以沿用到 v1.1.1。

---

## 3. 方案 B 測試項目（`docs/gui/PLAN_B_MSVC_RUNTIME_TEST.md`）

| # | 項目 | 結果 |
|---|---|---|
| 1 | Core / GUI regression | PASS |
| 2 | Golden byte comparison | PASS |
| 3 | A1–A4 | PASS |
| 4 | Error Contract | PASS |
| 5 | 已安裝 Redistributable 的 Windows | PASS |
| 6 | 乾淨 Windows、較舊 runtime | **BLOCKED / NOT TESTED** |
| 7 | 公司工作站 | PASS（2026-10-14） |

**#6 的處理（owner 2026-10-14 決定）：**
- 不作為 v1.1.1 的絕對 Release Blocker；
- 以交付前 runtime 版本檢查代替，並列為已知限制。

測試結果本身維持 **BLOCKED / NOT TESTED**。

---

## 4. 已知限制與交付前檢查

- **未測試：** 沒有安裝 Visual C++ Redistributable，或版本低於 14.44 的電腦。可能無法啟動，或載入其他軟體附帶的舊版 runtime。
- **交付前檢查**（寫在 `VC_REDIST_INSTALL.md` 與 `USER_GUIDE.md`）：
  1. 每台工作站使用前，在「設定 → 應用程式 → 已安裝的應用程式」確認 **Microsoft Visual C++ … Redistributable (x64)** 版本 ≥ 14.44，並記錄。
  2. 版本不足時，由使用者或 IT 從 https://aka.ms/vc14/vc_redist.x64.exe 安裝或更新。
  3. 不解除安裝工作站上既有的 Redistributable。
- **其他：** 與 v1.1.0 相同（英文介面、科學記號座標尚未在目標軟體驗證）。

---

## 5. 授權

- **VC++ runtime：** v1.1.1 不隨附。工作站上的 Redistributable 由使用者或 IT 直接從 Microsoft 取得（`docs/gui/MSVC_RUNTIME_LICENSE_EVIDENCE.md` §6）。
- **其他第三方元件：** 處理方式與 v1.1.0 交付包相同（`packaging/delivery/LICENSE_SUPPLEMENT.md`）。
- **不宣稱完全合規**；剩餘的未確認項目見 `THIRD_PARTY_NOTICES.md` §5。

---

## 6. Release Gate

| # | 條件 | 狀態 |
|---|---|---|
| 1 | 方案 B 整合至 `release/1.1.x`，`src/`、`tests/` 無變更 | **完成** |
| 2 | Regression、golden、Error Contract | **完成** |
| 3 | 乾淨 clone 建置 RC、smoke test、DLL 盤點與載入來源 | **完成** |
| 4 | A1–A4（打包後的程式） | **完成** |
| 5 | 與方案 B 測試包比對：只有版本與必要文件差異 | **完成** |
| 6 | 敏感資料掃描（push 前） | **完成**：新 commit 無命中；production 座標 token 0。全歷史掃描仍命中 2026-10-10 已記錄的本機路徑事件 commit（`docs/security/INCIDENT_2026-10-10_LOCAL_PATH_DISCLOSURE.md`），目前檔案樹中沒有 |
| 7 | GitHub Actions（Windows / Linux / package） | **完成**：`bbae890`，run 38450541009 全部 success |
| 8 | Owner 批准 tag `v1.1.1` 與 GitHub Release | **完成**（2026-10-14 批准並發布） |

### 發布程序（已完成，結果見 §7）

1. 在 `release/1.1.x` 建立 annotated tag `v1.1.1`。
2. 以 `validation/RELEASE_NOTES_v1.1.1.md` 建立 GitHub Release，**不附 GUI 執行檔**。
3. 由 tag 的乾淨 clone 重建 bundle：
   - smoke test；
   - 與本 RC 比對，應只有 `BUILD_INFO.txt` 不同。
4. 以 `packaging/assemble_delivery.py` 組裝**新的** v1.1.1 交付資料夾：
   - 不覆蓋 v1.1.0 交付包；
   - 完成 manifest 校驗。

v1.1.0 的 tag、GitHub Release 與交付包維持不變。PR #8 維持 Draft。

---

## 7. 發布與內部交付（發布後補記）

### 發布前保護

- `bb0c84e` 本機與遠端一致；工作目錄乾淨；沒有未解決的合併。
- 發布 commit 與工作目錄都沒有衝突標記。
- GitHub Actions run 38450873759（Windows / Linux / package）全部 success。
- 敏感資料掃描：
  - production 座標 token 0；
  - 發布 commit 的檔案樹沒有本機路徑；
  - 全歷史仍命中已記錄的 2026-10-10 事件 commit。

### 由 tag 重建的 Windows bundle

從 GitHub 重新 clone `v1.1.1`，以 `uv sync --locked` 建置。

| 檢查 | 結果 |
|---|---|
| `BUILD_INFO.txt` | commit `bb0c84ea…`、uncommitted changes: no、tracker-tool 1.1.1、PySide6 6.11.2 |
| VC++ runtime DLL | 建置時移除 10 個；bundle 中為 0 |
| Smoke test | PASS |
| 與已驗證 RC（`b327f91`）比較 | 檔案清單相同（168 個）；所有文件、DLL、`.pyd`、Qt plugins 逐 byte 相同；exe 與 `base_library.zip` 的 Python code object 完全相同；只有 `BUILD_INFO.txt`（commit、建置時間）及 dist-info 中含安裝路徑的 3 個檔案不同 |
| `TrackerTool.exe` SHA-256 | `bd85f81f4fe249f301c0eb9f5056b9e57ef6b03ca31f16d03197077c4e5df40d` |

### 內部交付包（`packaging/assemble_delivery.py`）

- **保存位置：** owner 指定的本機 v1.1.1 交付資料夾（不在 repository 中，路徑不記錄於公開文件）。
- **v1.1.0 交付包：** 另存於原資料夾，未覆蓋、未修改（186 個檔案，manifest 校驗通過）。

| 檢查 | 結果 |
|---|---|
| `DELIVERY_MANIFEST.txt` | 177 個檔案全部相符（另加 manifest 本身，共 178 個）；manifest SHA-256 `9bff2363…` |
| `TrackerTool/` | 與 v1.1.1 tag build 逐檔相同；不含 VC++ runtime DLL |
| 必要文件 | `VC_REDIST_INSTALL.md`、`USER_GUIDE.md`、`USE_AND_LICENSE.md`、`THIRD_PARTY_NOTICES.md`、`BUILD_INFO.txt`；`THIRD_PARTY_LICENSES/` 12 份條文 |
| `LICENSE_SUPPLEMENT/` | v1.1.1 版授權補充、Qt 6.11.2 第三方元件聲明 |
| `LGPL_SOURCES/` | `SHA256SUMS.txt` 校驗通過；Qt 原始碼符合官方 md5；`tracker-tool-v1.1.1-src.zip` 為 tag 的 `git archive`（`pyproject.toml` 1.1.1） |
| 原位 smoke test | PASS；執行後 manifest 仍全部相符 |

### 狀態

- v1.1.1 已發布，內部交付包已建立並驗證。
- **沒有未解決的發布阻擋。**
- #6 維持 **BLOCKED / NOT TESTED**，以交付前 runtime 版本檢查與已知限制處理（§3、§4）。
- 各工作站使用前，須依 `VC_REDIST_INSTALL.md` 確認 Redistributable (x64) ≥ 14.44。
