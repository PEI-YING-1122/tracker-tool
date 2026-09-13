# CANONICAL_2D_TRACK_CORE.md — Canonical 2D Track Core v01

## 1. Purpose

Canonical 是所有 supported tracking software 之間唯一的 software-independent intermediary semantic model。

Version：

```text
canonical_2d_track_core_v01
```

Serialization 可使用 JSON / other internal format，但 serialization 不是 semantic contract 本身。

---

## 2. Shot Metadata

```text
ShotMetadata {
    image_width
    image_height
    production_start_frame
    production_end_frame
}
```

Production implementation 另持有：

```text
source_software
target_software
```

作為 ShotConfig / execution context。

---

## 3. Track Model

```text
Track {
    track_id
    track_name
    observations: [
        {
            production_frame
            x_pixel
            y_pixel
        }
    ]
}
```

---

## 4. `track_id`

`track_id` 是 converter internal identity。

Requirements：

- string
- unique within current Canonical collection
- deterministic when possible
- 不得因 Target Software 改變
- 不得當作 Artist-visible name

Example：

```text
pf_autotrack::Auto000084
pf_usertrack::Tracker0001
```

它可保存 source provenance isolation，但不代表 Canonical 增加 `AutoTrack/UserTrack` semantic field。

---

## 5. `track_name`

`track_name` 是 Artist-visible source name。

Requirements：

- string
- exact text preservation when source supports it
- leading zeros preserved
- case preserved when possible
- 不得 numeric cast
- 不得自行 normalization

Example：

```text
"01"
"Auto000084"
"Tracker0001"
```

---

## 6. Observation

Observation：

```text
production_frame
x_pixel
y_pixel
```

Observation existence 本身代表：

```text
measurement exists
```

不存在代表：

```text
no measurement
```

Canonical v1 不使用：

```text
valid
visibility
confidence
quality
similarity
outcome
```

來控制 observation membership。

---

## 7. Frame Semantics

`production_frame`：

```text
actual production frame number
```

不是：

- 3DE internal frame
- SynthEyes zero-based frame
- array index
- clip-local index

Adapter 必須 Native ↔ Production Frame。

---

## 8. Coordinate Semantics

Canonical：

```text
Pixel Space
Origin = Top Left
X increases Right
Y increases Down
```

`x_pixel`, `y_pixel`：

- finite numeric
- no app-specific normalization
- no silent scaling

---

## 9. Natural Gaps

Natural gap 不建立 placeholder。

例如：

```text
1001
1002
1003
1007
1008
```

Canonical 只保存上述 observations。

不得建立：

```text
1004
1005
1006
```

的 null / interpolated / synthetic samples。

---

## 10. Uniqueness

同一 `track_id`：

```text
(track_id, production_frame)
```

必須 unique。

若同 frame 出現 conflicting observation：

```text
SAME_TRACK_FRAME_CONFLICT
```

不得自行取平均或覆蓋。

---

## 11. Multi-source Collection

一個 Source Adapter 可由多個 native source files 建立同一 Canonical Collection。

例如 PFTrack：

```text
AutoTrack TXT
UserTrack TXT
→ PFTrack Reader
→ Canonical
```

內部 identity 可包含 source role。

Artist-visible `track_name` 不因 internal role 自動改名。

---

## 12. Name Collision

如果不同 source files 中：

```text
track_name identical
```

但 identity 無法證明相同：

```text
CROSS_SOURCE_TRACK_NAME_COLLISION
```

不得 merge。

Canonical 可以同時保存不同 `track_id`，但 Target Writer 若不支援同名 tracks，必須建立 deterministic Target Name Mapping 或 fail。

---

## 13. Shot Geometry

Canonical 本身使用 pixel coordinates，因此 semantic model 可支援不同 resolution。

但 interchange 要求：

```text
same image geometry
```

Canonical 不負責：

- resize compensation
- crop offset
- overscan
- proxy scale
- reformat matrix

---

## 14. Excluded Fields

v1 禁止將以下內容提升為 Canonical Core：

- PFTrack similarity
- PFTrack zdepth
- PFTrack AutoTrack/UserTrack type
- SynthEyes Outcome
- 3DE static native field
- Camera solve data
- Lens data
- Survey
- 3D point
- Group
- Color
- Weight

這些可以存在於 diagnostics / Adapter-specific serialization，但不是 canonical semantics。

---

## 15. Serialization Rule

如果使用 JSON：

不得將 JSON schema 本身誤認為 Canonical semantic contract。

任何未來 serialization 只要完整保存：

```text
ShotMetadata
Track identity
Track name
Exact observation frame set
Pixel coordinates
```

即可符合 Canonical v01。
