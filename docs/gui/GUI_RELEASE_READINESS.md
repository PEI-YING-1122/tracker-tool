# Tracker Tool GUI — 正式 Release 必要條件盤點

```text
盤點日期 : 2026-10-10
GUI 狀態 : P1、P5 完成；P6 Artist 驗收 PASS（fde0c16，Tracking Artist 01）
Core     : v1.0.2（已發布，998ba70）＋ G2 / G1（contract.py、app.py）
狀態     : v1.1.0 release candidate 已就緒（release/1.1.x），待 owner 批准 tag；詳見 validation/RELEASE_READINESS_v1.1.0.md
```

---

## 1. 建議的版本安排

| 版本 | 內容 | 分支 | 理由 |
|---|---|---|---|
| **Core v1.0.2** | 只包含 CI-11（source set 成員必須至少有 1 條 track） | `release/1.0.x` | 這是已核准的 contract decision，但會讓先前被接受的輸入改為停止，屬於 Core 行為變更，應獨立發布。CLI 使用者不需要等 GUI，就能取得這個修正 |
| **Tracker Tool v1.1.0** | v1.0.2 ＋ `tracker_tool.contract` / `tracker_tool.app`（新的 public API）＋ GUI | 由 `gui/develop` 建立 `release/1.1.x` | 新增 public API 與 GUI，依 semver 屬於 minor 版本。Core 轉換行為與 v1.0.2 相同 |

`v1.0.1` tag 不受影響，保持不變。

---

## 2. 必要條件與狀態

### A. Core

| # | 條件 | 狀態 |
|---|---|---|
| A1 | CI-11 修正 | **完成**：owner 批准版本規劃（2026-10-10）後，合併至 `release/1.0.x`（merge `ba5a87c`）；版本號 1.0.2（`f14253d`） |
| A2 | Core v1.0.2 發布（含 tag 與 GitHub Release） | **完成**（2026-10-10，tag → `998ba70`） |
| A3 | v1.0.2 整合進 `gui/develop` | **完成**（merge `69f53dd`，無衝突） |
| A4 | G2 / G1 不改變 Core 行為 | **完成**：Golden 10/10、Error Contract 20 情境與 v1.0.1 相同、`test_cli.py` 未修改 |

### B. 驗證

| # | 條件 | 狀態 |
|---|---|---|
| B1 | P6 Artist GUI 驗收 | **PASS**（`docs/gui/GUI_ARTIST_VALIDATION.md`） |
| B2 | Release candidate 上的完整 regression、golden、Error Contract | **完成**（468 passed；golden、Error Contract 與 v1.0.2 相同） |
| B3 | GUI 輸出與 Artist 已驗收的 A1–A4 檔案逐 byte 相同 | **完成**（RC 上 4 / 4） |
| B4 | CI-11 的 Native Import 影響 | 只會讓 0-track 成員停止；有效輸入的輸出逐 byte 不變（golden 與 A1 / A2 實測），**不需要重新做 Artist Import** |
| B5 | GitHub CI（Windows / Linux / package） | **完成**（RC `e86b58c` 全部通過） |

### C. 打包與散布

| # | 條件 | 狀態 |
|---|---|---|
| C1 | Windows bundle 由 lock 過的依賴建置 | **完成**（CI 與本機都用 `uv sync --locked`；PySide6 6.11.2） |
| C2 | **第三方授權聲明** | **已接入 bundle（內部交付版）**：`THIRD_PARTY_NOTICES.md` 與 `THIRD_PARTY_LICENSES/` 隨附，smoke test 會檢查。已依實際 bundle 稽核更新（含 OpenSSL 來源修正）。未確認項目列於聲明 §5，**不宣稱完全合規** |
| C3 | **專案本身的授權（LICENSE）** | **不新增開源授權**（owner 2026-10-10：只供內部使用、不公開散布）。內部交付附 `USE_AND_LICENSE.md` |
| C4 | 程式碼簽章 | **不列為第一版必要條件**（owner 2026-10-10） |
| C5 | 交付 bundle | **不附在 GitHub Release**（owner：不公開散布執行檔）。批准後由 tag 建置，內部交付 |

### D. 文件

| # | 條件 | 狀態 |
|---|---|---|
| D1 | GUI 安裝與使用說明 | **完成**：`packaging/delivery/USER_GUIDE.md`，隨 bundle 附上；內容描述的是 v1.1.0（含 v1.0.2 的 CI-11 行為） |
| D2 | v1.0.2 / v1.1.0 release notes | v1.0.2 已發布；v1.1.0 草稿 `validation/RELEASE_NOTES_v1.1.0.md` |
| D3 | 試用指南中 CI-11 的「已知限制」 | **完成** |

### E. 分支與 main

| # | 條件 | 狀態 |
|---|---|---|
| E1 | PR #8（v1.0.1 → main） | Draft，**需要 owner 另外批准** |
| E2 | GUI release 是否需要 main 先更新到 v1.0.x | **需要 owner 決定**。建議依序：v1.0.x 合併進 main → v1.1.0 合併進 main |
| E3 | 臨時 branch 清理（`ci/linux-bool-dealloc-probe`、`fix/ci13-hash-tracker-guard`） | 待 owner 同意 |

---

## 3. 沿用到 v1.1.0 的已知限制

- 介面為英文（owner 決定維持）。
- SPEC-4：3DE export 中含 0-sample point 時，依規格停止轉換。
- CI-4：科學記號座標在 3DE R5 / PFTrack 2017 是否能匯入尚未驗證。
- CI-5、CI-7：hardening backlog。
- PySide6 固定 `<6.12`，原因見 `GUI_PACKAGING.md`。

---

## 4. 需要 owner 決定的事項

已決定（2026-10-10）：CI-11 與版本安排、專案授權（不新增）、第三方聲明（內部交付版）、程式碼簽章（第一版不需要）。

尚待決定：
1. 是否批准 tag `v1.1.0` 與 GitHub Release（`validation/RELEASE_READINESS_v1.1.0.md`）。
2. main 的合併順序（E1、E2）。
3. 臨時 branch 清理（E3）。
