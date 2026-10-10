# Tracker Tool — 程式碼來源、權利歸屬與第三方授權盤點

```text
盤點日期 : 2026-10-10
範圍     : GitHub repository PEI-YING-1122/tracker-tool（所有公開 branch / tag），以及 Windows GUI bundle
性質     : 事實盤點，供 owner 決定專案 LICENSE 使用。不是法律意見；所列義務均待確認
```

---

## 1. 專案目前的授權狀態

- Repository **沒有 LICENSE 檔**，`pyproject.toml` 也沒有宣告 license。
- Repository 是 **public**。
- 沒有授權條款時，一般視為「保留所有權利」：他人可以瀏覽，但沒有使用、修改、散布的授權。
- 打包的 GUI 散布了 LGPL 等第三方元件，因此專案授權的選擇會影響第三方義務能否滿足，見 §4。

---

## 2. 程式碼來源與權利歸屬

### Git 紀錄

| 項目 | 事實 |
|---|---|
| Commit author | 全部 71 個公開 commit 的 author 都是 `PEI-YING-1122 <milkmillk1256@gmail.com>` |
| 期間 | 2026-09-13 起，至 2026-10-10 |
| v1.0.0 之前（19 個 commit） | 沒有 AI 共同作者標記。依 handoff 文件，這段由 owner 搭配 Codex（OpenAI）開發 |
| v1.0.0 之後 | 51 個 commit 帶有 `Co-Authored-By: Claude Opus 5.5`，由 owner 指示 Claude Code 開發 |
| 外部貢獻者 | 沒有。沒有 PR 來自他人，也沒有其他 author |

### 內容來源

| 類別 | 來源 | 備註 |
|---|---|---|
| Core 與 GUI 原始碼、tests | 本專案開發：owner 搭配 AI 工具 | 沒有複製第三方原始碼進 repository |
| 規格文件（`docs/*.md`、`AGENTS.md`、`PROJECT_GOAL.md`） | 本專案撰寫 | 描述的是 3DE / PFTrack / SynthEyes 的檔案格式與觀察結果，沒有包含這些軟體的程式碼或文件原文 |
| Golden / test 資料（`validation/`、tests 內的資料） | 本專案製作的**合成資料** | 2026-10-10 掃描確認：公開 history 中沒有任何真實 production 座標 |
| 真實 production 素材 | **不在 repository 中** | 存放於本機的驗證資料夾 |
| `packaging/licenses/*.txt` | 第三方授權條款原文（GNU、Apache、PSF） | 這些條文本身允許原文散布 |

### 待 owner / 法務確認

- **AI 工具產出內容的權利：** AI（Codex、Claude）參與產出的程式碼，其權利歸屬取決於各工具的使用條款與適用法律。本盤點不做結論。
- **前東家或客戶的權利：** 開發是否在受雇或委託關係下進行（例如使用公司設備、工作時間、客戶專案的資料或驗證流程），可能影響權利歸屬。
- **商標名稱：** 3DEqualizer、PFTrack、SynthEyes 等名稱屬於各自的權利人。專案只用來描述相容性。

---

## 3. 第三方依賴

### Core（`tracker-tool`，無 extra）

- **Runtime 依賴：無。** 只使用 Python 標準函式庫。
- 以原始碼或 wheel 散布 Core 時，不會一併散布任何第三方套件。

### GUI（Windows bundle）實際散布的元件

詳細清單與檔案位置見 `packaging/THIRD_PARTY_NOTICES.md`（DRAFT）。

| 元件 | 授權 | 備註 |
|---|---|---|
| PySide6 / Shiboken6 6.11.2 | LGPL-3.0 / GPL-2.0 / GPL-3.0（擇一）或商業授權 | 開源使用時通常採 LGPL-3.0 |
| Qt 6 DLL 與 plugins | LGPL-3.0（開源） | 含 Qt 內部的第三方函式庫，清單見 Qt 官方「Licenses Used in Qt」 |
| Mesa `opengl32sw.dll` | MIT 類 | 隨 PySide6 一起安裝 |
| Python 3.11 runtime | PSF-2.0 | 含 bzip2、xz、libmpdec 等 |
| OpenSSL 3.5.5 | Apache-2.0 | 因 Python 的 `_hashlib` / `_socket` 一併被打包 |
| Microsoft VC++ runtime | Microsoft 可再散布條款 | |
| PyInstaller bootloader | GPL-2.0-or-later，附 bootloader 例外條款 | 例外條款允許以任何授權散布打包後的程式 |

### 只用於開發、測試、建置（不散布）

pytest、pytest-qt、pluggy、iniconfig、packaging、pygments、colorama、typing-extensions、PyInstaller、pyinstaller-hooks-contrib、altgraph、pefile、pywin32-ctypes、setuptools、uv。

授權都是 MIT / BSD / Apache-2.0 / PSF / GPL（僅限工具本身），不會隨 bundle 散布。

---

## 4. 初步義務整理（**未經確認**）

| 來源 | 可能的義務 | 目前狀態 |
|---|---|---|
| Qt / PySide6（LGPL-3.0） | 附上 LGPL-3.0 與 GPL-3.0 全文；提供對應版本的原始碼取得方式；讓使用者能替換 Qt 函式庫；專案本身的授權條款不得禁止為除錯而修改或逆向工程 | 條文已收集（`packaging/licenses/`）。one-folder bundle 的 Qt DLL 是獨立檔案。**尚未放入 bundle** |
| Python、OpenSSL、bzip2、xz、libmpdec | 附上授權與版權聲明 | Python / Apache-2.0 條文已收集；xz、libmpdec 條文**尚未收集** |
| Qt 內部第三方函式庫、Mesa | 附上各自的版權聲明 | **尚未收集** |
| Microsoft VC++ runtime | 依可再散布條款散布 | 待確認 |
| PyInstaller bootloader | 例外條款下通常沒有額外義務 | 待確認 |

**因此目前不宣稱完全合規。**

---

## 5. 需要 owner 決定的事項

1. **專案授權**，例如：
   - 開源，如 MIT 或 Apache-2.0；
   - 僅公開原始碼、不授權使用；
   - 改為 private repository。

   選擇時需確認與 §4 的 LGPL 義務相容，尤其是 LGPL-3.0 §4 對「不得禁止修改與逆向工程」的要求。
2. **§2 中待確認的權利歸屬**：AI 工具條款、雇傭 / 委託關係。
3. **GUI bundle 的第三方聲明**要以什麼形式隨附，並補齊尚未收集的條文。

以上決定後，我會：
- 把 `THIRD_PARTY_NOTICES` 和授權條文接到打包流程；
- 補齊缺少的條文；
- 再請你或法務確認是否足夠。
