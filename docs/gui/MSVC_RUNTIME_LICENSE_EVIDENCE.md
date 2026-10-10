# Microsoft Visual C++ Runtime — 再散布證據紀錄

```text
日期   : 2026-10-10
對象   : Tracker Tool v1.1.0 Windows bundle（tag v1.1.0 → 437e7e6）
性質   : 事實與官方文件整理，不是法律意見
結論   : 依目前證據，無法確認本專案有權隨附這些 DLL（見 §4）
```

---

## 1. Bundle 中的 VC++ runtime DLL 與實際來源

以 SHA-256 與建置環境中的檔案比對，沒有任何一個 DLL 來自建置機的 `System32`。

| Bundle 路徑 | 版本 | 來源（雜湊相同） |
|---|---|---|
| `_internal/VCRUNTIME140.dll`、`VCRUNTIME140_1.dll` | 14.44.35211.0 | python-build-standalone 的 CPython 3.11.14 |
| `_internal/PySide6/VCRUNTIME140*.dll`、`MSVCP140*.dll`（5 個） | 14.44.35211.0 | `PySide6-Essentials` 6.11.2 wheel |
| `_internal/shiboken6/VCRUNTIME140*.dll`、`MSVCP140.dll`（3 個） | 14.44.35211.0 | `shiboken6` 6.11.2 wheel |

---

## 2. 上游授權資訊

### Python

Python 的 `LICENSE.txt`「Additional Conditions for this Windows binary build」一節。這段文字也隨 bundle 附在 `THIRD_PARTY_LICENSES/Python-3.11-LICENSE.txt`：

> If you further distribute programs that include the Microsoft Distributable Code, you must comply with the restrictions on distribution specified by Microsoft. In particular, you must require distributors and external end users to agree to terms that protect the Microsoft Distributable Code at least as much as Microsoft's own requirements for the Distributable Code.

這一節本身也說明，這些限制來自 Microsoft。它**沒有**另外授予轉散布的權利。

### PySide6 / shiboken6

- 兩個 wheel 都包含這些 DLL：`RECORD` 中列有 `vcruntime140*.dll` 與 `msvcp140*.dll`。
- 但 wheel 的授權資料中沒有任何關於這些 DLL 的說明，包括：
  - `METADATA` 的 `License: LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only`；
  - `licenses/LicenseRef-Qt-Commercial.txt`。

---

## 3. Microsoft 官方文件（2026-10-10 讀取）

**「Redistribute Visual C++ Files」**（learn.microsoft.com/cpp/windows/redistributing-visual-cpp-files，ms.date 2026-04-13）：

> Distribution of the Visual C++ Runtime Redistributable package, merge modules, and individual binaries is limited to licensed Visual Studio users and is subject to Microsoft Software License Terms.

> It's also possible to directly install the Redistributable DLLs in the *application local folder*. […] For servicing reasons, we don't recommend that you use this installation location.

**「Visual Studio 2022 Redistribution」**，也就是 REDIST list（learn.microsoft.com/visualstudio/releases/2022/redistribution）：

> If you have a validly licensed copy of such software, you may copy and distribute with your program the unmodified form of the files listed below, subject to the License Terms for the software.

在「Visual C++ Runtime Files」一節：

> Subject to the License Terms for the software, you may copy and distribute with your program any of the files within the following folder and its subfolders […] `[VisualStudioFolder]\VC\redist`

> Distribution of the Visual C++ Runtime Redistributable package, merge modules, and individual binaries obtained from those pages is limited to licensed Visual Studio users and is subject to its license terms.

Visual Studio 授權條款「Distributable Code」一節的全文，無法以自動方式從 visualstudio.microsoft.com 取得，因此本紀錄沒有引用。

---

## 4. 結論

1. 隨附 VC++ runtime DLL 的權利，依 Microsoft 文件，限於**擁有有效 Visual Studio 授權的使用者**，並受其授權條款約束。
2. Python 與 PySide6 都沒有另外授予轉散布的權利。Python 的授權只要求轉散布者遵守 Microsoft 的限制。
3. 建置機沒有安裝 Visual Studio（找不到 `vswhere.exe`）。owner 或公司是否擁有有效的 Visual Studio 授權，**無法從 repository 或建置環境確認**。

因此**無法確認**目前的隨附方式符合 Microsoft 條款。

---

## 5. 替代方案

### 方案 A：不改檔案，確認授權事實

由 owner 確認一項**事實**：公司或 owner 是否擁有有效的 Visual Studio 授權，例如 Professional / Enterprise 訂閱，或符合 Community 授權資格。

- 若是：v1.1.0 交付包不需修改。另外在 `USE_AND_LICENSE.md` 補上 Python 授權要求的保護條款（不得修改、不得逆向工程 Microsoft 的檔案等），隨下一版交付。
- 若否，或無法確認：改用方案 B。

### 方案 B：不隨附 runtime，改用 Microsoft 官方 Redistributable（最小變更）

- **打包變更：** `packaging/build_gui.py` 在 PyInstaller 完成後，移除 bundle 中 10 個 `VCRUNTIME140*.dll` / `MSVCP140*.dll`，並由 smoke test 確認它們不存在。**GUI 程式碼與轉換邏輯不變。**
- **使用環境需求：** 每台工作站須安裝 Microsoft Visual C++ Redistributable x64，版本 **14.44 或更新**。由使用者或 IT 從 Microsoft 官方頁面安裝，由 Microsoft 直接授權給該電腦的使用者。
- **版本：** 屬於打包變更，需要新的 patch 版本（例如 v1.1.1）與 owner 批准。

可行性實驗（2026-10-10，只在暫存複本上進行，正式交付包未修改）：
- 從 v1.1.0 bundle 的複本移除上述 10 個 DLL，在已安裝 Redistributable 14.51 的建置機上執行；
- smoke test PASS；
- 執行中載入的 `VCRUNTIME140*.dll`、`MSVCP140*.dll` 全部來自 `C:\WINDOWS\SYSTEM32`（14.51.36247.0）。

方案 B 的必要測試：

| # | 測試 | 目的 |
|---|---|---|
| 1 | 完整 test suite、golden、Error Contract | 確認 Core 與 GUI 程式不受影響（預期不變） |
| 2 | Bundle 稽核：10 個 DLL 不存在，其餘檔案與 v1.1.0 相同 | 確認是最小變更 |
| 3 | 已安裝 Redistributable 的電腦：smoke test，並確認 DLL 從 `System32` 載入 | 主要使用情境 |
| 4 | A1–A4：以打包後的程式轉換，輸出與 Artist 已驗收檔案 byte-identical | 確認轉換結果不變 |
| 5 | 未安裝 Redistributable 的乾淨 Windows（VM）：確認無法啟動，並記錄錯誤畫面 | 寫入使用說明的安裝需求 |
| 6 | 只安裝較舊 Redistributable（< 14.44）的電腦 | 確認是否需要明確的最低版本 |
| 7 | 1–2 位 Tracking Artist 在實際工作站上啟動並轉換一次 | 不需要重做完整 P6 |
