# 安裝 Microsoft Visual C++ Redistributable（使用 Tracker Tool 前）

此版本的 Tracker Tool 不附帶 Microsoft Visual C++ runtime。每台電腦需要先安裝一次 Microsoft 官方的 **Visual C++ Redistributable (x64)**。

## 1. 檢查是否已安裝

1. 開啟 Windows **設定 → 應用程式 → 已安裝的應用程式**。
2. 搜尋 `Visual C++`。
3. 找到 **Microsoft Visual C++ 2015-2022 Redistributable (x64)**（新版名稱可能是 2017-2026）。
4. 版本號是 **14.44 或更新**（例如 `14.44.35211.0`、`14.51.36247.0`）時，不需要再安裝。

## 2. 安裝或更新

1. 從 Microsoft 官方下載：https://aka.ms/vc14/vc_redist.x64.exe
2. 執行 `vc_redist.x64.exe`，同意授權條款後按「安裝」。需要系統管理員權限。
3. 若顯示「已安裝其他版本」（錯誤 0x80070666），表示電腦上已經有更新的版本，可以直接使用。

公司由 IT 集中安裝時，可使用：

```text
vc_redist.x64.exe /install /passive /norestart
```

## 3. 啟動 Tracker Tool

執行 `TrackerTool\TrackerTool.exe`。視窗下方狀態列應顯示目前的 tracker-tool 版本。

若沒有安裝，或版本太舊，程式可能無法啟動、出現缺少 DLL 的錯誤，或載入其他軟體附帶的舊版檔案。請先依上方步驟安裝，再聯絡維護者。

- 只支援 Windows 10 / 11（64 位元）。
- Redistributable 由使用者或 IT 直接從 Microsoft 取得；安裝時須同意 Microsoft 的授權條款。Tracker Tool 交付包中不包含它。
