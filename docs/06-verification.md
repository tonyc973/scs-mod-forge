# 06 · Verification

## 1. Standard views

Define fixed views once per project and always use the same head position (default interior camera). The views we used:

| View | Where you look | Catches |
|---|---|---|
| **V1** | Straight ahead | Dash top, windshield base, cluster, wheel symmetry, interior mirror |
| **V2** | Head turned ~60° left | Left exterior mirror, A-pillar, door panel, side glass |
| **V3** | Head turned ~60° right | Right exterior mirror, passenger dash |
| **V4** | Down-forward | Dash surface, defroster slot, frit band, white blotches |
| **V5** | V1 at night, lights on | Backlight, warning lamps, headlight beams |

Add exterior free-camera views for wheels and lights (front ¾, rear ¾, side profile, wheel at full lock).

## 2. Getting screenshots to Claude Code

- The modder presses **F12** in each requested view.
- Claude Code reads the newest files from the game's screenshot folder (e.g. `Documents/Euro Truck Simulator 2/screenshot/`) if it has access; otherwise the modder sends them.
- Claude Code must **open** the screenshots and compare them. Listing filenames is not verification.

## 3. Comparison images

Use [`tools/compare_images.py`](../tools/compare_images.py):

```bash
python tools/compare_images.py ingame_v1.png refs/C10.jpg -o renders/compare_v1
# → compare_v1_side.png (side by side), compare_v1_overlay.png (50/50), compare_v1_diff.png (heat map)
```

For parts that can be photographed straight-on (vents, cluster), crop and align both images to the same region first. The overlay is then meaningful.

## 4. The A/B rule

For every change: screenshot **before** and **after** from the same view, next to the reference. Keep the change only if "after" is **clearly** closer. Otherwise revert. This one rule stopped most regressions.

## 5. Colour-tag diagnostics

When you can't tell which mesh or file produces something on screen:

1. In Blender, select the suspects and run [`tools/blender/diag_color_tag.py`](../tools/blender/diag_color_tag.py). Each object gets a unique flat, unlit-looking colour, and a `diag_colors.md` map is written.
2. Export a **separate diagnostic copy** of the mod (`*_diag`). Don't ship it.
3. Screenshot the same views in game.
4. Read the colours against the map.
   - A defect that **did not change colour** does not come from the tagged files. Look at inherited accessories, the exterior model and other active mods.
5. Record the answer, delete the diagnostic build.

This found the "ghost frame" around the interior mirror and the source of the black band over the side window in the Civic project. Both had survived several "fixes" applied to the wrong file.

## 6. Geometry checks in Blender

- [`mesh_audit.py`](../tools/blender/mesh_audit.py): non-manifold edges, concave n-gons, faces with inconsistent normals, zero-area faces, loose vertices. Run it on every object you touch.
- [`gap_raycast.py`](../tools/blender/gap_raycast.py): distance between two surfaces sampled along an edge (dashboard ↔ windshield ≤ 3 mm).
- [`eye_line.py`](../tools/blender/eye_line.py): project a contact line from the driver's eye point onto glass, e.g. to size the frit band so it hides the dash/glass junction from the player's view.

## 7. Physics verification

Measure in game exactly the tests your real-world data uses (e.g. 60–100 km/h in 4th, 5th, 6th). Log time and speed to CSV with a telemetry tool, run [`perf_from_telemetry.py`](../tools/perf_from_telemetry.py) and compare with the targets ([08](08-physics-calibration.md)).
