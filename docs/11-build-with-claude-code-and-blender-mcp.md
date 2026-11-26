# 11 · Build with Claude Code + Blender MCP

Step ② of the [architecture](01-architecture.md): Claude Code receives `round-prompt.md` and turns it into mod files, working inside a running Blender through MCP.

## The stack

```
Claude Code  (terminal, in your mod project folder)
     │  MCP tool calls: run Python (bpy), read scene/object info, viewport screenshots
     ▼
Blender MCP server
     │  local socket
     ▼
Blender add-on  →  Blender scene  +  SCS Blender Tools  →  export to the mod folder
```

## Setup

1. **Blender** (a version supported by your SCS Blender Tools release).
2. **SCS Blender Tools**: install and point it at your extracted base data, following the [SCS documentation](https://modding.scssoft.com/wiki/Documentation/Tools/SCS_Blender_Tools).
3. **A Blender MCP server**, e.g. the open-source `blender-mcp`: install its Blender add-on, start the connection from the add-on's panel, and register the server with Claude Code (`claude mcp add …`, as the server's README describes).
4. **Claude Code**, started in your mod project folder.
5. **Vanilla data**: extract the game archives (SCS extractor) into a read-only folder. Claude Code searches it for syntax patterns.
6. **Python tools** from this repo: `pip install -r tools/requirements.txt`.

## Project layout

```
my-civic-mod/
├── CLAUDE.md              ← standing rules (from templates/CLAUDE.md)
├── round-prompts/         ← one file per round, from Claude in Chrome
├── refs/                  ← reference photos downloaded by Claude Code (not shipped)
├── renders/               ← comparisons, overlays, measurements (not shipped)
├── tools/                 ← copied from this repo
├── blender/civic.blend    ← working file, with OLD_vN collections for history
├── mod/                   ← export target (def/, vehicle/, material/, …)
└── vanilla/ (read-only)   ← extracted game data
```

## How a build session runs

1. **You paste the prompt**: "Here is round 7: `round-prompts/round-07.md`".
2. **References**: Claude Code downloads every URL into `refs/round-07/` with `curl` and **opens each image**. If a site blocks the download, it asks you to save the image manually.
3. **Diagnose (gate G3)**:
   - `mesh_audit.py` on the objects in question;
   - if the source of a defect is unclear, a colour-tagged test build with `diag_color_tag.py`;
   - measurements with `photo_measure.py`, `gap_raycast.py`, `eye_line.py`.
   
   It writes down the cause before changing anything.
4. **Model through MCP**: it sends `bpy` code to Blender in small steps, inspects the scene and uses viewport screenshots to check its own work. Blender screenshots are drafts, not evidence.
5. **Export** with SCS Blender Tools into `mod/`, following vanilla `.sii` patterns.
6. **Ask for evidence**: "Load the mod and take V1 and V4 (daytime)."
7. **Compare (gate G4)**: it reads the newest files in the game's screenshot folder (or the ones you send) and builds side-by-side images with the reference (`compare_images.py`). Keep, iterate or revert.
8. **Report**: cause, files changed, comparisons, open differences, questions about the real car.

## Habits that made the difference

- **Small MCP steps.** One part at a time, saving the `.blend` between steps, so a bad command is cheap to undo.
- **Old parts stay.** Replaced objects move to an `OLD_vN` collection instead of being deleted.
- **Measure in Python, not by eye.** Gaps, heights and proportions come from scripts with printed numbers.
- **Never trust the viewport alone.** Culling, triangulation, mipmaps, lamp masks and mirror cameras only show their real behaviour in Prism3D.
- **Two failures → change method.** Colour-tag, then study how a working mod achieves the effect (technique only, no assets).
