# 系統需求與 Microsoft Visual C++ Redistributable 安裝說明

從 v1.1.1 起，Tracker Tool 不再附帶 Microsoft Visual C++ runtime，改用電腦上安裝的 Microsoft 官方版本。

## 系統需求

- Windows 10 / 11，64 位元（x64）。
- **Microsoft Visual C++ Redistributable (x64) 14.44 或更新版本。**
  - 建議安裝 Microsoft 官方提供的最新版本。
- 不符合以上需求的電腦，不在目前已驗證的支援範圍內。

---

## 1. 交付前檢查（每台電腦第一次使用前）

1. 開啟 Windows **設定 → 應用程式 → 已安裝的應用程式**。
2. 搜尋 `Visual C++`。
3. 找到 **Microsoft Visual C++ 2015-2022 Redistributable (x64)**（新版名稱可能是 2017-2026）。
4. 記錄版本號，並判斷：
   - **14.44 或更新**（例如 `14.44.35211.0`、`14.51.36247.0`）：符合需求，可以開始使用。
   - 沒有 x64 版本，或版本低於 14.44：依步驟 2 安裝或更新後再使用。

請不要解除安裝電腦上既有的任何 Visual C++ Redistributable，其他軟體可能需要它們。

## 2. 安裝或更新

1. 從 Microsoft 官方下載：https://aka.ms/vc14/vc_redist.x64.exe
2. 執行 `vc_redist.x64.exe`，同意授權條款後按「安裝」。需要系統管理員權限。
3. 若顯示「已安裝其他版本」（錯誤 0x80070666），表示電腦上已經有更新的版本，可以直接使用。
4. 完成後依步驟 1 再確認一次版本。

公司由 IT 集中安裝時，可使用：

```text
vc_redist.x64.exe /install /passive /norestart
```

Redistributable 由使用者或 IT 直接從 Microsoft 取得，安裝時須同意 Microsoft 的授權條款。Tracker Tool 交付包中不包含它。

## 3. 啟動 Tracker Tool

執行 `TrackerTool\TrackerTool.exe`。視窗下方狀態列應顯示目前的 tracker-tool 版本。

## 已知限制

- 已驗證的環境：
  - 建置用 Windows 11 電腦（Redistributable 14.51）；
  - 公司 Windows 工作站（已安裝 Redistributable，版本未記錄）。
- **尚未測試：** 沒有安裝 Redistributable，或只有較舊版本（低於 14.44）的電腦。
  - 這種電腦上，程式可能無法啟動、出現缺少 DLL 的錯誤；
  - 也可能載入其他軟體附帶的舊版檔案，行為無法保證。
  - 因此使用前務必完成步驟 1 的檢查。
