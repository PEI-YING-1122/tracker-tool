# Tracker Tool Core v1.0.1 — Release Readiness Report

```text
Released      : v1.0.1（annotated tag）→ ec17fb48b9dce12a13e22c23a1df5ef787bb5183
GitHub Release: https://github.com/PEI-YING-1122/tracker-tool/releases/tag/v1.0.1
                published 2026-10-10T03:05:33Z；not draft、not prerelease；latest
Package       : tracker-tool 1.0.1
Report date   : 2026-10-10（本報告於發布前撰寫；發布狀態於發布後補記）
Status        : RELEASED（owner 於 2026-10-10 批准 tag 與 GitHub Release）
Not done      : 合併至 main（PR #8，尚未批准）
```

---

## 1. 結論

**可發布。** 所有 release-gate 項目都已完成並通過，詳見 §5。

只剩一項：owner 的正式發布批准（§7）。

A1–A4 紀錄已補齊：日期 2026-10-10、Artist「Tracking Artist 01」。軟體 build 當時未記錄，依實際狀況登記為「未記錄」，不做推測。

---

## 2. 版本內容（相對 v1.0.0）

### 修正

| ID | 內容 | 類型 |
|---|---|---|
| CI-1 | PFTrack reader 支援真實 PFTrack 2017 export 的 layout：兩種已驗證的 header variant，以及每個 block 前剛好一行 blank separator。未驗證的 layout 一律拒絕。 | Core implementation ≠ released spec |
| CI-2 | 不完整的 3DE / PFTrack 輸入改為拋出描述性 `ValueError`，不再是 `IndexError`。 | Error Contract（exception type） |
| CI-3 | 3DE writer 拒絕前後有空白的 track name，不再寫出不合法的 3DE 檔。 | Writer 違反 3DE whitespace contract |
| CI-12 | 3DE reader 接受已有真實 export 證據的 static field 值 `0`、`3`；其他值仍拒絕。 | 規格缺口 |
| CI-13 | SynthEyes reader 遇到名稱完全等於 `#` 的 tracker 時停止，並提供處理建議（option C2，owner 2026-10-10 核准）。 | 來源資料完整性風險 / 保守輸入防護 |
| REL-1 | package version 改為 `1.0.1`（v1.0.0 時誤為 `0.1.0`）。 | Release metadata |

### 原始碼變更範圍

```text
src/tracker_tool/adapters/pftrack/reader.py     CI-1, CI-2
src/tracker_tool/adapters/threed/reader.py      CI-2, CI-12
src/tracker_tool/adapters/threed/writer.py      CI-3
src/tracker_tool/adapters/syntheyes/reader.py   CI-13 (C2)
```

以下都**沒有**變更：Canonical model、`conversion.py`（orchestration）、ShotConfig、CLI 參數、formal error codes。

### 新增

- **Regression tests：** golden byte parity、truncation fuzz、PFTrack native export layout、3DE name round-trip、3DE static field equivalence、PFTrack role equivalence、SynthEyes `#` guard。
- **Opt-in 真實檔 regression：** 預設 skip，以環境變數 `TRACKER_TOOL_PFTRACK_REAL_EXPORTS` / `TRACKER_TOOL_3DE_REAL_EXPORTS` 啟用。
- **GitHub Actions：** `.github/workflows/tests.yml`，在 Windows 與 Linux 執行 pytest。
- **文件：**
  - `validation/COVERAGE_MATRIX_v1.0.1.md`
  - `validation/README.md` 的 v1.0.1 紀錄
  - `README.md` 的 Native Source Format Notes
  - adapter 規格（PFTrack §2、3DE §4 / §8、SynthEyes §8）

### 未包含（刻意排除）

| 項目 | 原因 |
|---|---|
| CI-4 科學記號座標 | 需先做 Native Import 驗證 |
| CI-5、CI-7 | hardening backlog；目前沒有 production 檔受影響 |
| CI-6 同一 PFTrack 檔內的同名 track | 需規格決策 |
| CI-8、CI-9、CI-10 | 已延後 |
| CI-11 source set 的 0-track 成員 | 已有 contract decision；排在 GUI P4 前獨立處理 |
| SPEC-4 含 0-sample point 的 3DE export | 依規格會停止轉換；屬產品 / 規格議題 |
| `f72e44e` refactor、G1 / G2 / G5 | 屬 GUI 階段（v1.1），不放進 bugfix release |

---

## 3. 自動化驗證結果

| 項目 | 結果 |
|---|---|
| 完整 test suite（本機） | **304 passed, 2 skipped**（skipped 為 opt-in 真實檔 tests） |
| `core.autocrlf=false` 乾淨 clone | **304 passed, 2 skipped** |
| 逐 commit 測試（v1.0.0..HEAD，共 20 個 commit） | 全部通過，可 bisect |
| GitHub Actions @ `5772288` | `pytest (windows-latest)` **success**、`pytest (ubuntu-latest)` **success** |
| 10 組 released golden byte comparison（CLI） | **10 / 10 identical** |
| Error Contract：formal code 集合與 raise site 數量 | 與 v1.0.0 **完全相同**（7 種 code） |
| Error Contract：18 個 formal-code 失敗情境 + 2 個成功情境 | v1.0.0 與 HEAD 的 exception type 與 message **逐字相同** |
| 新增錯誤類型 | 全部為描述性 `ValueError`；**沒有新增 formal error code** |
| 真實 PFTrack 2017 export（opt-in） | 11 / 11 讀取成功；track 數與 observation 數正確 |
| 真實 3DE R5 export（opt-in） | 6 / 6 讀取成功（含 static field `3` 的 2 份） |
| 真實 SynthEyes 2304 export | 2 份乾淨 export 讀取成功；5 份含 `#` tracker 的 re-export 依 C2 停止並顯示處理建議 |
| A1–A4 驗收檔案 | 以 HEAD 重新產生，與 Artist 驗收時使用的檔案 byte-identical |

