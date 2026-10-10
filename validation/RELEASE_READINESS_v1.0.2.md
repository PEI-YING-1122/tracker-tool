# Tracker Tool Core v1.0.2 — Release Readiness Report

```text
Candidate     : release/1.0.x HEAD（f14253d 之後只有文件 commit）
Base          : v1.0.1（tag → ec17fb4，未變更）
Package       : tracker-tool 1.0.2
Report date   : 2026-10-10
Status        : 技術驗收完成，等待 project owner 批准 tag 與 GitHub Release
Not done      : v1.0.2 tag、GitHub Release、合併至 main（皆須 owner 明確批准）
```

---

## 1. 範圍

依 owner 2026-10-10 核准的版本規劃，v1.0.2 **只包含 CI-11 修正與必要文件**。

| 項目 | 內容 |
|---|---|
| CI-11（GitHub #3） | PFTrack source set 中，任一成員（AutoTrack / UserTrack）解析出 0 條 track 時，conversion 停止，並以描述性 `ValueError` 指出是哪一個成員。原本的行為是忽略該成員，只轉換另一個成員，造成無聲的部分輸出 |
| 規格 | `docs/ADAPTER_PFTRACK_2017.md` §10「Member Track Count」 |
| 使用說明 | `README.md`「PFTrack source set member without tracks」 |
| 版本 | `pyproject.toml` 1.0.2 |

---

## 2. 修正差異（v1.0.1..v1.0.2）

```text
src/tracker_tool/adapters/pftrack/reader.py   +13   read_pftrack_source_set: two empty-member checks
tests/test_pftrack_source_set_members.py      +145  new regression tests
docs/ADAPTER_PFTRACK_2017.md                  +10
README.md                                     +6
pyproject.toml / uv.lock                      version 1.0.2
```

### 行為變化範圍

| 輸入 | v1.0.1 | v1.0.2 |
|---|---|---|
| Source set，兩個成員都有 track | 轉換 | **相同**（輸出逐 byte 相同） |
| Source set，AutoTrack 為 0 track、UserTrack 有 track | 只轉換 UserTrack（無聲的部分輸出） | **停止**：`PFTrack source set AutoTrack file contains no tracks` |
| Source set，AutoTrack 有 track、UserTrack 為 0 track | 只轉換 AutoTrack | **停止**：`… UserTrack file contains no tracks` |
| Source set，兩個成員都是 0 track | 停止（`Canonical track collection must not be empty`） | 仍停止，訊息改為 AutoTrack 那一句 |
| Source set，AutoTrack 為 0 track、UserTrack 格式錯誤 | 停止（UserTrack 的 parse 錯誤） | 仍停止，先回報 AutoTrack 為空 |
| 單檔 conversion（所有軟體） | — | **相同** |
| 3DE、SynthEyes 來源 | — | **相同** |

最後兩列是「本來就失敗」的輸入，只有描述性訊息不同。描述性訊息不屬於 Error Contract（INTERCHANGE_MASTER「Error Contract」）。

### 0 track 的定義（已確認）

- `read_pftrack_tracks` 只有在以下兩種情況會回傳空清單：
  - 空字串；
  - 只有已驗證的 header、沒有任何 block。
- 依據：對 4,764 種組合輸入做窮舉 fuzz。其他輸入都會產生至少 1 條 track，或拋出 parse 錯誤。
- `read_pftrack_source_set` 在 Core 中只被 source-set conversion 路徑呼叫。

---

## 3. 驗證結果

| 項目 | 結果 |
|---|---|
| 完整 test suite（本機） | 316 passed, 2 skipped |
| `core.autocrlf=false` 乾淨 clone | 316 passed, 2 skipped |
| CI-11 tests（先寫 test） | 修正前 8 failed / 4 passed；修正後全部通過 |
| 10 組 released golden（CLI byte） | 10 / 10 identical |
| Error Contract：formal code 集合與 20 個情境 | 與 v1.0.1 逐字相同；**沒有新增 formal error code** |
| 真實 production export（opt-in） | PFTrack 11 / 11、3DE 6 / 6 讀取成功 |
| A1–A4 Artist 已驗收檔案 | 以 v1.0.2 重新產生，**4 / 4 byte-identical** |
| GUI 整合預演（v1.0.2 修正 → `gui/develop`） | 無衝突，465 passed |
| GitHub Actions（Windows / Linux） | 見 §5 |

---

## 4. Native Import

**不需要新的 Artist Import。**

- v1.0.2 唯一的行為變化，是讓「source set 成員為 0 track」的輸入停止，不會寫出任何檔案。
- 所有會產生輸出的輸入，輸出都與 v1.0.1 逐 byte 相同：
  - 10 組 golden；
  - A1–A4（v1.0.1 已由 Artist 驗收，2026-10-10）。
- v1.0.1 的 Coverage Matrix 對 v1.0.2 繼續有效。

---

## 5. Release Gate

| # | 條件 | 狀態 |
|---|---|---|
| 1 | CI-11 修正已合併並通過 regression | **完成**（merge `ba5a87c`） |
| 2 | 其他已驗收的轉換行為不變 | **完成**（golden、A1–A4、Error Contract） |
| 3 | GitHub Actions（Windows / Linux）通過 | 本報告 commit push 後確認 |
| 4 | Owner 批准 tag `v1.0.2` 與 GitHub Release | **待決定** |

批准後的程序與 v1.0.1 相同：
1. 在 `release/1.0.x` 建立 annotated tag `v1.0.2`。
2. 以 `validation/RELEASE_NOTES_v1.0.2.md` 建立 GitHub Release。
3. 將 `v1.0.2` 合併進 `gui/develop`，開始準備 v1.1.0。

`v1.0.1` tag 不受影響。PR #8（合併 main）維持 Draft。
