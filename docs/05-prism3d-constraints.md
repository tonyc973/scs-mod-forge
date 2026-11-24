# 05 · Prism3D constraints (ETS2 / ATS)

> **Always verify against the current SCS Modding Wiki and vanilla files for your game version.** This page summarizes what we relied on and links the sources. It is not a substitute for them.

## 1. The one rule that changes everything

**Mods cannot run code.** There are no scripts, no custom shaders and no runtime camera logic. Everything dynamic is done through mechanisms the engine already provides:

| You want | Prism3D way |
|---|---|
| A gauge needle / moving part | **Bone animation** bound to a vehicle value (e.g. `tachometer_anim`, `speedometer_anim`, `fuel_anim`), range set via `_anim_min` / `_anim_max` |
| A warning lamp | **Indicator animation** (2 keyframes, off/on), e.g. `button_left_blinker`, `button_high_beam_lights`, `button_parking_brake`, `button_4way` |
| Digital display text, bars and gauges | **Dashboard UI** elements bound to **element IDs** (e.g. 1020 current speed, 1030 odometer, 1040 current gear, 1050 clock, 1700 rpm bar, 1570/1580 blinkers, 1590 high beam) |
| Exterior lights | **Lamp material** + second **RGBA mask texture** + separate UV layer with **tile offsets** |
| Mirrors | Engine **mirror cameras** (main, side, front, hood types) configured through camera units, with glass using the mirror material |
| Engine sound | **FMOD Studio** bank built from the **SCS template**, events `engine`, `exhaust`, `turbo`, `start_bad`, parameters such as `engine/rpm`, `engine/load` |
| Illuminated surfaces (backlight) | Luminosity effects (e.g. `eut2.dif.lum`), coloured by `dashboard_color[]` |

Sources:
- Truck interior animations and dashboard IDs: <https://modding.scssoft.com/wiki/Documentation/Engine/Truck_Interior_Animations_and_IDs>
- Lamp system: <https://modding.scssoft.com/wiki/Documentation/Tools/SCS_Blender_Tools/Materials/Lamp_system>
- Lamp Switcher & UV Tool: <https://modding.scssoft.com/wiki/Documentation/Tools/SCS_Blender_Tools/SCS_Tools_Sidebar/Lamp_Switcher_%26_UV_Tool>
- Supported shaders: <https://modding.scssoft.com/wiki/Documentation/Tools/SCS_Blender_Tools/Supported_shaders>
- Sound system: <https://modding.scssoft.com/wiki/Documentation/Engine/Sound>
- Sound modding / template: <https://modding.scssoft.com/wiki/Documentation/Engine/Sound/Modding>, downloads: <https://modding.scssoft.com/wiki/Documentation/Engine/Sound/Downloads>
- Truck engine sound: <https://modding.scssoft.com/wiki/Documentation/Engine/Sound/TruckEngine>

## 2. Patterns that worked

### 2.1 A "filling" tachometer on an arc without shaders
The UI rpm bar (ID 1700) is a `ui_text_bar`. It is linear, so it can't follow a 210° arc on its own. What worked:

- **48–64 arc segments**, each on its own bone;
- **one** rpm animation (`tachometer_anim`) where segment *i* switches from scale 0 to 1 at frame ≈ `i/N × max_rpm`;
- the amber tip as a classic rotating needle bone in the same animation.

The result is visually a continuous fill.

### 2.2 Text layout on digital clusters
Each dashboard element ID can be used **once** (caching). Lay out zones by Y band and check bounding boxes at **maximum values** ("188", "1234 km", "99.9 l/100km"). Shrink the font of a row instead of letting it invade another zone.

### 2.3 Lights
Lit surfaces need **both** the lamp material/mask **and** the correct UV tile per function. Preview each function with the **Lamp Switcher** before exporting. Mask channels per the wiki: **R** left/right blinker, **G** high beam / brake, **B** low beam / reverse / DRL, **A** positional.

### 2.4 Chrome without reflection probes
Use a vanilla effect with an environment map for chrome and satin chrome. Pure white "metal" without env reads as matte plastic in game.

### 2.5 Mirrors
- Glass that is transparent, or a glass/env material, will never show what is behind the camera.
- Find which mirror camera slot your vehicle can repurpose, its orientation convention, and how the glass is bound to it. **Study a working car mod's technique** before building (don't copy its assets).
- Check which model renders in mirrors (often the **exterior** model). If its rear interior is a black box, the mirror shows black.

### 2.6 Packaging
Pack files under `/sound` with **store** (no compression), as SCS modders recommend.

## 3. Things that silently break realism

| Symptom | Usual Prism3D cause |
|---|---|
| Sawtooth edges in game, fine in Blender | concave n-gons re-triangulated at export |
| See-through gaps | single-sided faces + backface culling |
| Moiré on dash or glass | textures without mipmaps |
| Interior looks grey instead of black | base colour too light, or a colour-space mistake |
| White blotches | vertex colours / overlapping AO UVs / light leaks through gaps |
| Parts missing only in interior view | part/variant not included in what the interior camera renders |

See the full [failure catalog](07-failure-catalog.md).

## 4. Physics: per-vehicle vs global

ETS2 physics is tuned for trucks. Before calibrating a car, list **which parameters are per-vehicle** (engine torque and curve, rpm limits, gear ratios, final drive, wheel radius…) and which are global. Then calibrate against **measured times**, not nominal numbers ([08](08-physics-calibration.md)).
