# Native Import Validation

## Golden 01

Source:
- 3DE_R5
- Resolution: 1920x1080
- Production Start Frame: 1001
- Production End Frame: unknown / not supplied

Input:
- validation/inputs/3de_golden_01.txt

### PFTrack 2017

Output:
- validation/outputs/3de_to_pftrack_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS

### SynthEyes 2304

Output:
- validation/outputs/3de_to_syntheyes_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS

## Golden 02

Source:
- PFTRACK_2017
- Source Role: AUTOTRACK
- Resolution: 1920x1080
- Production Start Frame: 1001
- Production End Frame: unknown / not supplied

Input:
- validation/inputs/pftrack_golden_01.txt

### 3DEqualizer R5

Output:
- validation/outputs/pftrack_to_3de_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS

### SynthEyes 2304

Output:
- validation/outputs/pftrack_to_syntheyes_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS

## Golden 03

Source:
- SYNTHEYES_2304
- Resolution: 1920x1080
- Production Start Frame: 1001
- Production End Frame: unknown / not supplied

Input:
- validation/inputs/syntheyes_golden_01.txt

### 3DEqualizer R5

Output:
- validation/outputs/syntheyes_to_3de_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS

### PFTrack 2017

Output:
- validation/outputs/syntheyes_to_pftrack_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS

## Golden 05

Source:
- PFTRACK_2017
- Source Mode: AUTOTRACK + USERTRACK Source Set
- Resolution: 1920x1080
- Production Start Frame: 1001
- Production End Frame: unknown / not supplied

Inputs:
- validation/inputs/pftrack_source_set_autotrack_golden_01.txt
- validation/inputs/pftrack_source_set_usertrack_golden_01.txt

### 3DEqualizer R5

Output:
- validation/outputs/pftrack_source_set_to_3de_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- AutoTrack/UserTrack separation: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS

### SynthEyes 2304

Output:
- validation/outputs/pftrack_source_set_to_syntheyes_golden_01.txt

Validation:
- Import: PASS
- Track count: PASS
- Track names: PASS
- AutoTrack/UserTrack separation: PASS
- Frame mapping: PASS
- Coordinates: PASS
- Natural gaps: PASS
- Result: PASS