**自動化測試 PASS 不等於 Native Import PASS。** Native Import 結果見 §4。

---

## 4. Native Import 驗證

依 `validation/COVERAGE_MATRIX_v1.0.1.md`：

| 路徑 | 狀態 | 依據 |
|---|---|---|
| #1 3DE → PFTrack、#2 3DE → SynthEyes | Previously Verified | v1.0.0 Artist Import + golden byte parity + `0` / `3` 輸出等價 |
| #3 SynthEyes → 3DE、#4 SynthEyes → PFTrack | Previously Verified | v1.0.0 Artist Import + golden byte parity；C2 只影響名稱為 `#` 的 tracker |
| #5、#6 PFTrack AutoTrack → 3DE / SynthEyes | **Artist Import PASS**（A3、A4） | 真實 PFTrack export（含 zdepth header） |
| #7、#8 PFTrack UserTrack → 3DE / SynthEyes | 以自動化等價證明覆蓋 | 輸出與 #5、#6 byte-identical，並有 A3 / A4 |
| #9、#10 Source Set → 3DE / SynthEyes | **Artist Import PASS**（A1、A2） | 真實 Test 08 source set（不含 zdepth header） |

### 補充證據

**A6-a — SynthEyes 2304 re-export（Artist，2026-10-10）**
- re-export 中沒有 `#` 行。
- 同時構成一次真實軟體 round-trip：14 / 664，frame set 完全一致。
- 最大誤差 0.001018 px，屬 **ACCEPTABLE_SERIALIZATION**。

**C2 對 A1–A4 的影響**
- C2 只修改 SynthEyes source reader。
- A1–A4 的來源都是 PFTrack，重新產生的檔案 byte-identical。
- 因此不需要重做 A1–A4。

---

## 5. Release Gate

| # | 條件 | 狀態 |
|---|---|---|
| 1 | CI-13 resolved | **完成**：C2 已核准、合併並通過 regression |
| 2 | CI-12 fixed and regression-tested | **完成** |
| 3 | 完整 test suite 在本機與 GitHub Actions（Windows / Linux）通過 | **完成** |
| 4 | A1–A4 Native Import PASS | **完成**：2026-10-10，Tracking Artist 01。3DEqualizer R5 / SynthEyes 2304 的 build 未記錄。Observation 數為自動化核對 |
| 5 | `validation/README.md` 已加入 v1.0.1 Native Import 紀錄 | **完成** |
| 6 | Owner 正式批准 release | **待決定** |

---

## 6. 已知限制與剩餘風險

| 項目 | 說明 | 影響 |
|---|---|---|
| SynthEyes `#` tracker（CI-13 C2） | 含名稱為 `#` 之 tracker 的來源會停止轉換。若該 tracker 確實是 tracking data，Artist 必須先在 SynthEyes 中改名。 | 明確停止，不會靜默錯誤 |
| 3DE static field | 只接受 `0`、`3`，其他值會拒絕，直到取得真實 export 證據。 | 明確停止 |
| SPEC-4 | 含 0-sample point 的 3DE export 依規格停止轉換。 | 明確停止 |
| CI-4 | 極小或極大座標會輸出科學記號，3DE R5 / PFTrack 2017 是否接受尚未驗證。 | 只在 \|x\| < 1e-4 或 ≥ 1e16 時發生 |
| 目標軟體設定 | camera plate 必須涵蓋完整 production frame range，plate resolution 必須等於轉換使用的 resolution（Same Image Geometry）。 | 操作程序，已記錄於驗證紀錄 |
| TEST-2 | golden 在 Git 中以 LF 儲存；Artist Import 時是 CRLF。 | 已由 regression 處理；`.gitattributes` 政策待定 |

---

## 7. 正式發布前尚待處理

1. **Owner 正式批准 release。**
2. **GitHub Issue / PR 更新**：需 `gh` 以官方流程登入後執行。
   - #1 CI-13 → 以 C2 resolved。
   - #2 CI-12 → fixed。
   - PR #8 checklist 更新。
   - 新增 SPEC-4 issue。

## 8. 批准後的發布程序（建議）

1. 在 `release/1.0.x` HEAD 建立 annotated tag `v1.0.1`，tag message 見 `validation/RELEASE_NOTES_v1.0.1.md`。`v1.0.0` 保持不變。
2. 建立 GitHub Release `v1.0.1`，內文使用 `validation/RELEASE_NOTES_v1.0.1.md`。
3. 經 owner 另外批准後，透過 PR #8 合併至 `main`。
4. 將 `v1.0.1` merge 進 `gui/develop`（合併預演已驗證無衝突），再依 GUI 計畫進行 `f72e44e` cherry-pick 與 G2 / G1。
