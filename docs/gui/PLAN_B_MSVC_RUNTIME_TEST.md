# 方案 B 測試報告：不隨附 Microsoft VC++ Runtime

```text
日期       : 2026-10-10（#7 結果與最終評估：2026-10-14）
分支       : test/no-msvc-runtime（由 tag v1.1.0 建立；未合併、未建立 tag / Release）
測試包     : 本機測試輸出資料夾（與正式交付資料夾分開；路徑不記錄於公開 repository）
             由 cc5820b 的乾淨 clone 建置（BUILD_INFO.txt）；之後的 commit 只修改 docs/
正式交付包 : owner 指定的本機 v1.1.0 交付資料夾（未修改）
背景       : docs/gui/MSVC_RUNTIME_LICENSE_EVIDENCE.md
```

---

## 1. 修改的檔案（相對 v1.1.0）

只修改打包流程與交付文件。`src/`、`tests/` 沒有任何變更：Core、GUI、Canonical Model、Conversion、CLI / GUI App、Error Contract 都相同。

| 檔案 | 變更 |
|---|---|
| `packaging/build_gui.py` | PyInstaller 完成後，移除名稱符合 `vcruntime*` / `msvcp*` / `concrt*` / `vccorlib*` 的 DLL；把 `VC_REDIST_INSTALL.md` 加入交付文件 |
| `packaging/smoke_test_frozen.py` | bundle 中出現上述 DLL 時失敗；要求 `VC_REDIST_INSTALL.md` 存在 |
| `packaging/delivery/VC_REDIST_INSTALL.md` | **新增**：Artist 安裝說明（繁體中文） |
| `packaging/delivery/USER_GUIDE.md` | 安裝步驟加上 Redistributable 前置需求 |
| `packaging/THIRD_PARTY_NOTICES.md` | VC++ runtime 改為「不隨附」 |

---

## 2. 測試包內容

- **移除的 DLL（10 個）：**
  - `_internal/VCRUNTIME140.dll`、`VCRUNTIME140_1.dll`
  - `_internal/PySide6/VCRUNTIME140.dll`、`VCRUNTIME140_1.dll`、`MSVCP140.dll`、`MSVCP140_1.dll`、`MSVCP140_2.dll`
  - `_internal/shiboken6/VCRUNTIME140.dll`、`VCRUNTIME140_1.dll`、`MSVCP140.dll`
- **其他同類 DLL：** bundle 中沒有 `concrt`、`vccorlib`、`ucrtbase`、`api-ms-win-*`、`msvcr*`、`vcomp`、`mfc`；剩下的 DLL 都不是 Microsoft 發行的。
- **與 v1.1.0 tag bundle 逐檔比對：**
  - 只少了上述 10 個 DLL，多了 `VC_REDIST_INSTALL.md`；
  - 內容不同的只有：`BUILD_INFO.txt`、兩份修改的文件，以及 clone 路徑造成的 dist-info 中繼資料。
- **程式碼：** 把 `TrackerTool.exe`（142 項）與 `base_library.zip`（155 項）中的 Python code object 逐一比對（忽略時間戳與路徑），**完全相同**。
  - 反向對照：同一支比對腳本能抓出 v1.0.2 與 v1.1.0 之間的 CI-11 差異。

---

## 3. 驗證結果

| # | 項目 | 結果 | 說明 |
|---|---|---|---|
| 1 | 完整 Core / GUI regression | **PASS** | 468 passed, 2 skipped；GUI tests（Windows native）102 passed |
| 2 | 10 組 golden byte comparison | **PASS** | 20 / 20（每組有轉換文字與 CLI bytes 兩項） |
| 3 | A1–A4 真實資料 | **PASS** | 以 UI Automation 操作**打包後的** `TrackerTool.exe`，4 / 4 與 Artist 已驗收檔案 byte-identical。同一腳本跑 v1.1.0 bundle 也是 4 / 4 |
| 4 | Error Contract | **PASS** | 20 個情境與 v1.1.0 逐字相同 |
| 5 | 已安裝合適 Redistributable 的 Windows | **PASS** | 建置機（Windows 11，Redistributable 14.51.36247.0）：smoke test PASS；實際載入的 `VCRUNTIME140*.dll`、`MSVCP140*.dll` 全部來自 `C:\WINDOWS\SYSTEM32`（14.51.36247.0），沒有用到 PATH 或其他位置的副本 |
| 6 | 乾淨 Windows、較舊 Runtime 環境 | **BLOCKED** | 目前沒有可用環境。依指示不以現有電腦代替。評估與準備見 §3a |
| 7 | Artist 實際工作站 smoke test | **PASS** | 2026-10-14，owner 在公司 Windows 工作站以 `artist_kit` 測試包測試：GUI 正常啟動；實際 tracking point 轉換成功；`fc /b` 比對新舊輸出檔，逐 byte 相同；未發現影響使用的問題。工作站的 Windows 版本與 Redistributable 版本**未在回報中提供** |

