# Tracker Tool — 使用範圍與授權說明

## 使用範圍

本工具供 owner 本人與公司內部 Tracking Artist 使用，在 Windows 上執行。

不公開散布執行檔。

## Tracker Tool 本身的授權

- Tracker Tool 目前**沒有**採用開源授權（例如 MIT、Apache-2.0），也沒有另行訂定使用條款。
- 原始碼位於 GitHub repository `PEI-YING-1122/tracker-tool`。
- 程式碼來源與權利歸屬的盤點，見 repository 中的 `docs/LICENSING_INVENTORY.md`。

## 第三方元件

交付包內含第三方元件，例如 Qt / PySide6、Python、OpenSSL。各元件依各自的授權提供，詳見：

- `THIRD_PARTY_NOTICES.md`：元件、版本、授權、原始碼來源，以及尚未確認的項目
- `THIRD_PARTY_LICENSES/`：授權全文

依 Qt / PySide6 的 LGPL-3.0 授權：使用者可以用修改過、或相容的版本替換 `_internal/PySide6/`、`_internal/shiboken6/` 下的 Qt / PySide6 函式庫，本工具不禁止此類修改，或為除錯此類修改而進行的逆向工程。

## 版本資訊

- 本交付包的確切版本記錄在 `TrackerTool/BUILD_INFO.txt`：commit、是否有未 commit 的修改、建置時間、tracker-tool 與 PySide6 版本。
- 程式中的 `Copy diagnostics` 也會帶出同樣的資訊。
