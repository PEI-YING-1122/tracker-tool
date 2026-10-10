# Tracker Tool GUI — Artist 試用指南（P6）

這份指南提供給 Tracking Artist 試用 Windows 版 Tracker Tool GUI。

## 試用目的

確認在實際工作流程中，GUI 能否順利完成轉換，以及操作與訊息是否清楚。

**轉換結果本身由 Core v1.0.1 負責，已通過驗證。** 自動化測試已確認：GUI 產生的檔案與 CLI、與 v1.0.1 的 golden 檔、與 A1–A4 Artist 已驗收的檔案逐 byte 相同。所以這次試用主要評估 GUI 的操作體驗。

---

## 1. 安裝與啟動

1. 將 `TrackerTool` 資料夾整個複製到本機任意位置。路徑可以包含中文。
2. 執行 `TrackerTool\TrackerTool.exe`。不需要安裝 Python。
3. 視窗下方狀態列應顯示 `tracker-tool 1.0.1`。
4. 如果 Windows 或防毒軟體阻擋執行，請記錄下來並回報。這個試用版本沒有數位簽章。

`TrackerTool` 資料夾內的 `BUILD_INFO.txt` 記錄這個版本的 commit 與建置時間，請不要刪除。

---

## 2. 操作流程

視窗由上而下依序是 **Source → Target → Shot → Output → Convert → Result**。

### Source

- **Software**：選擇來源軟體。工具不會依檔名或檔案內容自動判斷。
- **PFTrack 來源時**，再選擇一種模式：
  - **Single file**：選一個檔案，並**必須**選擇 Role（AutoTrack 或 UserTrack）。Role 沒有預設值。
  - **Source set (AutoTrack + UserTrack)**：分別選 AutoTrack 和 UserTrack 兩個檔案。
- **Input**：按 `Browse…` 選檔，或直接貼上路徑。

### Target

- 選擇目標軟體。與來源相同的軟體會呈現灰色、無法選擇，滑鼠移上去會顯示原因。

### Shot

| 欄位 | 填寫方式 |
|---|---|
| Width / Height | plate 的實際解析度，必須與目標軟體中 plate 的設定相同 |
| Start frame | production 起始 frame，例如 `1001` |
| End frame | 知道的話填入；不知道就勾選 `Unknown` |

- 欄位只能輸入整數。數值是否合理由 Core 判斷，不合理時會顯示錯誤。
- 工具**不會**記住上一顆 shot 的數值，每顆 shot 都要重新輸入。

### Output 與 Convert

1. 在 `Output` 按 `Browse…` 選擇輸出檔案。
   - 若輸出檔已經存在，且路徑是直接輸入的，按下 Convert 時會先詢問是否覆寫。
2. 按 `Convert`。轉換期間所有輸入欄位都會鎖定。

### Result

| 顯示 | 意思 |
|---|---|
| `PASS` | 檔案已寫出。可按 `Open output folder` 開啟資料夾 |
| `FAIL — <ERROR CODE>` | 正式錯誤代碼，例如 `INVALID_SHOT_METADATA`。相關區塊的標題會變成紅色 |
| `FAIL — Core rejected the input` | 來源檔案格式問題。訊息是 Core 的原文說明 |
| `FAIL — File error` | 檔案無法讀取或寫入 |
| `FAIL — Unexpected Core failure` | 非預期錯誤，請務必回報 |

- `PASS` 時一定會附上提醒：**轉換成功不等於已在目標軟體驗證**。匯入目標軟體確認，仍是 Artist 的判斷。
- `Copy diagnostics` 會把版本、設定與錯誤細節複製到剪貼簿，回報問題時請貼上這段內容。

---

## 3. 建議的試用情境

請盡量使用**實際工作中的檔案**。可以只做部分情境。

| # | 情境 | 請確認 |
|---|---|---|
| T1 | 3DEqualizer R5 → PFTrack 2017 / SynthEyes 2304 | 能否順利完成；輸出能否匯入目標軟體 |
| T2 | SynthEyes 2304 → 3DEqualizer R5 / PFTrack 2017 | 同上 |
| T3 | PFTrack 2017 單檔（選 Role）→ 3DE / SynthEyes | Role 的選擇是否清楚 |
| T4 | PFTrack 2017 source set（AutoTrack + UserTrack）→ 3DE / SynthEyes | 兩個輸入欄位是否清楚 |
| T5 | 故意填錯，例如 Width 填 `0`，或 End frame 早於資料範圍 | 錯誤訊息與紅色標示是否容易理解 |
| T6 | 輸出到已存在的檔案、`Open output folder`、`Copy diagnostics` | 是否符合預期 |
| T7 | 路徑含中文或網路磁碟（若工作上會用到） | 能否正常讀寫 |

---

## 4. 已知限制（不需回報）

- 介面是英文。
- 一般 3DE / SynthEyes 檔案會直接寫出，只有以下情況會停止轉換並顯示原因。工具不會自動修正或刪除任何資料：
  - PFTrack export 只接受已驗證的格式。
  - 3DE track 名稱若有前後空白，無法輸出到 3DE。
  - SynthEyes 中名稱剛好是 `#` 的 tracker。
  - 3DE export 中沒有任何 sample 的點。
- **PFTrack source set**（P6 試用 build 的限制）：若 AutoTrack 或 UserTrack 其中一個檔案沒有任何 track，P6 試用 build 仍會轉換，只輸出另一個檔案的 track。Core v1.0.2 已修正（CI-11）：v1.1.0 起，這種情況會停止轉換，並指出是哪一個檔案。
- 座標極小（\|x\| < 1e-4）時會以科學記號輸出，目標軟體能否接受尚未驗證。

---

## 5. 回報方式

請在 `TRIAL_FEEDBACK.md`（與試用版放在一起）中填寫每個情境的結果。有問題時，附上 `Copy diagnostics` 的內容。

請勿把含有 production 資料的檔案或截圖放進公開的 GitHub repository。
