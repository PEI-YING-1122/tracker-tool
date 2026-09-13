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
