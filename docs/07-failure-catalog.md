# 07 · Failure catalog

Every entry happened in a real project. Format: **symptom (as the modder saw it) → likely causes (in order) → fix → how to prove it.**

## Geometry

### Sawtooth / "teeth" along an edge (A-pillar, dash edge)
- **Causes**: concave n-gons triangulated differently at export; duplicate vertices; zero-area faces; coplanar overlapping faces (z-fighting) with another part.
- **Fix**: rebuild with clean quads or a Triangulate modifier (Beauty) before export; *Merge by Distance*; dissolve degenerate faces; remove or offset the duplicate surface (≥ 2 mm).
- **Prove**: `mesh_audit.py` shows 0 concave n-gons and 0 non-manifold edges; V1/V2 screenshot shows a clean edge.

### See-through gaps, parts vanish from some angles
- **Causes**: single-sided faces + backface culling; flipped normals.
- **Fix**: give trims real thickness (Solidify 3–4 mm); *Recalculate Outside*; check *Face Orientation*.
- **Prove**: in-game views from both sides.

### A part "floats" (dash looks suspended, glass without housing)
- **Causes**: missing transition geometry (no frit band hiding the dash/glass junction); housing faces culled or in a variant not rendered in interior view.
- **Fix**: measure the gap with `gap_raycast.py` (target ≤ 3 mm); add the frit band as a separate mesh sized with `eye_line.py`; rebuild the housing as a closed solid in the correct part/variant.
- **Prove**: V1/V4 or V2/V3 next to references.

### Huge faceted trim (A-pillar like a block)
- **Cause**: low-poly piece grown by repeated patching.
- **Fix**: rebuild from scratch: guide curve along the glass edge, swept profile, subdivision, measured width.

### Tyre clips through the fender
- **Causes**: wheel radius or track wrong; arch too shallow; steering lock too high for the geometry.
- **Fix**: real tyre diameter, published track and wheelbase; max steer from turning circle; intersection test at full lock + full compression; black arch liner with depth. Never "fix" by just reducing lock.

## Materials and textures

### Moiré / noisy pattern on the dash or glass
- **Cause**: textures without mipmaps, high-frequency patterns.
- **Fix**: generate mipmaps (DDS); real geometry for slots; lower-contrast detail maps.

### Interior grey or beige instead of black
- **Causes**: base colours too light; colour-space mistake; over-strong ambient.
- **Fix**: near-black base colours (#141414–#1A1A1A), check sRGB/linear handling against vanilla materials.

### White blotches on large surfaces
- **Causes**: vertex colours multiplied by the shader; AO baked with overlapping UVs; light leaking through gaps.
- **Fix**: clear or rebake vertex colours; unique UVs for bakes; close gaps.

### Chrome looks like white plastic
- **Cause**: no environment reflections.
- **Fix**: vanilla env-mapped effect; base around #9A9A9A for satin chrome, roughness ~0.3.

### "SRS AIRBAG" / labels too loud
- **Fix**: emboss with a normal map in the same colour; real labels are subtle.

## Digital cluster

### Speed disappears / text overlaps the speed
- **Causes**: element ID reused or missing; another element on top; zones defined at small values only.
- **Fix**: one ID per element; Y-band layout; bounding-box check at max values; shrink fonts per row.

### Tachometer doesn't move
- **Causes**: animation not bound; segments behind the background (depth); wrong frame mapping.
- **Fix**: verify the anim name and range; 0.3–0.5 mm offset towards the driver; test sweep screenshots at four rpm values.

### Warning lamps never light
- **Fix**: map each real lamp to a dashboard ID or indicator animation; unlit lamps nearly invisible, lit ones saturated.

## Mirrors

### Interior mirror shows the road ahead (or the bonnet)
- **Cause**: camera slot oriented forward (axis convention).
- **Fix**: rotate 180° yaw with the correct axis sign; test with a vehicle overtaking (it must appear in the mirror only once it is *behind* you).

### Mirror glass is black
- **Causes**: glass not bound to a rendered camera slot; a black face in front of the glass; the camera starts inside closed geometry; the exterior model's rear window is opaque from inside.
- **Fix, in order**: colour-tag the parts; put the working side-mirror material on the glass as a binding test; move the camera origin out of geometry; make the exterior rear glass transparent from inside; study a working car mod's technique.

### Ghost frame that survives every fix
- **Cause**: it isn't in the file being edited (inherited accessory, exterior model, another mod).
- **Fix**: colour-tag diagnostics; whatever doesn't change colour lives elsewhere.

### Exterior mirror glass floats, housing missing
- **Causes**: housing single-sided or normals flipped; housing in a part not rendered from interior.
- **Fix**: closed solid housing, correct normals, same part/variant as the glass; scale from published width with/without mirrors.

## Lights

### Headlights and taillights never light
- **Causes**: not using the lamp material; missing RGBA mask; lamp UVs not on the right tiles; no light sources/flares defined.
- **Fix**: follow the SCS lamp system; preview with Lamp Switcher; copy the light-source structure from a vanilla vehicle.

## Physics

### Car feels slow at speed
- **Causes**: truck-tuned global physics; nominal torque instead of calibrated torque; wrong final drive or tyre radius.
- **Fix**: calibrate against measured in-gear times; verify rpm at a known speed against the real car ([08](08-physics-calibration.md)).

## Process failures

| Failure | Prevention |
|---|---|
| Wrong engine assumed (shader code for a no-code engine) | Engine named in `CLAUDE.md`; engine-truth check every round |
| "Fixed" in Blender, broken in game | In-game standard views required for acceptance |
| Same failing fix repeated | Escalation after two failures: diagnostics + study a working mod |
| Earlier request silently dropped (frit band, door handle) | Carry open items forward explicitly in the next round |