### 3a. 第 6 項：隔離環境評估（2026-10-10）

- **建置機：** Windows 11 Pro for Workstations 26200；CPU 支援虛擬化且已在韌體啟用。
- **Windows Sandbox：** 可安裝，但目前**停用**（`Containers-DisposableClientVM: Disabled`）；Hyper-V 也停用。
- **啟用條件：**
  - 需要系統管理員權限並重新開機；
  - 會啟用 hypervisor，可能影響這台工作站上的其他軟體。
  - 這屬於系統設定變更，**未自行啟用**，需要 owner 決定。
- **已準備的測試**（本機測試資料夾中的 `sandbox/`）：Sandbox 設定檔與登入後自動執行的腳本。
  - 測試包以唯讀方式掛載。
  - 依序測試三種狀態：
    - P1：未安裝 Redistributable；
    - P2：Visual Studio 2019 Redistributable（14.29，低於需求）；
    - P3：最新版。
  - 每個階段先記錄 runtime 狀態（System32 / Windows 目錄中的檔案、登錄、已安裝程式、PATH 中的副本），再記錄實際載入的 DLL 與結束代碼；出現錯誤視窗時截圖。
  - 若 Sandbox 內原本就有 runtime，P1 的紀錄會如實顯示，**不會被當作乾淨環境**。
  - 安裝程式只接受有效的 Microsoft 簽章。

### 第 5 項的風險觀察

建置機上，除了 `System32` 的 14.51 之外，還有其他軟體留下的舊副本：
- `C:\WINDOWS\vcruntime140.dll`（14.24）；
- ImageMagick 目錄（在 PATH 中）的 14.32 版。

Windows 的 DLL 搜尋順序是 `System32` 在 Windows 目錄與 PATH 之前，所以已安裝 Redistributable 時，不會用到這些副本（已實測）。但**未安裝 Redistributable 的電腦**可能載入這類舊副本，而不是直接報錯。這需要在第 6 項的乾淨環境中確認。

---

## 4. 版本需求（Microsoft 官方文件）

- 「The version of the Redistributable installed on the machine must be the same or later than the version of the MSVC Build Tools used to create your application.」（Latest Supported Visual C++ Redistributable Downloads）
- 「When you mix binaries built by different supported versions of the build tools, the Redistributable version must be at least as new as the latest build tools used by any app component.」（C++ binary compatibility 2015-2026）
- Python 與 PySide6 隨附的 runtime 都是 14.44.35211.0，因此需求為 **x64，14.44 或更新**。
- 永久下載連結：https://aka.ms/vc14/vc_redist.x64.exe
- 最新版只支援 Windows 10 / 11。

---

## 5. Artist 實際工作站 smoke test（待安排）

給 Artist 的說明與回報表：`docs/gui/PLAN_B_ARTIST_SMOKE_TEST.md`。它與測試包放在一起，交付給 Artist。

重點：
- 只記錄現有的 Redistributable 版本，**不在工作站上安裝或解除安裝**任何 runtime；版本不足時先回報。
- 用一顆已用 v1.1.0 轉換過的 shot 重新轉換，再用 `fc /b` 比對兩個輸出檔是否完全相同。

---

## 6. 最終 Release Readiness 評估（2026-10-14）

驗證狀態：#1–#5、#7 **PASS**；#6 **BLOCKED**（owner 未批准啟用 Windows Sandbox，也沒有其他乾淨環境）。

### 6.1 能否把 Redistributable x64 14.44 以上列為正式系統需求

**可以。** 依據：
- Microsoft 官方文件規定，Redistributable 版本不得低於建置所用的 build tools；Python 與 PySide6 都以 14.44 建置（§4）。
- 有 Redistributable（14.51）的環境實測通過：
  - 建置機：#3、#5，並確認 DLL 實際從 `System32` 載入；
  - owner 的公司工作站：#7。

**限制：**
- #7 的回報沒有記錄工作站的 Redistributable 版本，所以「14.44 是最低可用版本」只來自 Microsoft 規定，**沒有在 14.44 本身或更舊版本上實測**。
- 實測過的只有 14.51。

