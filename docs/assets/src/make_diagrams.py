#!/usr/bin/env python3
"""Generate the documentation diagrams (light + dark SVG variants).

    python docs/assets/src/make_diagrams.py

Writes docs/assets/<name>-light.svg and <name>-dark.svg. Edit the content here,
not the SVGs. Plain string templating, no dependencies.
"""
import math
import os
from html import escape

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "light": dict(bg="#FFFFFF", panel="#F6F8FA", border="#D0D7DE", text="#1F2328", muted="#59636E",
                  faint="#8C959F", lane="#F6F8FA", lane_text="#8C959F", arrow="#57606A", chip="#FFFFFF"),
    "dark": dict(bg="#0D1117", panel="#161B22", border="#30363D", text="#E6EDF3", muted="#9198A1",
                 faint="#6E7681", lane="#11161D", lane_text="#6E7681", arrow="#8B949E", chip="#0D1117"),
}
# role colours: (accent, light tint, dark tint)
ROLE = {
    "modder":   ("#0E9F8E", "#E6F6F4", "#0B2A27"),
    "director": ("#6366F1", "#EEEFFE", "#1C1E3D"),
    "builder":  ("#E08A1E", "#FDF3E6", "#33240F"),
    "game":     ("#22A55B", "#E8F6EE", "#0F2A1B"),
    "truth":    ("#8B5CF6", "#F3EEFE", "#241A3A"),
}


def tint(role, theme):
    a, l, d = ROLE[role]
    return a, (l if theme == "light" else d)


class Svg:
    def __init__(self, w, h, t, title):
        self.w, self.h, self.t, self.parts = w, h, THEMES[t], []
        self.theme = t
        self.title = title

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=13, weight=400, fill=None, anchor="start", italic=False, ls=0):
        fill = fill or self.t["text"]
        st = ' font-style="italic"' if italic else ""
        lsp = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
                 f'text-anchor="{anchor}"{st}{lsp}>{escape(s)}</text>')

    def rect(self, x, y, w, h, fill, stroke=None, r=12, sw=1, dash=None, opacity=None):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}{d}{o}/>')

    def path(self, d, stroke, sw=1.8, dash=None, marker="arrow", fill="none"):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
                 f'stroke-linecap="round" stroke-linejoin="round"{ds}{m}/>')

    def badge(self, x, y, n, color):
        self.add(f'<circle cx="{x}" cy="{y}" r="11" fill="{color}"/>')
        self.text(x, y + 4.5, str(n), size=12, weight=700, fill="#FFFFFF", anchor="middle")

    def render(self):
        a = self.t["arrow"]
        defs = f'''<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{a}"/></marker>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
    <feDropShadow dx="0" dy="1.5" stdDeviation="2.2" flood-color="#000" flood-opacity="{0.08 if self.theme == 'light' else 0.45}"/>
  </filter>
</defs>'''
        body = "\n".join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" font-family="{FONT}" role="img" aria-label="{escape(self.title)}">\n'
                f'<title>{escape(self.title)}</title>\n{defs}\n'
                f'<rect width="{self.w}" height="{self.h}" rx="16" fill="{self.t["bg"]}"/>\n{body}\n</svg>\n')


def save(name, theme, svg):
    path = os.path.join(OUT, f"{name}-{theme}.svg")
    with open(path, "w") as f:
        f.write(svg.render())
    return path


# ---------------------------------------------------------------- overview
CW = 264                    # card width
COLS = [32, 32 + CW + 42, 32 + 2 * (CW + 42), 32 + 3 * (CW + 42)]  # x of the four role columns (cards at +30)


def role_card(s, x, y, w, h, role, kicker, title, tool, bullets):
    accent, fill = tint(role, s.theme)
    s.add('<g filter="url(#shadow)">')
    s.rect(x, y, w, h, s.t["bg"], stroke=s.t["border"], r=14)
    s.add("</g>")
    s.rect(x, y, w, 5, accent, r=2)
    s.rect(x + 1, y + 5, w - 2, 56, fill, r=0)
    s.text(x + 18, y + 27, kicker.upper(), size=10.5, weight=700, fill=accent, ls=1.2)
    s.text(x + 18, y + 49, title, size=18, weight=700)
    s.text(x + 18, y + 84, tool, size=12, weight=500, fill=s.t["muted"])
    for i, b in enumerate(bullets):
        yy = y + 112 + i * 24
        s.add(f'<circle cx="{x + 22}" cy="{yy - 4}" r="2.6" fill="{accent}"/>')
        s.text(x + 33, yy, b, size=12.5)


