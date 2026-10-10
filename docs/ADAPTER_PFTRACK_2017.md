# ADAPTER_PFTRACK_2017.md — PFTrack 2017 Native ↔ Canonical Adapter

## 1. Scope

本 Adapter 只負責：

```text
PFTrack Native Source Set ↔ Canonical 2D Track Core
```

以及 Canonical → PFTrack native writer。

不得執行：

- Selection
- Quality filtering
- Similarity filtering
- Interpolation
- Duplicate cleanup
- Source software branching in Writer

---

## 2. Verified Native Grammar

Header：

```text
# "Name"
# clipNumber
# frameCount
# frame, xpos, ypos, similarity, zdepth
```

Track block：

```text
"<TRACK_NAME>"
<clipNumber>
<frameCount>
<frame> <xpos> <ypos> <similarity>
...
```

目前 verified rows 使用 4 numeric values：

```text
frame xpos ypos similarity
```

Header 雖列 zdepth，但不得自動 fabricate zdepth。

### Verified Header Variants

真實 PFTrack 2017 export 已確認兩種 header，只有第 4 行不同：

```text
# frame, xpos, ypos, similarity, zdepth
```

```text
# frame, xpos, ypos, similarity
```

兩種 variant 的 observation rows 都是 4 numeric values。

### Reader Layout Contract

Reader 只接受兩種 verified layout：

```text
Layout A — headerless
<block>
<block>
...
```

不含 header，也不含任何 blank line。此為 v1.0.0 已支援的 layout，也是 PFTrack Writer 的輸出 layout。

```text
Layout B — PFTrack 2017 native export
<verified header, 4 lines, exact text>
<blank line>
<block>
<blank line>
<block>
...
```

每個 track block 前必須剛好一行 blank separator line（包含第一個 block）。

已觀察的真實 export 不含 trailing blank line，因此 trailing blank line 不屬於 verified layout。

Reader 必須拒絕：

- unknown header（任何不完全等於 verified variant 的 header）
- 檔案中段出現 header 或 `#` 行
- track block 內部的 blank line
- 連續 blank line
- trailing blank line
- headerless data 中的 blank line
- 其他未被 verified native grammar 支援的結構

Reader 不得以「略過所有 `#` 行與 blank line」的方式處理 native data。

Header 內容不進入 Canonical。

Evidence：11 份真實 PFTrack 2017 export，包含 Test 08 AutoTrack / UserTrack source set（v1.0.1 CI-1）。

---

## 3. Forbidden Flat-row Grammar

以下曾由 implementation 自行發明，實際 PFTrack Import FAIL：

```text
TRACK_NAME FRAME XPOS YPOS SIMILARITY
01 1001 X Y 1.000000
```

必須 reject：

```text
PFTRACK_NATIVE_FORMAT_MISMATCH
```

---

## 4. Frame Contract

PFTrack native frame：

```text
production_frame
```

Reader：

```text
production_frame = pftrack_frame
```

Writer：

```text
pftrack_frame = production_frame
```

不得 +1 / -1 / zero-based remap。

---

## 5. Coordinate Contract

PFTrack：

```text
xpos = x_pixel
ypos = y_pixel
```

direct pixel pass-through。

---

## 6. Similarity

PFTrack Similarity：

```text
app-specific field
```

不加入 Canonical。

Reader：

- parse 可驗證 numeric
- 不影響 observation existence
- 不當成 Canonical confidence

Writer 如果 native format 要求 similarity：

```text
1.000000
```

可作：

```text
SYNTHETIC_FORMAT_FIELD
```

不得聲稱是真實 tracking quality。

---

## 7. Z Depth

v1 Canonical 不含 zdepth。

如果 Source native 有 zdepth：

- 可 diagnostics 保存
- 不加入 Canonical v1

Writer 不得 fabricate zdepth。

---

## 8. Track Name

Reader：

```text
PFTrack visible name → Canonical.track_name
```

Writer：

```text
Canonical.track_name → PFTrack visible name
```

若 target naming 需要 normalization，必須：

```text
deterministic
reversible
documented
```

不得 silent rename。

---

## 9. PFTrack Multi-source Source Set

PFTrack production workflow 已驗證可能需要分別 export：

```text
AutoTrack TXT
UserTrack TXT
```

Adapter 必須支援：

```text
PFTRACK_SOURCE_SET
```

每份 input 必須標記 role：

```text
AUTOTRACK
USERTRACK
```

Role 不得由 coordinates 猜測。

若 role 無法判定：

```text
PFTRACK_SOURCE_ROLE_UNRESOLVED
```

---

## 10. Independent Parse Before Source-set Aggregation

AutoTrack / UserTrack 必須先各自驗證：

- Track Count
- Observation Count
- Frame Range
- Track Names
- malformed records
- same-track/frame conflicts
- finite coordinates

兩份都 PASS 才可進行 Source-set Aggregation。

### Member Track Count（v1.0.2 CI-11）

每一個明確指定的成員檔（AutoTrack、UserTrack）都必須至少解析出 1 條 Track。

任一成員為 0 條 Track（例如空檔案，或只有 header 的 export）時，必須停止 conversion 並回報描述性錯誤。不得忽略該成員、只使用另一份檔案轉換。

原因：0-track 成員可能代表錯檔、空 export、parser 問題或 export 失敗，不應 silent success。

此錯誤為描述性 `ValueError`，不是 formal error code。

Source-set Aggregation 必須將每條 Track 保留為獨立 Track。

不得將不同 native Track 的 observations 組合至同一 Canonical Track。

---

## 11. Internal Identity

Recommended：

```text
pf_autotrack::<native_track_name>
pf_usertrack::<native_track_name>
```

只用於 Canonical.track_id。

Artist-visible：

```text
Canonical.track_name
```

仍保存 native name。

---

## 12. Cross-source Name Collision

如果 AutoTrack / UserTrack 出現相同 `track_name`：

```text
CROSS_SOURCE_TRACK_NAME_COLLISION
```

不得：

- silent Track Merge
- guess by coordinate proximity
- guess by frame overlap
- guess by order

identity 無法確定時 block conversion。

---

## 13. Source-set Aggregation Integrity

Source-set Aggregation 中不允許 Track Merge：

```text
Aggregated Track Count
=
AutoTrack Track Count
+
UserTrack Track Count
```

```text
Aggregated Observation Count
=
AutoTrack Observations
+
UserTrack Observations
```

Test 08：

```text
7 + 7 = 14 tracks
339 + 325 = 664 observations
```

PASS。

---

## 14. PFTrack Writer

Writer 使用 verified block grammar。

每 Track：

```text
"<track_name>"
1
<actual observation count>
<production_frame> <x_pixel> <y_pixel> 1.000000
...
```

`clipNumber = 1` 為目前 verified target-format field。

不得自行推論更深 semantics。

---

## 15. Validation

Strict parser 必須 reject invented flat-row syntax。

Real PFTrack Artist Import 才是 native compatibility boundary。

Test 07 已實證：

- invented flat-row parser PASS
- PFTrack actual import FAIL
- corrected block grammar actual import PASS

---

## 16. Round-trip Evidence

Test 07 PFTrack Round-trip：

```text
9 tracks
144 observations
Max Pixel Error ≈ 0.000132716 px
PRACTICALLY_LOSSLESS
```

Test 08 使用 PFTrack 作 real Source Set，multi-source Source-set Aggregation PASS。
