# ADAPTER_SYNTHEYES_2304.md — SynthEyes 2304 Native ↔ Canonical Adapter

## 1. Scope

Target：

```text
SynthEyes 2304 / 23.04.1056
Tracker 2-D Paths
```

本 Adapter 只負責：

```text
SynthEyes Native ↔ Canonical 2D Track Core
```

---

## 2. Verified Schema

```text
<TRACKER_NAME> <FRAME> <U> <V> <OUTCOME>
```

每 observation 一行。

Natural gap：

```text
omit row
```

---

## 3. Frame Contract

SynthEyes frame 為 zero-based relative shot frame。

Writer：

```text
syntheyes_frame
=
production_frame
- production_start_frame
```

Reader：

```text
production_frame
=
syntheyes_frame
+ production_start_frame
```

例如：

```text
production_start_frame = 1001
1001 → 0
```

不得 hard-code start frame。

---

## 4. Coordinate Contract

Canonical：

```text
Pixel / Top Left / X Right / Y Down
```

SynthEyes normalized：

```text
U = (2*x_pixel/image_width) - 1
V = 1 - (2*y_pixel/image_height)
```

Inverse：

```text
x_pixel = ((U + 1)/2) * image_width
y_pixel = ((1 - V)/2) * image_height
```

`image_width`, `image_height` 必須 runtime ShotConfig 取得。

不得 hard-code historical resolutions。

---

## 5. Vertical Convention

目前 Artist 2D Track Interchange contract 已由實際 Test isolated verified：

```text
V = 1 - (2*y/H)
```

此 contract 與過往 AI Tracking → SynthEyes pipeline contract 分開管理。

不得因本 Interchange 測試結果自動修改 legacy AI pipeline。

---

## 6. Outcome

Writer 使用：

```text
15
```

只視為：

```text
software-specific deterministic field
```

不加入 Canonical。

不得解讀成：

- confidence
- tracking quality
- similarity
- reprojection score

---

## 7. Precision

U/V 至少：

```text
9 decimal digits
```

不得過早 rounding。

---

## 8. Track Name

Writer 預設：

```text
Canonical.track_name
```

不得將：

```text
Canonical.track_id
```

直接作 visible tracker name。

若 target name collision 必須 deterministic mapping。

### Canonical Track Identity

SynthEyes Tracker 2-D Paths 每一筆 observation 使用：

```text
<TRACKER_NAME> <FRAME> <U> <V> <OUTCOME>
```

此 native schema 沒有獨立 Track ID 或 Track block identity。

因此 Reader 必須以 exact native TRACKER_NAME 作為 native grouping key。

所有具有相同 exact TRACKER_NAME 的 observation rows 屬於同一條 Canonical Track。

Canonical identity 規則：

```text
track_id = syntheyes::<exact native tracker name>
track_name = <exact native tracker name>
```

Example：

Native rows：

```text
Tracker0001 0 ...
Tracker0001 1 ...
Tracker0001 3 ...
```

Canonical：

```text
track_id   = syntheyes::Tracker0001
track_name = Tracker0001
```

Rules：

- tracker name 必須 exact preserve。
- leading zeros / case 不得自行 normalize。
- 同一 exact tracker name 的 rows 必須聚合為同一 Canonical Track。
- 不得依 row order、coordinate proximity 或 frame overlap 建立額外 Track identity。
- 不得使用 random UUID。
- 不得自行加入 block index 或 occurrence index。
- 若同一 tracker name 在同一 frame 出現多筆 observation，視為 same-track/frame conflict，Reader 必須拒絕。
- 同一 tracker name 在不同 frame 出現，仍屬同一 Track；缺少的 frame 為 natural gap。
- track_id 只作 Canonical internal identity。
- Writer 仍輸出 Canonical.track_name，而不是 Canonical.track_id。


---

## 9. Natural Gaps

Missing Canonical observation：

```text
no SynthEyes row
```

禁止：

- interpolation
- gap filling
- artificial extension
- fabricated observation

---

## 10. Reader Validation

確認：

- each row field count = 5
- tracker name valid
- frame integer
- U finite
- V finite
- Outcome integer
- no same-track/frame conflict
- natural gaps preserved
- no malformed row

Outcome 不控制 Canonical membership。

---

## 11. Writer Validation

Writer output parse 後確認：

- Track Count = Canonical
- Observation Count = Canonical
- Exact frame set
- Identity mapping
- finite U/V
- no fabricated observation

並執行 inverse numeric check：

```text
Synth U/V
→ Canonical pixel
→ compare source Canonical
```

---

## 12. Same Geometry Requirement

SynthEyes normalized conversion 必須使用 target plate same image geometry。

如果 target image geometry 不同：

```text
IMAGE_GEOMETRY_MISMATCH
```

不得 silent renormalize to different plate。

---

## 13. Artist Import Boundary

Parser PASS 不等於 SynthEyes Import PASS。

Tracking Artist 必須實際確認：

- tracker count
- frame mapping
- position
- natural gaps
- editability

---

## 14. Round-trip Evidence

Test 07：

```text
9 tracks
144 observations
Max Pixel Error ≈ 0.001123731 px
ACCEPTABLE_SERIALIZATION
```

Test 08：

```text
14 tracks
664 observations
Max Pixel Error ≈ 0.001017606 px
ACCEPTABLE_SERIALIZATION
```

目前 SynthEyes 2304 Interchange Adapter 在兩個不同 resolution / real shot 上完成 real software round-trip PASS。
