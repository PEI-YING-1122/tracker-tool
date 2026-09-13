# VALIDATION_CONTRACT.md — Artist 2D Track Interchange Validation Contract

## 1. Purpose

Validation 目標不是證明 Track Quality。

它證明：

```text
Data Interchange Integrity
```

---

## 2. Validation Stages

正式 validation 分為：

1. Preflight
2. Source Native Reader Validation
3. Canonical Validation
4. Target Writer Structural Validation
5. Real Software Artist Import Validation
6. Real Software Round-trip Validation

禁止將任一前段 PASS 誤報成後段 PASS。

---

## 3. Preflight

至少 resolve：

```text
image_width
image_height
production_start_frame
```

production formal implementation 應取得：

```text
production_end_frame
```

如果缺少必要 metadata：

```text
MISSING_REQUIRED_SHOT_METADATA
```

Resolution 不得由 track extrema 推論。

Start Frame 不得由 native observation bounds 猜測。

---

## 4. Source Reader Validation

必須確認：

- Native grammar valid
- Track Count
- Observation Count
- Track identity
- Track name
- Frame set per track
- Natural gaps
- Coordinate finite
- Same-track/frame uniqueness
- No malformed record

Multiple Source Files：

每份必須先獨立 PASS，再 merge。

---

## 5. Canonical Validation

確認：

- unique `track_id`
- valid `track_name`
- finite x/y
- production frame valid
- exact observation membership
- no fabricated observation
- no conflict

禁止任何 selection / filtering / interpolation。

---

## 6. Target Writer Parser Validation

Writer output 必須再以 strict target grammar parse。

但：

```text
Parser PASS != Software Import PASS
```

Strict Parser 必須依已驗證 native grammar，而不是 Writer 自己定義的新 grammar。

---

## 7. Native Grammar Acceptance

Native grammar 包含：

```text
Field Grammar
Record Order
Exact Whitespace / Newline Layout
```

Validation parser 不得先 normalize invalid native whitespace，再宣稱 PASS。

特別是 3DE：

```text
Blank Line Count = 0
```

為目前 verified contract。

---

## 8. Artist Import Validation

只有 Tracking Artist 實際在目標 software import 成功後，才能標記：

```text
ARTIST_IMPORT_PASS
```

至少人工確認：

- File Import
- Track Count
- Track Identity
- Frame Mapping
- Point Position
- Natural Gap
- Editability

Parser Validation 不得替代此 boundary。

---

## 9. Round-trip Integrity

最高強度 validation：

```text
Golden Source Native
→ Reader
→ Golden Canonical
→ Writer
→ Real Target Software Import
→ Real Target Software Export
→ Reader
→ Round-trip Canonical
→ Compare Golden Canonical
```

必須使用 REAL GUI / software export。

禁止：

- Writer output 當 round-trip export
- simulated export
- generated target export
- copied Golden

---

## 10. Structural Round-trip Compare

每條 path 比較：

- Track Count
- Observation Count
- Track Identity
- Exact Frame Set per Track
- Natural Gap Set
- Added Observations
- Missing Observations
- Same-track/frame conflicts

不得只比：

```text
min frame
max frame
```

---

## 11. Position Error

每筆 matching observation：

```text
dx = roundtrip_x - golden_x
dy = roundtrip_y - golden_y
pixel_error = sqrt(dx^2 + dy^2)
```

Report：

- Max DX
- Max DY
- Max Pixel Error
- Mean Pixel Error
- Median Pixel Error

---

## 12. Precision Classification

```text
<= 0.001 px
PRACTICALLY_LOSSLESS
```

```text
> 0.001 px and <= 0.01 px
ACCEPTABLE_SERIALIZATION
```

```text
> 0.01 px and <= 0.1 px
REVIEW_REQUIRED
```

```text
> 0.1 px
ROUNDTRIP_POSITION_FAIL
```

這些 thresholds 只衡量 interchange serialization integrity。

不是 Tracking Accuracy 標準。

---

## 13. Hard Failure Codes

至少支援：

```text
MISSING_REQUIRED_SHOT_METADATA
IMAGE_GEOMETRY_MISMATCH

TRACK_COUNT_MISMATCH
OBSERVATION_COUNT_MISMATCH
TRACK_IDENTITY_LOST
FRAME_MAPPING_ERROR
FRAME_SET_MISMATCH
NATURAL_GAP_FILLED
MISSING_OBSERVATION
FABRICATED_OBSERVATION
SAME_TRACK_FRAME_CONFLICT

HORIZONTAL_FLIP
VERTICAL_FLIP
NON_FINITE_COORDINATE
OUT_OF_IMAGE_BOUNDS
ROUNDTRIP_POSITION_FAIL

CROSS_SOURCE_TRACK_NAME_COLLISION
PFTRACK_SOURCE_ROLE_UNRESOLVED

3DE_NATIVE_FORMAT_MISMATCH
3DE_NATIVE_WHITESPACE_MISMATCH
PFTRACK_NATIVE_FORMAT_MISMATCH
```

---

## 14. No Silent Correction

Validation 過程禁止：

- auto rename without mapping
- auto merge
- auto deduplicate
- auto gap fill
- auto frame offset correction
- auto coordinate flip
- auto coordinate clamp
- auto geometry scaling
- auto whitespace normalization followed by PASS

發現 mismatch：

```text
Preserve Evidence
Generate Diagnostic Report
Stop Affected Path
```

---

## 15. Test 07 Evidence

Test 07：

- Source 3DE
- 4096×2160
- Start 1001
- 9 tracks
- 144 observations
- PFTrack real import PASS
- SynthEyes real import PASS
- PFTrack Round-trip max error ≈ 0.000132716 px
- SynthEyes Round-trip max error ≈ 0.001123731 px
- Final PASS

---

## 16. Test 08 Evidence

Test 08：

- Source PFTrack
- 3424×2202
- Start 1001
- AutoTrack 7 / 339
- UserTrack 7 / 325
- Merged 14 / 664
- 3DE real import PASS after exact grammar/whitespace correction
- SynthEyes real import PASS
- 3DE Round-trip max error ≈ 3.22e-13 px
- SynthEyes Round-trip max error ≈ 0.001017606 px
- Final PASS

Test 08 proves：

```text
Self-parser PASS can still be false positive for native software compatibility.
```

因此 real software import 是 mandatory acceptance boundary。