def truth_card(s, x, y, w, h, title, lines):
    accent, fill = tint("truth", s.theme)
    s.rect(x, y, w, h, fill, stroke=s.t["border"], r=12)
    s.rect(x, y, 4, h, accent, r=2)
    s.text(x + 16, y + 25, title, size=13.5, weight=700)
    for i, l in enumerate(lines):
        s.text(x + 16, y + 46 + i * 18, l, size=11.5, fill=s.t["muted"])


def chip(s, x, y, label, role):
    accent, _ = tint(role, s.theme)
    w = 18 + len(label) * 6.7 + 14
    s.rect(x, y, w, 28, s.t["chip"], stroke=s.t["border"], r=14)
    s.add(f'<circle cx="{x + 14}" cy="{y + 14}" r="4" fill="{accent}"/>')
    s.text(x + 25, y + 18.5, label, size=11.5, weight=500)
    return w


def lane(s, y, h, label):
    s.rect(24, y, s.w - 48, h, s.t["lane"], r=12)
    s.add(f'<text x="38" y="{y + h / 2}" font-size="10" font-weight="700" fill="{s.t["lane_text"]}" '
          f'letter-spacing="2" text-anchor="middle" transform="rotate(-90 38 {y + h / 2})">{label}</text>')


def overview(theme):
    s = Svg(1280, 900, theme, "scs-mod-forge architecture: roles, sources of truth, artifacts and the verification loop")
    t = s.t
    s.text(56, 50, "scs-mod-forge", size=13, weight=700, fill=t["muted"], ls=0.5)
    s.text(56, 78, "Architecture: four roles, one loop, the game as the judge", size=22, weight=700)

    # lanes
    lane(s, 104, 128, "TRUTH")
    lane(s, 252, 300, "ROLES")
    lane(s, 572, 196, "ARTIFACTS")

    # truth cards
    truth_card(s, COLS[0] + 30, 118, CW, 100, "Real vehicle",
               ["tyre size, rpm at speed, colours", "owner's photos & measurements", "highest authority"])
    truth_card(s, COLS[1] + 30, 118, CW, 100, "Real-world references",
               ["OEM press, owner's manual diagrams", "road tests with measurements", "close-ups, night & in-use photos"])
    truth_card(s, COLS[2] + 30, 118, CW, 100, "Engine truth",
               ["SCS Modding Wiki", "vanilla game files (patterns)", "SCS Blender Tools docs"])
    truth_card(s, COLS[3] + 30, 118, CW, 100, "Measured behaviour",
               ["in-game screenshots (F12)", "telemetry CSV (speed vs time)", "what actually renders & drives"])

    # role cards
    y0, h0 = 268, 232
    role_card(s, COLS[0] + 30, y0, CW, h0, "modder", "Owner · QA", "Modder", "human, plays the game",
              ["Reports defects in plain words", "Takes the requested F12 views", "Confirms specs on the real car",
               "Accepts or rejects a round"])
    role_card(s, COLS[1] + 30, y0, CW, h0, "director", "Research · Direction", "Director",
              "chat assistant + web + browser",
              ["Triages each screenshot", "Finds & inspects references", "Checks what Prism3D supports",
               "Writes the round prompt"])
    role_card(s, COLS[2] + 30, y0, CW, h0, "builder", "Execution", "Builder",
              "Claude Code + Blender MCP",
              ["Diagnoses with evidence", "Measures, models, exports", "Compares game vs reference",
               "A/B: keeps or reverts"])
    role_card(s, COLS[3] + 30, y0, CW, h0, "game", "Ground truth", "Game",
              "ETS2 / ATS · Prism3D engine",
              ["Loads the exported mod", "Renders views V1–V5", "Logs driving telemetry",
               "The only acceptance judge"])

    a = t["arrow"]
    ry = y0 + 118  # role arrows y
    # 1 modder -> director, 3 director -> builder, 4 builder -> game
    for i, n in ((0, 1), (1, 3), (2, 4)):
        x1 = COLS[i] + 30 + CW
        x2 = COLS[i + 1] + 30
        s.path(f"M{x1 + 4},{ry} L{x2 - 6},{ry}", a, sw=2)
        s.badge((x1 + x2) / 2, ry - 20, n, tint(["modder", "director", "builder"][i], theme)[0])
    # 2 truth -> director (references) and engine truth -> director & builder
    s.path(f"M{COLS[1] + 30 + CW / 2},{218} L{COLS[1] + 30 + CW / 2},{y0 - 6}", a, sw=2)
    s.badge(COLS[1] + 30 + CW / 2 + 20, 243, 2, ROLE["truth"][0])
    s.path(f"M{COLS[2] + 30 + 60},{218} C{COLS[2] + 30 + 60},{240} {COLS[1] + 30 + CW - 40},{236} "
           f"{COLS[1] + 30 + CW - 40},{y0 - 6}", a, sw=1.6, dash="5 4")
    s.path(f"M{COLS[2] + 30 + CW / 2},{218} L{COLS[2] + 30 + CW / 2},{y0 - 6}", a, sw=1.6, dash="5 4")
    s.path(f"M{COLS[0] + 30 + CW / 2},{218} L{COLS[0] + 30 + CW / 2},{y0 - 6}", a, sw=1.6, dash="5 4")
    s.path(f"M{COLS[3] + 30 + CW / 2},{y0 - 6} L{COLS[3] + 30 + CW / 2},{218 + 4}", a, sw=1.6, dash="5 4")

    # verification loop under the cards
    yb = y0 + h0  # 500
    gx = COLS[3] + 30 + CW / 2
    mx = COLS[0] + 30 + CW / 2
    bx = COLS[2] + 30 + CW / 2
    s.path(f"M{gx},{yb + 4} L{gx},{yb + 36} Q{gx},{yb + 44} {gx - 8},{yb + 44} L{mx + 8},{yb + 44} "
           f"Q{mx},{yb + 44} {mx},{yb + 36} L{mx},{yb + 8}", tint("game", theme)[0], sw=2)
    s.badge((gx + mx) / 2 + 120, yb + 44, 5, tint("game", theme)[0])
    s.text((gx + mx) / 2 + 138, yb + 40, "views V1–V5 on screen", size=11.5, fill=t["muted"])
    s.path(f"M{mx + 40},{yb + 8} L{mx + 40},{yb + 22} Q{mx + 40},{yb + 28} {mx + 46},{yb + 28} "
           f"L{bx - 46},{yb + 28} Q{bx - 40},{yb + 28} {bx - 40},{yb + 22} L{bx - 40},{yb + 8}",
           tint("modder", theme)[0], sw=2)
    s.badge(mx + 150, yb + 28, 6, tint("modder", theme)[0])
    s.text(mx + 168, yb + 24, "F12 screenshots", size=11.5, fill=t["muted"])
    # 7: compare / iterate loop, drawn in the gap between Builder and Game
    lcx, lcy, lr = COLS[3] + 30 - 23, yb - 52, 13
    bc = tint("builder", theme)[0]
    s.path(f"M{lcx + lr},{lcy} A{lr},{lr} 0 1 1 {lcx},{lcy - lr}", bc, sw=2)
    s.badge(lcx, lcy + 30, 7, bc)
    # artifacts
    rows = {
        0: [("Bug screenshots", "modder"), ("Plain-words complaint", "modder"), ("In-game views V1–V5", "modder"),
            ("Owner's measurements", "modder")],
        1: [("Reference table", "director"), ("Round prompt", "director"), ("Engine-truth notes", "director")],
        2: [("CLAUDE.md rules", "builder"), ("Diagnostic build", "builder"), ("Measurements", "builder"),
            ("A/B comparisons", "builder"), ("Round report", "builder")],
        3: [("Exported mod", "game"), ("Telemetry CSV", "game")],
    }
    for col, items in rows.items():
        x = COLS[col] + 30
        y = 590
        for lab, role in items:
            chip(s, x, y, lab, role)
            y += 34

    # legend
    ly = 800
    s.rect(24, ly - 12, s.w - 48, 88, t["panel"], stroke=t["border"], r=12)
    steps = [
        (1, "modder", "Modder reports defects with screenshots"),
        (2, "truth", "Director gathers & inspects references"),
        (3, "director", "Director hands over one round prompt"),
        (4, "builder", "Builder diagnoses, builds, exports the mod"),
        (5, "game", "Game renders the agreed views V1–V5"),
        (6, "modder", "Modder sends F12 screenshots back"),
        (7, "builder", "Builder compares, iterates or reverts"),
    ]
    for i, (n, role, txt) in enumerate(steps):
        col, row = i % 4, i // 4
        x = 48 + col * 305
        y = ly + 14 + row * 34
        s.badge(x + 11, y - 4, n, ROLE[role][0])
        s.text(x + 30, y + 1, txt, size=12)
    s.text(48 + 3 * 305 + 30, ly + 49, "Dashed: consulted sources", size=12, fill=t["muted"], italic=True)
    return s


