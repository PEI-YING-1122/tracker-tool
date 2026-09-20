# INTERCHANGE_MASTER.md — Artist 2D Track Interchange v1

## 1. Goal

本規格定義 3DEqualizer R5、PFTrack 2017、SynthEyes 2304 之間的 Artist-created 2D Tracking Point interchange。

目標：

```text
Source Software
→ Source Reader / Import Adapter
→ Canonical 2D Track Core
→ Target Writer / Export Adapter
→ Target Software
```

本系統不是建立六套 pairwise converter。

任何 Target Writer 都只能接受：

```text
Canonical Track Data + ShotConfig
```

不得依賴 Source Software 特例。

---

## 2. v1 Scope

v1 只交換：

- Track identity
- Artist-visible track name
- Observation frame
- 2D pixel coordinate
- Natural gap

v1 不交換：

- Camera solve
- Focal length
- Filmback
- Lens distortion
- Survey
- 3D points
- Coordinate system / orientation / scale
- Object track
- Camera constraints
- Group
- Color
- Weight
- Tracking state
- Software-specific quality metadata
- Similarity
- SynthEyes Outcome
- PFTrack Z Depth
- AutoTrack / UserTrack classification as Canonical semantics

---

## 3. Core Architecture

唯一正式架構：

```text
Native Source
↓
Source Adapter Reader
↓
Canonical 2D Track Core
↓
Target Adapter Writer
↓
Native Target
```

禁止：

```text
3DE → PFTrack direct converter
3DE → SynthEyes direct converter
PFTrack → 3DE direct converter
...
```

Writer 不得包含：

```text
if source_software == ...
```

來改變 Target Native Format。

---

## Conversion Orchestration Contract

唯一 conversion architecture：

```text
Source Native
→ Source Native Reader
→ Canonical 2D Track Core
→ Canonical Validation
→ Target Native Writer
→ Target Native
```

禁止建立 pairwise converters，例如：

```text
3DE → PFTrack
3DE → SynthEyes
PFTrack → 3DE
...
```

所有轉換必須經過 Canonical。

正式 internal software identifiers：

```text
3DE_R5
PFTRACK_2017
SYNTHEYES_2304
```

不要自動接受 alias，也不要由 filename/content 猜 software。

Reader responsibility：

- Source-specific parsing
- Native validation
- Native → Canonical mapping

Canonical Validation responsibility：

- 驗證既有 Canonical contract
- 不修改資料

Writer responsibility：

- Canonical → target native
- Writer 只可依賴 Canonical + target 所需 runtime ShotConfig
- Writer 不得依 source software branching
- Writer 不得知道原始 source-specific semantics

Orchestration responsibility：

- dispatch correct Reader
- run Canonical validation
- dispatch correct Writer
- 不做 filtering / merge / rename / interpolation / repair

PFTrack source role：

```text
AUTOTRACK / USERTRACK
```

只屬 PFTrack Reader provenance / diagnostics。

不得進入 Canonical track semantics。

Step 11 第一版 single-source contract：

先支援：

- 3DE_R5 single source
- PFTRACK_2017 AUTOTRACK single source
- PFTRACK_2017 USERTRACK single source
- SYNTHEYES_2304 single source

```text
PFTRACK_SOURCE_SET
```

AutoTrack + UserTrack aggregation 保留既有 Reader 能力，但不納入第一個 orchestration function 的最小實作，後續獨立接入。

### Same-source / Same-target Contract

Conversion Core v1 只允許：

```text
source_software != target_software
```

以下 conversion 必須拒絕：

```text
3DE_R5 → 3DE_R5
PFTRACK_2017 → PFTRACK_2017
SYNTHEYES_2304 → SYNTHEYES_2304
```

原因：

1. v1 定位是不同 tracking software 之間的 interchange。
2. Canonical v1 不保存所有 native-only metadata。
3. PFTrack Similarity 不屬 Canonical data，Writer 可產生 synthetic 1.000000。
4. SynthEyes Outcome 不屬 Canonical data，Writer 使用 deterministic 15。
5. 因此 same-source parse → Canonical → rewrite 不等於 byte-preserving 或 native-metadata-preserving no-op。
6. 不得讓使用者誤認 same-source conversion 是原檔無損重存。

