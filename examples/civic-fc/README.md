# Case study: Honda Civic Sedan 2020 (FC, 1.5 VTEC Turbo, 6MT) for ETS2

The project: rebuild a drivable car mod's interior, exterior details and driving feel so that it is indistinguishable from the real car, owned by the modder. Research and prompts: Claude with Claude in Chrome (browser, web search, image inspection). Build: Claude Code driving Blender through the Blender MCP server.

The original round prompts are in [`prompts/`](prompts/). They are written **in Romanian**, the language the project was run in; their structure is what matters, and the English [template](../../templates/round-prompt.md) reproduces it.

## Round by round

| Round | Modder's complaint (summarised) | What Claude in Chrome added | Method lesson |
|---|---|---|---|
| [1](prompts/round-01-interior-baseline.md) | Interior looks generic; the H logo and the gear knob are unrealistic | OEM/dealer reference links per component; component-by-component description (emblem geometry, steering wheel trims, cluster, console, shifter) | **No reference, no work** |
| [2](prompts/round-02.md) | Sawtooth A-pillar, outline left under the logo, generic cluster, empty slot on the passenger dash, wheel needs refinement | Ordered diagnosis lists (concave n-gons, normals, z-fighting, thickness); cluster references from four trims | **Describe "now" before "real"**; give causes in order |
| [3](prompts/round-03.md) | Cluster still unrealistic, rpm not visible; interior mirror only shows the front; crude grab handle; noisy "grille" on the dash | Cluster geometry measured from photos; **driving photos** revealed the rpm is a white fill with an amber tip; overlay/diff acceptance | **Behaviour references** (photos of the part in use) |
| [3.1](prompts/round-03.1-prism3d-addendum.md) | (Claude Code pointed out: ETS2 mods cannot run code) | Rewrite of every dynamic requirement into Prism3D mechanisms: bone animations, dashboard UI IDs, mirror cameras | **Engine truth first**: Claude in Chrome had assumed a scriptable engine |
| [4](prompts/round-04.md) | Speed gone, no indicators; vents unrealistic; wheel/cluster symmetry | Full dashboard-ID mapping table for every warning lamp; vent close-ups; symmetry measured as equal X coordinates | **Map every real behaviour to an engine signal** |
| [5](prompts/round-05.md) | Range/fuel text drawn over the speed; mirror still wrong | Y-band layout with bounding boxes at max values; mirror diagnosis steps; **A/B-or-revert rule** | **Prove improvement or revert** |
| [6](prompts/round-06-exterior-physics.md) | Mirror shows the front; wiper area too black; tyre through the fender; lights dead; car feels slow at 160 in 5th | Exterior gallery references; lamp mask system; turning circle → steering angle; gear-speed math; performance targets | Scope grows: **the same method applies to exterior and physics** |
| [7](prompts/round-07.md) | Ugly A-pillar; vents not identical; mirror black; dash "floats"; side glass covered in black; in-gear pull | **Colour-tag diagnostics**; OpenCV measurement of vents from a rectified photo; "learn from a working mod"; **ADAC-measured in-gear times** for this exact variant | After two failures: **diagnose with evidence, don't retry** |
| [8](prompts/round-08.md) | Exterior mirrors: glass floating without housing; dash front still floating | **In-game verification loop with standard views V1–V5**; raycast gap check; frit band sized from the driver's eye | **The game is the judge**: Blender renders are drafts |
| [sound](prompts/sound.md) | Engine sound | Record the real car; legal-source rules; strict input spec; FMOD template pipeline | **Owner's car = best source** |

## What made the biggest difference

1. **Driving / in-use references.** The cluster only looked right once a photo of it *while driving* showed how rpm is drawn.
2. **The engine addendum.** Half of round 3 was unimplementable until the requirements were translated into Prism3D mechanisms.
3. **Colour-tag diagnostics.** Two defects (a ghost mirror frame and a black band over the side glass) survived several "fixes" because they lived in files nobody was editing.
4. **Measured physics targets for the exact variant.** "Feels slow in 5th at 160" became "60–100 km/h in 5th must take 8.2 s".
5. **In-game acceptance.** Before round 8, requested features (e.g. the windshield frit band) were reported as done but never reached the game.

## Real-vehicle checks requested from the owner
- Tyre size on the sidewall (215/50 R17 vs 235/45 R17)
- Engine speed at 100 and 130 km/h in 6th (to confirm the final drive)
- Headliner/pillar colour
- Photos of parts that vary by market (rear fog lamp, third brake light, mirror details)
