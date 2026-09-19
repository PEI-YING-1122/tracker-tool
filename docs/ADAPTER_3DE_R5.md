# ADAPTER_3DE_R5.md — 3DEqualizer R5 Native ↔ Canonical Adapter

## 1. Scope

本 Adapter 只負責：

```text
3DE Native ↔ Canonical 2D Track Core
```

不得處理：

- Selection
- Track filtering
- Interpolation
- Camera solve
- Lens
- Survey
- 3D points
- Source-software-specific branching in Writer

---

## 2. Verified Native Structure

目前 verified 3DE native block：

```text
<TRACK_COUNT>
<TRACK_NAME>
<STATIC_FIELD>
<SAMPLE_COUNT>
<FRAME> <X> <Y>
...
```

Example：

```text
14
Auto000084
0
50
1 1159.443726000 1524.375000000
2 1154.000000000 1524.000000000
...
Auto000094
0
50
...
```

---

## 3. Exact Whitespace Contract

3DE native grammar 對 exact layout 敏感。

Verified rule：

```text
Blank Line Count = 0
```

禁止：

- TRACK_COUNT 後 blank line
- Track blocks 之間 blank line
- observation rows 之間 blank line
- indentation
- comments
- section headers
- separator lines
- leading/trailing spaces on structural lines

Validation parser 不得先 strip blank lines 再判 PASS。

若違反：

```text
3DE_NATIVE_WHITESPACE_MISMATCH
```

---

## 4. Static Field

Track Name 後目前 verified native field：

```text
0
```

Writer 使用：

```text
0
```

但 semantic meaning 尚未正式確認。

只視為：

```text
VERIFIED_NATIVE_FORMAT_FIELD
```

不得將其提升為 Canonical semantic field。

---

## 5. Sample Count

```text
SAMPLE_COUNT
=
actual observation rows for that track
```

不得使用：

- shot length
- frame max
- assumed constant

Natural gaps 不計入 sample count。

---

## 6. Frame Contract

3DE native 使用 internal frame。

Reader：

```text
production_frame
=
production_start_frame
+ 3de_internal_frame
- 1

Writer：

```text
3de_internal_frame
=
production_frame
- production_start_frame
+ 1
```

`production_start_frame` 必須由 ShotConfig runtime 取得。

不得 hard-code 1001。

---

## 7. Coordinate Contract

3DE Native ↔ Canonical：

```text
X = x_pixel
Y = y_pixel
```

same image geometry 下 direct pixel pass-through。

不得 normalize / flip / scale。

---

## 8. Track Name Contract

Reader：

```text
native track name → Canonical.track_name
```

exact preserve string。

例如：

```text
01
```

不得轉成：

```text
1

### Canonical Track Identity

3DE native Track 沒有獨立 stable Track ID。

Reader 必須以：

```text
3de::<6-digit 1-based native track block index>::<exact native track name>
```

生成 Canonical `track_id`。

例如第一個 native Track：

```text
Track Name:
Point0001
```

應得到：

```text
track_id = 3de::000001::Point0001
track_name = Point0001
```

第二個 Track 如果也叫 `Point0001`，則：

```text
track_id = 3de::000002::Point0001
track_name = Point0001
```

規則：

- native track block index 使用 1-based。
- index 固定格式為 6 位數、前方補 0。
- `track_name` 必須保持原始 Artist-visible Track Name。
- `track_id` 只作為 Canonical internal identity。
- 不得把 `track_name` 單獨當成 `track_id`。
- 不得使用 random UUID。
- 不得依 coordinate proximity 或 frame overlap 推測、合併或重新判定 Track identity。
- native Track block order 只能用於產生上述 1-based `native_track_index`，不得用來推測兩條不同 Track 為同一 Track identity。
- 同名 Track 必須保持為不同 Track，不得 merge。


Writer：

預設輸出：

```text
Canonical.track_name
```

不得輸出：

```text
Canonical.track_id
```

例如：

```text
track_id   = pf_autotrack::Auto000084
track_name = Auto000084
```

3DE Native 必須寫：

```text
Auto000084
```

不是：

```text
pf_autotrack::Auto000084
```

---

## 9. Natural Gap

3DE missing frame row：

```text
no observation
```

Reader 不補值。

Writer 不插值。

---

## 10. Reader Validation

確認：

- Track Count
- Track Name
- Static Field
- Sample Count
- actual row count
- frame integer
- X/Y finite
- no same-track/frame conflict
- exact whitespace contract

---

## 11. Writer Validation

Writer output strict validation 必須檢查：

```text
Blank Line Count = 0
```

以及：

- Track Count = Canonical Track Count
- Observation Count = Canonical Observation Count
- Sample Count exact
- Frame Set exact
- Natural gaps preserved
- X/Y exact within serialization tolerance
- no fabricated observations

---

## 12. Artist Import Boundary

只有實際 3DE Import 成功後：

```text
3DE_ARTIST_IMPORT_PASS
```

Parser PASS 不足以宣稱 import readiness。

Test 08 已實證：

- v01 grammar 錯誤 → parser 曾 PASS，但 3DE FAIL
- v02 field grammar 正確但多 blank line → 3DE FAIL
- v03 exact whitespace 正確 → 3DE PASS

---

## 13. Round-trip Evidence

Test 08 real 3DE export Round-trip：

```text
14 tracks
664 observations
Max Pixel Error ≈ 3.22e-13 px
PRACTICALLY_LOSSLESS
```

3DE Adapter v1 contract 已通過 real software round-trip。
