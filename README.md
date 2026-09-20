# Tracker Tool

Artist-created 2D Tracking Point interchange tool for:

* 3DEqualizer R5
* PFTrack 2017
* SynthEyes 2304

本工具用於在不同 3D Tracking Software 之間轉換 Artist 已建立的 2D Tracking Tracks。

v1 專注於：

* Track identity
* Track name
* Observation frame
* 2D pixel coordinate
* Natural frame gaps


---

## Supported Software IDs

CLI 必須使用以下正式 Software ID：

```text
3DE_R5
PFTRACK_2017
SYNTHEYES_2304
```

不接受 alias，例如：

```text
3DE
PFTRACK
SYNTHEYES
```

工具不會依檔名或檔案內容自動猜測 Source Software。

---

## Architecture

所有 conversion 都使用同一套 Canonical architecture：

```text
Source Native File
↓
Source Reader
↓
Canonical 2D Track
↓
Canonical Validation
↓
Target Writer
↓
Target Native File
```

本工具不是建立：

```text
3DE → PFTrack converter
3DE → SynthEyes converter
PFTrack → 3DE converter
...
```

Target Writer 只依賴 Canonical Track Data 與 Target 所需的 ShotConfig。

---

## Supported Conversion

Single-source conversion 支援：

```text
3DE_R5 → PFTRACK_2017
3DE_R5 → SYNTHEYES_2304

PFTRACK_2017 → 3DE_R5
PFTRACK_2017 → SYNTHEYES_2304

SYNTHEYES_2304 → 3DE_R5
SYNTHEYES_2304 → PFTRACK_2017
```

PFTrack Source Set 支援：

```text
PFTrack AutoTrack
+
PFTrack UserTrack
↓
3DE_R5
```

以及：

```text
PFTrack AutoTrack
+
PFTrack UserTrack
↓
SYNTHEYES_2304
```

---

## Same-source Conversion

v1 不允許 Same-source conversion：

```text
3DE_R5 → 3DE_R5
PFTRACK_2017 → PFTRACK_2017
SYNTHEYES_2304 → SYNTHEYES_2304
```

本工具定位為不同 Tracking Software 之間的 interchange，而不是 native file rewrite / normalization tool。

---

# CLI

目前提供兩個主要 command：

```text
tracker-tool convert
```

以及：

```text
tracker-tool convert-pftrack-source-set
```

在開發環境可使用：

```powershell
uv run tracker-tool --help
```

查看主說明。

---

# 1. Single-source Conversion

基本 command：

```powershell
uv run tracker-tool convert `
    --source SOURCE `
    --target TARGET `
    --input INPUT_FILE `
    --output OUTPUT_FILE `
    --width IMAGE_WIDTH `
    --height IMAGE_HEIGHT `
    --start-frame START_FRAME
```

可選：

```text
--end-frame END_FRAME
```

PFTrack 作為 Source 時另外必須指定：

```text
--pftrack-source-role AUTOTRACK
```

或：

```text
--pftrack-source-role USERTRACK
```

---

## Example — 3DE → PFTrack

```powershell
uv run tracker-tool convert `
    --source 3DE_R5 `
    --target PFTRACK_2017 `
    --input input_3de.txt `
    --output output_pftrack.txt `
    --width 1920 `
    --height 1080 `
    --start-frame 1001 `
    --end-frame 1100
```

---

## Example — 3DE → SynthEyes

```powershell
uv run tracker-tool convert `
    --source 3DE_R5 `
    --target SYNTHEYES_2304 `
    --input input_3de.txt `
    --output output_syntheyes.txt `
    --width 1920 `
    --height 1080 `
    --start-frame 1001
```

`--end-frame` 可以省略。

---

## Example — PFTrack AutoTrack → 3DE

```powershell
uv run tracker-tool convert `
    --source PFTRACK_2017 `
    --target 3DE_R5 `
    --input pftrack_autotrack.txt `
    --output output_3de.txt `
    --width 1920 `
    --height 1080 `
    --start-frame 1001 `
    --pftrack-source-role AUTOTRACK
```

---

## Example — PFTrack UserTrack → SynthEyes

```powershell
uv run tracker-tool convert `
    --source PFTRACK_2017 `
    --target SYNTHEYES_2304 `
    --input pftrack_usertrack.txt `
    --output output_syntheyes.txt `
    --width 1920 `
    --height 1080 `
    --start-frame 1001 `
    --pftrack-source-role USERTRACK
```

