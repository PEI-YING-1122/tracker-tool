# Tracker Tool — 使用說明（Windows）

Tracker Tool 用來在 **3DEqualizer R5**、**PFTrack 2017**、**SynthEyes 2304** 之間轉換 Artist 建立的 2D tracking point。

轉換只處理 track 名稱、frame 與 2D 座標，**不會**刪除、補點、合併或改名任何 track。

---

## 1. 安裝與啟動

0. 第一次使用前，確認電腦已安裝 Microsoft Visual C++ Redistributable (x64) 14.44 或更新版本，步驟見 `VC_REDIST_INSTALL.md`。
1. 將整個 `TrackerTool` 資料夾複製到本機。路徑可以包含中文。
2. 執行 `TrackerTool\TrackerTool.exe`。不需要安裝 Python。
3. 視窗下方狀態列會顯示目前的 tracker-tool 版本。

請保留 `BUILD_INFO.txt`、`THIRD_PARTY_NOTICES.md`、`THIRD_PARTY_LICENSES/` 等檔案，不要刪除。

---

## 2. 操作流程

視窗由上而下依序是 **Source → Target → Shot → Output → Convert → Result**。

### Source

- **Software**：選擇來源軟體。工具不會依檔名或檔案內容自動判斷。
- **PFTrack 來源時**，再選擇一種模式：
  - **Single file**：選一個檔案，並**必須**選擇 Role（AutoTrack 或 UserTrack）。
  - **Source set (AutoTrack + UserTrack)**：分別選 AutoTrack 和 UserTrack 兩個檔案。兩個檔案都必須包含 track。
- **Input**：按 `Browse…` 選檔，或直接貼上路徑。

### Target

- 選擇目標軟體。與來源相同的軟體無法選擇。

### Shot

| 欄位 | 填寫方式 |
|---|---|
| Width / Height | plate 的實際解析度，必須與目標軟體中 plate 的設定相同 |
| Start frame | production 起始 frame，例如 `1001` |
| End frame | 知道的話填入；不知道就勾選 `Unknown` |

- 工具**不會**記住上一顆 shot 的數值，每顆 shot 都要重新輸入。
- 匯入目標軟體時，plate 的 frame 範圍必須涵蓋所有 track 的 frame，解析度也必須與這裡填的相同。

### Output 與 Convert

1. 在 `Output` 按 `Browse…` 選擇輸出檔案。若直接輸入的路徑已有檔案存在，按 Convert 時會先詢問是否覆寫。
2. 按 `Convert`。

### Result

| 顯示 | 意思 |
|---|---|
| `PASS` | 檔案已寫出。可按 `Open output folder` 開啟資料夾 |
| `FAIL — <ERROR CODE>` | 正式錯誤代碼，例如 `INVALID_SHOT_METADATA`，相關區塊會標示為紅色 |
| `FAIL — Core rejected the input` | 來源檔案格式或內容問題，訊息為詳細說明 |
| `FAIL — File error` | 檔案無法讀取或寫入 |
| `FAIL — Unexpected Core failure` | 非預期錯誤，請回報 |

- `PASS` 不等於已在目標軟體驗證，匯入後請確認 track 數量、位置與 frame。
- 遇到問題時，按 `Copy diagnostics`，把內容貼給維護者，內含版本與設定資訊。

---

## 3. 會停止轉換的情況

以下情況工具不會自動修正，而是停止並說明原因：

- PFTrack export 的格式不是已驗證的 layout。
- PFTrack source set 的 AutoTrack 或 UserTrack 檔案沒有任何 track。
- 3DE track 名稱有前後空白，無法輸出到 3DE。
- SynthEyes 中有名稱剛好是 `#` 的 tracker：請在 SynthEyes 檢查，不是 tracking data 就刪除，否則改名，再重新匯出。
- 3DE export 中有沒有任何 sample 的 point。
- Shot 資料不完整或不合理，例如 Width 為 0，或 track 的 frame 超出 Start / End frame。

## 4. 已知限制

- 介面為英文。
- 座標極小（\|x\| < 1e-4）時會以科學記號輸出，目標軟體能否接受尚未驗證。
