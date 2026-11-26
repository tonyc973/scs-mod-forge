# Research brief (send this to Claude, with Claude in Chrome enabled)

Attach your in-game screenshots, then fill in and send:

---

I'm building a mod for **<Euro Truck Simulator 2 | American Truck Simulator>** (Prism3D engine: mods can't run code).
Vehicle: **<make, model, generation/code, year, body, market, trim, engine, gearbox>**.
The build agent is **Claude Code connected to Blender through MCP**, exporting with SCS Blender Tools.

What looks wrong (one line per screenshot, in the order attached):
1. <…>
2. <…>

Please:
1. Name each defect precisely and list the likely causes in order.
2. Use Chrome to find **real photos** of each part: close-ups, the driver's view, and in-use photos (lit, driving, reflecting). Open and inspect every image. Reject aftermarket parts, other markets and other generations, and note caveats.
3. Collect numbers that matter (dimensions, tyre size, measured performance), each with its source and the exact variant.
4. Check on the SCS Modding Wiki how Prism3D supports what's needed.
5. Write `round-prompt.md` for Claude Code following this structure: references table → per defect *now · real · diagnose · build · accept* → what not to touch → deliverables → questions for me about the real car.

Don't touch (working now): <cluster, steering wheel, …>
Still open from earlier rounds: <…>