---

## Example — SynthEyes → PFTrack

```powershell
uv run tracker-tool convert `
    --source SYNTHEYES_2304 `
    --target PFTRACK_2017 `
    --input input_syntheyes.txt `
    --output output_pftrack.txt `
    --width 1920 `
    --height 1080 `
    --start-frame 1001
```

---

# 2. PFTrack Source Set Conversion

PFTrack workflow 可能同時包含：

```text
AutoTrack
+
UserTrack
```

因此提供獨立 command：

```text
tracker-tool convert-pftrack-source-set
```

基本格式：

```powershell
uv run tracker-tool convert-pftrack-source-set `
    --autotrack-input AUTOTRACK_FILE `
    --usertrack-input USERTRACK_FILE `
    --target TARGET `
    --output OUTPUT_FILE `
    --width IMAGE_WIDTH `
    --height IMAGE_HEIGHT `
    --start-frame START_FRAME
```

可選：

```text
--end-frame END_FRAME
```

這個 command 的 Source 固定為：

```text
PFTRACK_2017
```

因此不需要：

```text
--source
```

也不需要：

```text
--pftrack-source-role
```

AutoTrack / UserTrack role 已由各自的 input argument 明確指定。

Valid targets：

```text
3DE_R5
SYNTHEYES_2304
```

PFTRACK_2017 is not a valid target because same-source conversion is not allowed。

---

## Example — PFTrack Source Set → 3DE

```powershell
uv run tracker-tool convert-pftrack-source-set `
    --autotrack-input pftrack_auto.txt `
    --usertrack-input pftrack_user.txt `
    --target 3DE_R5 `
    --output output_3de.txt `
    --width 1920 `
    --height 1080 `
    --start-frame 1001
```

---

## Example — PFTrack Source Set → SynthEyes

```powershell
uv run tracker-tool convert-pftrack-source-set `
    --autotrack-input pftrack_auto.txt `
    --usertrack-input pftrack_user.txt `
    --target SYNTHEYES_2304 `
    --output output_syntheyes.txt `
    --width 1920 `
    --height 1080 `
    --start-frame 1001
```

如果 AutoTrack 與 UserTrack 出現相同的 Artist-visible Track Name：

```text
CROSS_SOURCE_TRACK_NAME_COLLISION
```

conversion 會停止。

v1 不會自動 merge 或 rename。

---

# Required Shot Metadata

每次 conversion 至少需要：

```text
image_width
image_height
production_start_frame
```

CLI 對應：

```text
--width
--height
--start-frame
```

`production_end_frame` 可選：

```text
--end-frame
```

---

## Metadata Rules

### Image Width / Height

必須是正整數：

```text
width > 0
height > 0
```

例如：

```text
1920 × 1080
4096 × 2160
4608 × 1757
```

以下不合法：

```text
0
負數
float
string
boolean
```

---

### Production Start Frame

必須是 integer。

可以是：

```text
1001
0
-10
```

v1 不強迫 Production Frame 必須為正數。

---

### Production End Frame

可以：

```text
None / 未提供
```

如果有提供，必須：

```text
production_end_frame >= production_start_frame
```

例如：

```text
start = 1001
end   = 1100
```

合法。

```text
start = 1001
end   = 1001
```

也合法。

但：

```text
start = 1001
end   = 1000
```

不合法。

---

# Observation Frame Range

每一筆 observation 都必須：

```text
production_frame >= production_start_frame
```

如果有提供 `production_end_frame`，則同時必須：

```text
production_frame <= production_end_frame
```

因此當完整 Shot Range 已知時：

```text
production_start_frame
<= observation.production_frame
<= production_end_frame
```

如果沒有提供 End Frame，本工具不會從最後一筆 Track Observation 自動推算實際 Shot End Frame。

---

# Coordinate Rules

Canonical Coordinate 使用：

```text
Pixel Space
Origin = Top Left
X = Right
Y = Down
```

Coordinate 必須是 finite numeric value。

允許：

```text
負座標
畫面範圍外座標
```

例如：

```text
x = -20.5
y = 300.0
```

可能代表合法的 off-screen tracking observation，不會只因超出 image bounds 而被拒絕。

不允許：

