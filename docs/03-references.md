# 03 · Reference hunting

Realism comes from references, not from "make it realistic". Claude in Chrome's job is to find the **few best** references per component and **look at every one** before linking it.

## 1. Source ranking (best first)

| Rank | Source type | Good for | Watch out for |
|---|---|---|---|
| 1 | **Owner's manual diagrams** (OEM) | Exact layout: warning-lamp positions, switch labels, cluster structure | Line art; colours must come from photos |
| 2 | **OEM press / dealer images** (high-res, studio lit) | Shapes, proportions, materials, steering-wheel buttons | Top trims and other markets; may show options you don't have |
| 3 | **Independent tests with measurements** (e.g. ADAC, magazines) | Weights, rpm at speed, in-gear acceleration, turning circle, tyre size tested | Trim/market differences; check the exact variant |
| 4 | **Professional review galleries** (consistent sets of 40–60 photos of one car) | Night shots, close-ups, driver's view, wheels in arches | Market-specific equipment |
| 5 | **Owner photos on enthusiast forums** | "In use" views: the mirror *with what it reflects*, the cluster *while driving* | Modifications, aftermarket parts, phone distortion |
| 6 | Shop listings for spare parts | Isolated part shape (grab handle, mirror, trim) | Aftermarket ≠ OEM; watermarks |

**Never use** aftermarket "styled" parts as reference for the stock look (carbon covers, RGB taillights, tuned exhausts) unless that is your target.

## 2. What to collect per component

- **One straight-on photo** (for overlays and measurements).
- **One in-context photo** from the player's viewpoint (driver's eye for interiors).
- **One close-up** (buttons, textures, edges).
- **One "behaviour" photo** if the part changes state: lit lamps at night, cluster while driving, mirror with its reflection.
- **One authoritative layout source** if one exists (manual diagram).

Example from the Civic: the cluster needed a manual diagram (lamp positions), a close-up in **km/h** (layout and fonts), and a **driving** photo. Only the driving photo showed that the tachometer is a white bar filling over a coloured ring, not a needle.

## 3. Inspect before you link

For every reference write one line:

```
| C3 | cluster while driving, 80 km/h, red theme: rpm shown as white fill + amber tip | <url> | caveat: CVT car (shows "D") |
```

Things Claude in Chrome caught only by looking:

- an aftermarket ring on a tweeter photo;
- India-spec camera under the side mirror;
- a 7th-generation car in a "10th gen vents" search result;
- the right half of a "before/after" image being an aftermarket part.

## 4. Measuring from photos

Eyeballing proportions is the fastest way to get "close but obviously wrong". Use [`tools/photo_measure.py`](../tools/photo_measure.py):

1. Pick a straight-on reference.
2. Give the four corners of a rectangular region (e.g. the vent panel) → the tool corrects the perspective.
3. It extracts contours and reports dimensions **relative to the region width**.
4. Turn relative into absolute with a **scale anchor** you trust:
   - published dimensions (overall width with and without mirrors → mirror protrusion);
   - a standard part (a 7" 16:9 screen ≈ 155 mm active width; tyre diameter from its size code);
   - the modder's tape measure on the real car (best).

## 5. Published data you will want

| Data | Typical source | Used for |
|---|---|---|
| Wheelbase, track front/rear, overall width (with/without mirrors) | spec databases, OEM | wheel placement, mirror size |
| Turning circle | spec databases, road tests | max steering angle |
| Tyre size | OEM per trim, road-test car | wheel radius, gear speeds |
| Gear ratios + final drive | OEM spec sheets (often only for some markets) | gear speed table |
| Measured mass, rpm at speed, in-gear acceleration | road tests (ADAC etc.) | physics calibration |

Mark every number with its source and the **exact variant** it applies to. Ask the modder to confirm the ones that matter (rpm at 130 km/h in top gear is a great single-number check of final drive and tyre size).

## 6. Licensing

- Reference images are **linked**, not copied into the repo or the mod.
- Do not trace logos or artwork into textures you distribute unless you have the rights. Model the *shape* of real parts.
- Audio from videos is not a legal source for mod sounds (see [09](09-sound.md)).
