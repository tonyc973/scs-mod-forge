# Standing rules for this mod project (Claude Code)

## Project
- Game: <Euro Truck Simulator 2 | American Truck Simulator>, version <x.yy>. Engine: **Prism3D**.
- Vehicle: <make, model, year, engine, gearbox, market>.
- Blender is driven through MCP; export with **SCS Blender Tools**.
- Vanilla extracted data (read-only): `<path>`.
- Round prompts come from Claude + Claude in Chrome (research agent) in `round-prompts/`. They contain verified reference URLs: download them with `curl` into `refs/round-NN/` and **open every image** before modeling. If a download is blocked, ask me to save the image.
- Renders and comparisons: `renders/`. Tools: `tools/`.

## Engine truth (non-negotiable)
- **Mods cannot run code.** No scripts, custom shaders or runtime camera logic. Use only: bone animations bound to vehicle values, dashboard UI element IDs, the lamp material + mask system, engine mirror cameras, vanilla `eut2.*` effects, FMOD banks from the SCS template.
- **Never invent `.sii` attributes or effect names.** Every attribute you use must appear in a vanilla file (cite the path) or on the SCS Modding Wiki (cite the page). If you can't find a mechanism, say so and propose the closest alternative; wait for approval.

## Evidence
- **Blender renders are drafts. Acceptance requires in-game screenshots.**
- Standard views (same head position, default interior camera):
  - V1 straight ahead · V2 head left ~60° · V3 head right ~60° · V4 down-forward at the dash · V5 V1 at night with lights on.
- After a change, ask me for specific views. Read the screenshots from `<Documents/Euro Truck Simulator 2/screenshot/>` (or I'll send them), **open them**, and compare each next to its reference.
- **A/B or revert**: keep a change only if "after" is clearly closer to the reference than "before".

## Method
- No reference, no modeling: open the references for a component before touching it.
- Measure, don't eyeball: use `tools/photo_measure.py`, published dimensions and scale anchors.
- Diagnose before fixing: run `tools/blender/mesh_audit.py` on touched objects. If the source of a visible defect is unclear, make a colour-tagged diagnostic build (`tools/blender/diag_color_tag.py`) and log it in `diag_colors.md`.
- Escalate after two failed attempts on the same item: diagnostics + study how a working mod achieves it (learn the technique, never copy assets).
- Keep old parts in `OLD_vN` collections; don't delete history mid-round.
- Don't touch systems marked as working in the current round prompt.

## Real-vehicle truth
- Specs from the internet are hypotheses. When a value matters (tyre size, rpm at speed, colours), list it as a question for me; I can check the real vehicle.

## Legal
- Reference photos are linked, never copied into the mod. Sounds only from my recordings or properly licensed sources.