### 6.2 #6 未完成是否必須阻擋內部交付

**建議：不作為絕對阻擋，但以交付前檢查代替，並列為已知限制。**

- #6 要回答的是「沒有安裝或版本過舊時會怎樣」，不是「符合需求時能不能用」。後者已由 #3、#5、#7 確認。
- 主要風險：工作站沒有 Redistributable 時，可能載入其他軟體留下的舊副本（建置機上就有 14.24、14.32），而不是直接報錯。
  - 結果可能是無法啟動，或在版本不足的 runtime 上執行；
  - 這部分**未經驗證**。
- 內部交付的工作站數量有限且可確認，因此建議：
  1. 每台工作站在使用前，依 `VC_REDIST_INSTALL.md` 確認 x64 Redistributable ≥ 14.44，並記錄版本；版本不足時由 IT 安裝，不在工作站上卸載既有 runtime。
  2. 在 release notes 與使用說明中，把「未在無 Redistributable / 舊版環境測試」列為已知限制。
  3. 日後有閒置電腦或 IT 提供的乾淨 VM 時，執行已準備的 `runtime_test.ps1` 補完 #6。
- 若 owner 要求交付前必須完成所有測試，#6 就是阻擋項目。這是風險接受的決定，由 owner 決定。

### 6.3 能否在保留 Core、GUI 與轉換行為的前提下正式採用

**可以。**
- `src/`、`tests/` 沒有任何變更。
- exe 與 `base_library.zip` 中的 Python code object 與 v1.1.0 完全相同。
- 打包後的程式轉換 A1–A4，以及工作站實際轉換，都與 v1.1.0 逐 byte 相同。
- 差異只有：不附 runtime DLL、新增一份安裝說明、兩份文件更新。

### 6.4 若採用 v1.1.1：最小修改範圍

以 `release/1.1.x` 為基礎（它在 v1.1.0 之後只有交付文件、交付腳本與 Qt 授權聲明的補充，沒有程式變更）：

| # | 修改 | 說明 |
|---|---|---|
| 1 | 套用 `0142a17` | 打包流程移除 runtime DLL、smoke test 檢查。模擬套用無衝突 |
| 2 | 套用 `cc5820b` | 安裝說明、`USER_GUIDE.md`、`THIRD_PARTY_NOTICES.md`。`THIRD_PARTY_NOTICES.md` §5 有一處預期中的衝突（release 分支已改寫 VC++ runtime 一項），需手動合併 |
| 3 | 更新授權文件 | `LICENSE_SUPPLEMENT.md` §3 / §4、`MSVC_RUNTIME_LICENSE_EVIDENCE.md`：VC++ runtime 改為「不隨附」；`LICENSING_INVENTORY.md` 同步 |
| 4 | 版本 1.1.1 | `pyproject.toml`、`uv.lock`，獨立 commit |
| 5 | Release 文件 | `RELEASE_NOTES_v1.1.1.md`（系統需求、已知限制）與 `RELEASE_READINESS_v1.1.1.md` |

不需要任何 `src/` 或 `tests/` 的修改。

### 6.5 v1.1.1 發布前必要驗證

1. 完整 regression（offscreen 與 Windows native GUI）、10 組 golden、Error Contract。
2. 由 RC commit 的乾淨 clone 建置：
   - smoke test；
   - bundle 中沒有 runtime DLL；
   - 與 v1.1.0 bundle 逐檔比對：只有預期的差異；
   - code object 比對完全相同。
3. 以 UI Automation 操作打包後的程式，A1–A4 逐 byte 相同。
4. 確認實際載入的 runtime 來自 `System32`。
5. GitHub Actions（Windows / Linux / package）通過。
6. push 前，對所有要 push 的 ref 執行敏感資料掃描。
7. tag 後：
   - 由 tag 的乾淨 clone 重建；
   - 以 `assemble_delivery.py` 組裝**新的** v1.1.1 交付資料夾，不覆蓋 v1.1.0；
   - 完成 manifest 校驗與 smoke test。
8. 不需要重做 P6。#7 已涵蓋實際工作站；若 RC 的 bundle 與已測試的測試包只有文件差異，可沿用 #7 結果。

### 6.6 不變的部分

v1.1.0 的 tag、GitHub Release 與正式交付包都不修改。採用 v1.1.1 後，交付以 v1.1.1 交付包取代 v1.1.0 交付包。
