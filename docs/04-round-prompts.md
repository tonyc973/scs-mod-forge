# 04 · Writing round prompts

A round prompt is a **work order with built-in proof requirements**. The test of a good prompt: *could the agent claim success without actually fixing the problem?* If yes, the prompt is not finished.

Template: [`templates/round-prompt.md`](../templates/round-prompt.md)

## 1. Anatomy

```
# Title (vehicle, round number, engine)

Intro: what improved, what this round covers, what not to touch.

## 0. Rules / process for this round
   - engine constraints (link to standing rules)
   - verification loop + standard views
   - A/B or revert
   - new rules learned from the last round's failures

## 1. References (table: id · what it shows · caveats · URL)

## 2..N. One section per defect
   ### Now        - neutral description of the screenshot
   ### Real       - how the real part looks, citing reference ids
   ### Diagnose   - ordered list of likely causes and how to check each one
   ### Build      - concrete, measurable steps
   ### Accept     - which in-game views, next to which references, which numbers

## N+1. Deliverables
```

## 2. Rules that make prompts robust

1. **Describe "now" before "real".** The agent must see the delta. "Glass floats, a white sliver where the housing should be" points at normals and culling. "Make the mirror realistic" points nowhere.
2. **Reference ids everywhere.** "Four horizontal louvers (count them on R4)" beats "a few louvers".
3. **Numbers with sources.** "Each mirror protrudes ~138 mm (2076 mm − 1799 mm, divided by 2)" can be checked. "Realistic size" cannot.
4. **Deterministic steps for geometry problems.** "Raycast along the dash edge every 20 mm; target ≤ 3 mm; report max before/after."
5. **Engine-truth in the step, not as a footnote.** "Use the lamp material with the RGBA mask (R blinkers, G high beam/brake, B low beam/reverse/DRL, A position) and the Lamp UV Tool tiles" instead of "make the lights work".
6. **Ordered diagnosis.** List likely causes in order and how to rule each out. This stops random fixes.
7. **Escalation clause.** "If this fails twice, colour-tag diagnose and study a working mod's technique; if the engine can't do it, report evidence and wait for approval."
8. **Acceptance = in-game views next to named references.** Never "looks good".
9. **Protect what works.** Name the systems not to touch.
10. **Ask the owner.** List what the modder must confirm on the real vehicle; don't let internet specs silently override reality.

## 3. Writing about the "real" part

Describe the real part the way you would to a modeler who has never seen it:

- **Structure**: what pieces, in what order (e.g. "frame → 4 louvers → chrome tab on the 2nd louver → recessed vertical vanes → dark duct").
- **Proportions**: relative to something measurable.
- **Materials**: colour (hex), roughness, metal or not, texture (grain, perforation).
- **Behaviour**: what lights, moves or reflects, and when.
- **What it is not**: "no needle; the rpm is a white fill". "No ring around the glass; nearly frameless".

## 4. Prompt evolution in the Civic project

| Round | What the prompt added | Why |
|---|---|---|
| 1 | Reference links + component-by-component description | Baseline was generic and "cartoonish" |
| 2 | Diagnosis lists for artifacts (n-gons, normals, z-fighting) | Sawtooth pillars, see-through gaps |
| 3 | Measured cluster geometry, behaviour from driving photos | Cluster didn't resemble the real one |
| 3.1 | **Engine addendum**: Prism3D cannot run code | Round 3 assumed a scriptable engine |
| 4 | Dashboard UI element IDs, lamp/indicator mapping table | Speed missing, no warning lamps |
| 5 | **A/B-or-revert rule**, bounding-box overlap check for text | Text overlapping the speed |
| 6 | Exterior, lights (lamp mask system), physics targets | Scope extended to the whole car |
| 7 | **Colour-tag diagnostics**, "learn from a working mod", measured in-gear data | Mirror failed four times |
| 8 | **In-game verification loop with standard views**, raycast-based geometry | Fixes "done" in Blender but absent in game |

The full prompts are in [`examples/civic-fc/prompts/`](../examples/civic-fc/prompts/).