如果未來需要：

- native validation
- native normalization
- same-format rewrite

必須作為獨立 operation / contract 定義，不得自動視為 interchange conversion。

本次：

- 不定義正式 error code
- 不定義 error message wording
- 不修改 CLI contract
- 不修改其他既有 conversion semantics

不定義 CLI option syntax。CLI command-line argument contract 仍留待後續 wrapper 層定義。

不新增任何 selection / filtering / interpolation / track merge 行為。

本次不要定義 file path IO contract。Conversion Core 先以 native text 作為 input/output，file reading/writing 留給 CLI/application layer。

---
## 4. Lossless Interchange Principle

Artist-created Source Track Data 預設：

```text
100% PRESERVE
```

禁止：

- Selection
- Retention
- Coverage Floor
- Ranking
- Quality filtering
- Similarity filtering
- Duplicate cleanup
- Track pruning
- Interpolation
- Natural gap filling
- Track extension
- Fabricated observation
- Automatic cleanup

Source native observation 存在：

```text
= measurement exists
```

Source native observation 不存在：

```text
= no measurement
```

不得由 converter 推測或補值。

---

## 5. Source Truth

每次 conversion 只能有一個 authoritative Source Truth。

若 Source Software 需要多個 native files 才能完整取得 Artist Data，例如 PFTrack AutoTrack / UserTrack 分開輸出：

```text
Multiple Native Source Files
→ one Source Adapter
→ one Canonical Track Collection
```

各 source file 必須先獨立 parse，再進行 Source-set Aggregation。

不得因 target software 不同而重新解讀 Source Data。

---

## 6. Required ShotConfig / Preflight

正式 runtime ShotConfig：

```text
ShotConfig {
    image_width
    image_height
    production_start_frame
    production_end_frame
    source_software
    target_software
}
```

其中最低 universal required resolved metadata：

```text
image_width
image_height
production_start_frame
```

正式 production implementation 應優先取得：

```text
production_end_frame
```

但不得從最後一筆 Track observation 自動推論實際 plate end。

如果 authoritative end frame 尚未取得，可記錄：

```text
observed_production_frame_min
observed_production_frame_max
```

這不等於 actual shot range。

Required metadata 不代表必須由 Artist 手動輸入。

可由：

- Plate / image sequence
- Project metadata
- Sidecar
- Pipeline database
- Avalon
- Artist UI

解析。

解析完成前不得執行需要該 metadata 的 conversion。

缺少必要 metadata：

```text
MISSING_REQUIRED_SHOT_METADATA
```

---

## 7. Same Image Geometry Contract

Resolution-independent 的正確定義：

> Source 與 Target 必須描述相同的 image geometry。

如果兩邊存在：

- Resize
- Crop
- Proxy
- Overscan
- Reformat
- Different plate geometry

v1 不做自動補償。

必須：

```text
IMAGE_GEOMETRY_MISMATCH
```

並停止。

禁止 silent scaling X/Y。

禁止從 Track coordinate extrema 推測 resolution。

---

## 8. Canonical Coordinate Semantics

Canonical 一律：

```text
Pixel Space
Origin = Top Left
X = Right
Y = Down
```

3DE 與 PFTrack 在 same image geometry 下：

```text
X/Y = direct pixel pass-through
```

SynthEyes 由 Adapter 負責 normalized U/V conversion。

---

## 9. Production Frame Principle

Canonical 儲存：

```text
actual production frame
```

不同軟體 frame mapping 由各 Adapter 負責。

禁止讓 Canonical 保存 app-local frame numbering。

---

## 10. Track Identity Principle

Canonical 必須區分：

```text
track_id
track_name
```

`track_id`：

- Converter internal identity
- 必須 unique
- 可用於 multiple source files 的 collision isolation
- 不等於 Artist-visible native name

`track_name`：

- Artist-visible text
- Source 支援時 exact preserve
- 包含 leading zero
- 不得自行 numeric normalize

例如：

```text
track_id   = pf_autotrack::Auto000084
track_name = Auto000084
```

Target Writer 預設只能將：

```text
track_name
```

寫入 Artist-visible native name。

不得把 `track_id` 直接寫進 native software。

只有 target name collision 無法避免時，可建立：

