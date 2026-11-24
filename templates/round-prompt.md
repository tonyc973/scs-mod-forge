# <Vehicle> – round <N> (<game> / Prism3D)

<!-- 2–3 lines: what improved since last round, what this round covers, what must NOT be touched. -->
Progress since round <N-1>: <…>. This round covers <K> items. Do not touch: <working systems>.

## 0. Rules for this round
- Standing rules in `CLAUDE.md` apply (engine truth, no invented attributes, in-game acceptance).
- **Verification loop**: after each item, ask me for screenshots from views <V1…V5>; compare each one next to its reference.
- **A/B or revert**: keep a change only if "after" is clearly closer to the reference.
- **Escalation**: if an item fails twice, use colour-tag diagnostics and study a working mod's technique before trying again.
- <New rule learned from the previous round's failure, if any.>

## 1. References
| id | what it shows | caveats | url |
|---|---|---|---|
| R1 | | | |
| R2 | | | |

Docs: <SCS wiki pages relevant to this round>

---

## 2. <Item 1 name>

### Now
<Neutral description of the screenshot: what is visible, where, how it is wrong.>

### Real
<How the real part looks, citing reference ids. Structure → proportions (with a scale anchor) → materials (hex, roughness) → behaviour → what it is NOT.>

### Diagnose (in order)
1. <Most likely cause>: how to check it.
2. <Next cause>: how to check it.

### Build
1. <Concrete, measurable step. Prefer scripts/measurements over eyeballing.>
2. <…>

### Accept
- In-game <view(s)> next to <reference ids>.
- Numbers: <e.g. gap ≤ 3 mm, overlay deviation ≤ 2 %, test times within ±5 %>.

---

## 3. <Item 2 name>
<same structure>

---

## N. Carried-over open items
- <Requests from earlier rounds not yet visible in game.>

## N+1. Deliverables
1. Diagnosis per item (what the cause was).
2. Files changed.
3. In-game A/B screenshots next to references, with your verdict.
4. Remaining differences and why.
5. What I must check or measure on the real vehicle.