# ---------------------------------------------------------------- round loop
OWNER = {"modder": "Modder", "director": "Director", "builder": "Builder", "game": "Game · with Modder",
         "truth": "Director"}


def stage_card(s, x, y, w, h, n, name, role, lines):
    accent, fill = tint(role, s.theme)
    s.add('<g filter="url(#shadow)">')
    s.rect(x, y, w, h, s.t["bg"], stroke=s.t["border"], r=14)
    s.add("</g>")
    s.rect(x, y, w, 5, accent, r=2)
    s.badge(x + 26, y + 32, n, accent)
    s.text(x + 46, y + 37, name, size=15.5, weight=700)
    s.text(x + 18, y + 62, OWNER[role].upper(), size=10, weight=700, fill=accent, ls=1.1)
    for i, l in enumerate(lines):
        s.text(x + 18, y + 86 + i * 19, l, size=12.5, fill=s.t["muted"])


def round_loop(theme):
    s = Svg(1280, 710, theme, "The round loop: nine stages from screenshot to accepted change")
    t = s.t
    s.text(56, 50, "scs-mod-forge", size=13, weight=700, fill=t["muted"], ls=0.5)
    s.text(56, 78, "One round: from \u201cthis looks wrong\u201d to \u201caccepted in game\u201d", size=22, weight=700)
    W, H, G = 220, 148, 28
    xs = [40 + i * (W + G) for i in range(5)]
    y1, y2 = 120, 340
    row1 = [
        ("Capture", "modder", ["F12 screenshots of what", "looks wrong + one plain", "line per defect"]),
        ("Triage", "director", ["observed (neutral)", "likely causes, ranked", "real-world target"]),
        ("References", "truth", ["find, open, inspect", "rank by source type", "note caveats & scale"]),
        ("Engine truth", "director", ["how does Prism3D do it?", "cite wiki / vanilla file", "else: ask, then wait"]),
        ("Round prompt", "director", ["now \u00b7 real \u00b7 diagnose", "build \u00b7 accept", "protect what works"]),
    ]
    row2 = [  # placed right-to-left
        ("Diagnose", "builder", ["mesh audit", "colour-tag build", "raycasts & measurements"]),
        ("Build", "builder", ["measure \u2192 model", "materials, UVs", "export with SCS tools"]),
        ("Verify in game", "game", ["views V1\u2013V5 (F12)", "side by side with refs", "A/B: keep or revert"]),
        ("Report & close", "modder", ["diagnosis, evidence", "open differences", "checklist ticked"]),
    ]
    for i, (name, role, lines) in enumerate(row1):
        stage_card(s, xs[i], y1, W, H, i + 1, name, role, lines)
        if i < 4:
            s.path(f"M{xs[i] + W + 4},{y1 + H / 2} L{xs[i + 1] - 6},{y1 + H / 2}", t["arrow"], sw=2)
    for j, (name, role, lines) in enumerate(row2):
        col = 4 - j
        stage_card(s, xs[col], y2, W, H, 6 + j, name, role, lines)
        if j < 3:
            s.path(f"M{xs[col] - 4},{y2 + H / 2} L{xs[col - 1] + W + 6},{y2 + H / 2}", t["arrow"], sw=2)
    # 5 -> 6 (down)
    cx5 = xs[4] + W / 2
    s.path(f"M{cx5},{y1 + H + 4} L{cx5},{y2 - 6}", t["arrow"], sw=2)
    # 8 -> 6 feedback (iterate)
    bc = tint("builder", theme)[0]
    x8, x6 = xs[2] + W / 2, xs[4] + W / 2
    s.path(f"M{x8},{y2 + H + 4} C{x8},{y2 + H + 66} {x6},{y2 + H + 66} {x6},{y2 + H + 8}", bc, sw=2, dash="6 5")
    s.text((x8 + x6) / 2, y2 + H + 76, "not matching the reference \u2192 iterate, or revert", size=12.5,
           weight=600, fill=bc, anchor="middle")
    # 9 -> next round (back to 1)
    x9 = xs[1]
    cx1 = xs[0] + W / 2
    mc = tint("modder", theme)[0]
    s.path(f"M{x9 - 4},{y2 + H / 2} L{cx1 + 10},{y2 + H / 2} Q{cx1},{y2 + H / 2} {cx1},{y2 + H / 2 - 10} "
           f"L{cx1},{y1 + H + 8}", mc, sw=2)
    s.text(cx1 + 12, y2 + 20, "next round", size=12.5, weight=600, fill=mc)
    # rules strip
    ry = 600
    s.rect(24, ry, 1232, 84, t["panel"], stroke=t["border"], r=12)
    s.text(48, ry + 32, "Rules that hold in every round", size=14, weight=700)
    rules = ["The game is the judge", "No reference, no work", "Measure, don\u2019t eyeball",
             "A/B or revert", "Two failures \u2192 diagnose, don\u2019t retry", "Never invent engine attributes"]
    for k, r_ in enumerate(rules):
        col, row = k % 3, k // 3
        x = 330 + col * 310
        y = ry + 32 + row * 26
        s.add(f'<circle cx="{x}" cy="{y - 4}" r="3" fill="{t["arrow"]}"/>')
        s.text(x + 12, y, r_, size=13)
    # role legend (top right)
    lx = 1232
    for role, lab in reversed((("modder", "Modder"), ("director", "Director"), ("truth", "References"),
                               ("builder", "Builder"), ("game", "Game"))):
        lx -= 22 + len(lab) * 7
        s.add(f'<circle cx="{lx}" cy="{73}" r="5" fill="{ROLE[role][0]}"/>')
        s.text(lx + 10, 77.5, lab, size=12, fill=t["muted"])
    return s