```text
True
False
NaN
Infinity
非數字文字
```

---

# Same Image Geometry

v1 conversion assumes the Source Track Data and Target Software use the same image geometry.

v1 does not automatically compensate for or detect：

- Resize
- Crop
- Proxy with different resolution / framing
- Overscan
- Reformat
- Other different plate geometry

The supplied image width and height must correspond to the actual plate geometry used for the conversion.

v1 does not perform automatic X/Y scaling or infer resolution from Track coordinate extrema。

# SynthEyes Target Track Name Constraints

目前 verified SynthEyes v1 grammar：

```text
<TRACKER_NAME> <FRAME> <U> <V> <OUTCOME>
```

### Whitespace

包含 whitespace 的 Canonical `track_name` 無法由目前 verified grammar 無損表示。

例如：

```text
Point 001
```

必須拒絕 conversion。

不得自動：

```text
Point 001 -> Point_001
```

### Duplicate target names

SynthEyes 使用 exact tracker name 作為 Track grouping identity。

因此兩條不同 Canonical Tracks 如果具有相同：

```text
track_name
```

必須拒絕 SynthEyes output。

不得 automatic rename。

例如不得自行變成：

```text
Point0001
Point0001_2
```


# Natural Gaps

Natural frame gaps 會保留。

例如 Source Track：

```text
1001
1002
1004
1007
```

Target 仍然只會包含這些 observation。

工具不會自行補：

```text
1003
1005
1006
```

---

# What v1 Does Not Do

v1 不執行：

* Track filtering
* Track ranking
* Track selection
* Retention
* Coverage floor
* Similarity filtering
* Duplicate cleanup
* Automatic track pruning
* Interpolation
* Natural gap filling
* Track extension
* Observation fabrication
* Automatic Track merge
* Automatic Track rename
* Coordinate auto-fix
* Resolution scaling
* Camera solve
* Lens distortion processing
* Focal length conversion
* Filmback conversion
* Survey conversion
* 3D point conversion
* Object Tracking conversion

本工具目前只處理 Artist-created 2D Track interchange。

---

# Failure Behavior

Conversion 發生錯誤時：

```text
conversion stops
```

CLI output is written only after conversion succeeds。

If conversion fails：

- a new output file is not created
- an existing output file is not modified, truncated, or deleted

pre-existing output content is preserved exactly。

工具不會為了讓 conversion 成功而自動：

* 修正 frame offset
* 翻轉 coordinate
* Scale coordinate
* 補 observation
* 刪 observation
* Merge Track
* Rename Track

# Input / Output Path Safety

Single-source conversion：

```text
output must not resolve to the same file as input
```

PFTrack Source Set：

```text
output must not resolve to the same file as autotrack-input
output must not resolve to the same file as usertrack-input
```

如果發生 collision：

```text
conversion stops before any file is written
```

v1 does not support in-place rewriting of a source native file。


---

# Formal Error Codes

v1 對外使用的正式 Error Code：

```text
MISSING_REQUIRED_SHOT_METADATA
INVALID_SHOT_METADATA
OBSERVATION_OUTSIDE_SHOT_RANGE
CROSS_SOURCE_TRACK_NAME_COLLISION
SAME_SOURCE_CONVERSION_NOT_ALLOWED
UNSUPPORTED_SOURCE_SOFTWARE
UNSUPPORTED_TARGET_SOFTWARE
```

CLI 缺少 required command-line argument 時，由 command-line parser 直接拒絕，不會轉換成 `MISSING_REQUIRED_SHOT_METADATA`。

---

# Validation

Automated tests 只代表程式行為符合目前 contract。

```text
pytest PASS
!=
Native Software Import PASS
```

Native output 的最終 compatibility boundary 仍然是實際軟體：

* 3DEqualizer R5
* PFTrack 2017
* SynthEyes 2304

的 Artist Import Validation。

---

# Development Test

Run the full automated test suite with：

```powershell
uv run pytest -v
```

All tests must pass before treating the current repository state as a valid development baseline。

# Detailed Specification

完整 architecture、Canonical contract、Native Format contract、validation boundary 與 production rules 請參考：

```text
docs/INTERCHANGE_MASTER.md
```

README 只提供工具定位與實際使用方式。

`INTERCHANGE_MASTER.md` 才是 v1 formal technical specification。