```text
deterministic
reversible
documented
```

的 Target Name Mapping。

---

## 11. Multi-source PFTrack Rule

PFTrack workflow 可能需要分別輸出：

```text
AutoTrack TXT
UserTrack TXT
```

PFTrack Source Adapter 必須支援 source set。

每個 file role：

```text
AUTOTRACK
USERTRACK
```

只屬 source provenance / diagnostics。

不加入 Canonical v1 semantics。

如果不同 source files 出現相同 visible Track Name：

```text
CROSS_SOURCE_TRACK_NAME_COLLISION
```

不得進行 Track Merge。

---

## 12. Native Format Contract

Native Format Contract 不只包含欄位。

正式定義：

```text
Native Format Contract
=
Field Grammar
+ Record Order
+ Exact Whitespace / Newline Layout
```

Writer 不得：

- invent private interchange syntax
- 自行增加 comment/header
- 自行增加 separator
- 自行增加 blank line
- 自行改變 field order
- 將 Canonical internal data 塞進 native grammar
- 假設 parser 能讀就代表 software 能讀

---

## 13. Validation Boundary

Validation 至少區分：

```text
Parser Validation
Artist Import Validation
Round-trip Validation
```

重要：

```text
Parser PASS != Software Import PASS
```

Self-parser validation 不能取代 actual software import。

Writer 與 parser 不得共同發明一套 private grammar，再互相驗證為 PASS。

真正 native-format acceptance boundary：

```text
Real Software Artist Import
```

---

## 14. Failure Principle

發現 mismatch 時：

禁止：

- Auto fix Golden
- Auto rename
- Auto frame offset correction
- Auto coordinate flip
- Auto resolution scaling
- Auto gap filling
- Auto observation deletion
- Auto duplicate Track Merge
- Auto whitespace normalization後宣稱 native valid

必須：

```text
Preserve Evidence
Report Failure
Stop Affected Path
```

---

## 15. Tool UI Requirement

正式 Production Tool 建議明確提供：

```text
Source Software
Target Software
Source File(s)
Image Width
Image Height
Start Frame
End Frame (when available)
```

例如：

```text
Source Software [ PFTrack ]
Target Software [ SynthEyes ]
```

UI 選項只決定：

```text
Selected Source Reader
→ Canonical
→ Selected Target Writer
```

不得改變底層 architecture。

---

## 16. Codex Fallback Requirement

即使正式 Tool 完成前後，應保留一份：

```text
Codex Conversion Handoff
```

用途：

- Tool 完成前 production fallback
- Technical validation
- Emergency conversion
- Regression investigation

Codex Handoff 必須依同一份正式 spec，不得另建 conversion semantics。

---

## 17. Verified Production Evidence

### Original Golden Validation

Test 01–06：

- 4608×1757
- 3DE / PFTrack / SynthEyes six directions
- Artist Import PASS
- Round-trip PASS

### Test 07 — New Real Shot

- Source: 3DE
- Resolution: 4096×2160
- Start Frame: 1001
- 9 tracks
- 144 observations
- Different real topology / gaps
- PFTrack Artist Import PASS
- SynthEyes Artist Import PASS
- PFTrack Round-trip PASS
- SynthEyes Round-trip PASS

Final:

```text
TEST07_FINAL_PASS
```

### Test 08 — New Real Shot

- Source: PFTrack
- Resolution: 3424×2202
- Start Frame: 1001
- AutoTrack: 7 tracks / 339 observations
- UserTrack: 7 tracks / 325 observations
- Aggregated: 14 tracks / 664 observations
- 3DE Artist Import PASS
- SynthEyes Artist Import PASS
- 3DE Round-trip PASS
- SynthEyes Round-trip PASS

Final:

```text
TEST08_FINAL_PASS
```

Test 08 additionally validates:

- PFTrack multi-source Source-set Aggregation
- Source provenance isolation
- `track_id` vs `track_name`
- 3DE exact native whitespace contract

---

## 18. Production Baseline

目前 v1 可視為：

```text
PRODUCTION-READY BASELINE
```

範圍限定為：

```text
Artist-created 2D Track Core Interchange
```

不得將此結論延伸至 v1 Scope 外的 Camera / Lens / Survey / 3D / Object Tracking 等資料。