# ---------------------------------------------------------------- truth hierarchy
def truth(theme):
    s = Svg(1280, 520, theme, "Sources of truth, in priority order")
    t = s.t
    s.text(56, 50, "scs-mod-forge", size=13, weight=700, fill=t["muted"], ls=0.5)
    s.text(56, 78, "Where truth comes from (highest priority first)", size=22, weight=700)
    levels = [
        ("Real vehicle", "the modder's own car: measurements, photos, rpm at speed", "modder"),
        ("The game", "what actually renders and how it drives: screenshots, telemetry", "game"),
        ("SCS docs & vanilla files", "what Prism3D supports and how vanilla content does it", "director"),
        ("OEM & independent measurements", "press images, owner's manuals, road tests (e.g. ADAC)", "truth"),
        ("Enthusiast sources", "forums, owner photos: cross-check, watch for modifications", "builder"),
        ("The AI's memory", "lowest priority: never used alone", None),
    ]
    top, step = 112, 64
    for i, (name, desc, role) in enumerate(levels):
        w = 1180 - i * 80
        x = (1280 - w) / 2
        y = top + i * step
        accent, fill = (tint(role, theme) if role else (t["faint"], t["panel"]))
        s.rect(x, y, w, 52, fill, stroke=t["border"], r=12)
        s.rect(x, y, 6, 52, accent, r=3)
        s.badge(x + 32, y + 26, i + 1, accent)
        s.text(x + 54, y + 31, name, size=15, weight=700)
        s.text(600, y + 31, desc, size=13, fill=t["muted"])
    return s


def main():
    for theme in THEMES:
        for name, fn in (("architecture", overview), ("round-loop", round_loop), ("sources-of-truth", truth)):
            print(save(name, theme, fn(theme)))


if __name__ == "__main__":
    main()
