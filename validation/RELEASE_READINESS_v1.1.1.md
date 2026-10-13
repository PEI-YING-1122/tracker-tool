# Tracker Tool v1.1.1 — Release Readiness Report

```text
Candidate     : release/1.1.x
                RC bundle 建置自 b327f91；之後的 commit 只新增 validation/ 下的 release 文件，不進入 bundle
Base          : v1.1.0（tag → 437e7e6，未變更）
Package       : tracker-tool 1.1.1
Report date   : 2026-10-14
Status        : RELEASE CANDIDATE — 尚未建立 tag 或 GitHub Release
Not done      : tag v1.1.1、GitHub Release、v1.1.1 交付包、合併至 main（PR #8 仍為 Draft）
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
| 8 | Owner 批准 tag `v1.1.1` 與 GitHub Release | **待決定** |

### 批准後的程序

1. 在 `release/1.1.x` 建立 annotated tag `v1.1.1`。
2. 以 `validation/RELEASE_NOTES_v1.1.1.md` 建立 GitHub Release，**不附 GUI 執行檔**。
3. 由 tag 的乾淨 clone 重建 bundle：
   - smoke test；
   - 與本 RC 比對，應只有 `BUILD_INFO.txt` 不同。
4. 以 `packaging/assemble_delivery.py` 組裝**新的** v1.1.1 交付資料夾：
   - 不覆蓋 v1.1.0 交付包；
   - 完成 manifest 校驗。

v1.1.0 的 tag、GitHub Release 與交付包維持不變。PR #8 維持 Draft。
