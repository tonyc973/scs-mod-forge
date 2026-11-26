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


# ---------------------------------------------------------------- shared pieces
def step(s, x, y, w, h, code, title, lines, role):
    accent, fill = tint(role, s.theme)
    s.add('<g filter="url(#shadow)">')
    s.rect(x, y, w, h, s.t["bg"], stroke=s.t["border"], r=10)
    s.add("</g>")
    s.rect(x, y, 4, h, accent, r=2)
    s.rect(x + 14, y + 12, 30, 20, fill, r=6)
    s.text(x + 29, y + 26.5, code, size=11, weight=700, fill=accent, anchor="middle")
    s.text(x + 54, y + 27, title, size=14, weight=700)
    for i, l in enumerate(lines):
        s.text(x + 54, y + 47 + i * 17, l, size=11.8, fill=s.t["muted"])


def zone(s, x, y, w, h, num, kicker, title, subtitle, role):
    accent, fill = tint(role, s.theme)
    s.rect(x, y, w, h, fill, stroke=s.t["border"], r=16)
    s.rect(x, y, w, 6, accent, r=3)
    s.badge(x + 26, y + 34, num, accent)
    s.text(x + 46, y + 31, kicker.upper(), size=10.5, weight=700, fill=accent, ls=1.3)
    s.text(x + 46, y + 53, title, size=19, weight=700)
    s.text(x + 18, y + 80, subtitle, size=12, weight=500, fill=s.t["muted"])


def pill(s, x, y, label, color, w=None):
    w = w or (len(label) * 6.6 + 30)
    s.rect(x, y, w, 26, s.t["chip"], stroke=s.t["border"], r=13)
    s.add(f'<circle cx="{x + 13}" cy="{y + 13}" r="4" fill="{color}"/>')
    s.text(x + 23, y + 17.5, label, size=11.5, weight=500)
    return w


def label_box(s, cx, y, text, color, size=12):
    w = len(text) * 6.7 + 24
    s.rect(cx - w / 2, y - 15, w, 24, s.t["bg"], stroke=color, r=12)
    s.text(cx, y + 1.5, text, size=size, weight=600, fill=color, anchor="middle")


# ---------------------------------------------------------------- pipeline (main architecture)
def pipeline(theme):
    s = Svg(1280, 1010, theme,
            "scs-mod-forge architecture: Claude in Chrome researches real references and writes the prompt, "
            "Claude Code builds in Blender through MCP, ETS2 verifies")
    t = s.t
    R, B, G, Y, P = (ROLE["director"][0], ROLE["builder"][0], ROLE["game"][0], ROLE["modder"][0], ROLE["truth"][0])
    s.text(40, 46, "scs-mod-forge", size=13, weight=700, fill=t["muted"], ls=0.5)
    s.text(40, 74, "Research in the browser → build in Blender → verify in the game", size=22, weight=700)

    # sources band
    s.rect(24, 96, 1232, 92, t["panel"], stroke=t["border"], r=14)
    s.text(40, 120, "SOURCES", size=10.5, weight=700, fill=t["lane_text"], ls=1.5)
    s.text(40, 138, "the web, opened in Chrome", size=11.5, fill=t["muted"])
    x = 214
    for lab in ("Bing / Google Images", "OEM & dealer galleries", "Owner's manuals", "Review galleries",
                "Owner forums", "Road tests (e.g. ADAC)"):
        x += pill(s, x, 110, lab, P) + 8
    s.text(40, 168, "documentation & files", size=11.5, fill=t["muted"])
    x = 214
    for lab in ("SCS Modding Wiki", "SCS Blender Tools docs"):
        x += pill(s, x, 152, lab, R) + 8
    x += 24
    for lab in ("Vanilla game files (extracted)", "Your real car"):
        x += pill(s, x, 152, lab, B if "Vanilla" in lab else Y) + 8

    # zones
    zy, zh = 222, 600
    Z1, Z2, Z3 = (24, 430), (488, 420), (942, 314)
    zone(s, Z1[0], zy, Z1[1], zh, 1, "Research & prompt", "Claude + Claude in Chrome",
         "claude.ai + the Chrome extension: browses, views images, searches", "director")
    zone(s, Z2[0], zy, Z2[1], zh, 2, "Build", "Claude Code + Blender MCP",
         "in your mod project folder, connected to a running Blender", "builder")
    zone(s, Z3[0], zy, Z3[1], zh, 3, "Verify", "ETS2 / ATS",
         "Prism3D engine: the only judge", "game")

    sx, sw = Z1[0] + 16, Z1[1] - 32
    ys = [zy + 100 + i * 98 for i in range(5)]
    step(s, sx, ys[0], sw, 84, "1a", "Read your screenshots",
         ["names each defect precisely", "ranks the likely causes (normals, culling, IDs…)"], "director")
    step(s, sx, ys[1], sw, 84, "1b", "Hunt real photos in Chrome",
         ["image search, OEM / review galleries, forums", "pulls the direct image URLs from result pages"], "director")
    step(s, sx, ys[2], sw, 84, "1c", "Open and inspect every image",
         ["screenshot + zoom on details", "rejects aftermarket parts, wrong market or generation"], "director")
    step(s, sx, ys[3], sw, 84, "1d", "Check numbers and engine rules",
         ["dimensions, tyre size, road-test data", "SCS Wiki: what Prism3D can actually do"], "director")
    step(s, sx, ys[4], sw, 84, "1e", "Write round-prompt.md",
         ["table of reference URLs + caveats", "per defect: now · real · diagnose · build · accept"], "director")

    bx, bw = Z2[0] + 16, Z2[1] - 32
    step(s, bx, ys[0], bw, 84, "2a", "Load the rules, download refs",
         ["CLAUDE.md: engine truth, evidence rules", "curl the reference URLs into refs/, opens them"], "builder")
    step(s, bx, ys[1], bw, 84, "2b", "Measure and diagnose",
         ["photo_measure.py, mesh_audit.py", "colour-tagged test build when unclear"], "builder")
    # MCP stack inside step 2c
    y2c = ys[2]
    s.add('<g filter="url(#shadow)">')
    s.rect(bx, y2c, bw, 182, t["bg"], stroke=t["border"], r=10)
    s.add("</g>")
    s.rect(bx, y2c, 4, 182, B, r=2)
    accent, fill = tint("builder", theme)
    s.rect(bx + 14, y2c + 12, 30, 20, fill, r=6)
    s.text(bx + 29, y2c + 26.5, "2c", size=11, weight=700, fill=accent, anchor="middle")
    s.text(bx + 54, y2c + 27, "Model in Blender through MCP", size=14, weight=700)
    names = [("Claude Code", "sends bpy code"), ("Blender MCP server", "local socket"),
             ("Blender + SCS Blender Tools", "scene \u00b7 export")]
    for i, (n_, d_) in enumerate(names):
        yy = y2c + 44 + i * 44
        s.rect(bx + 54, yy, bw - 70, 34, fill, stroke=t["border"], r=8)
        s.text(bx + 66, yy + 21.5, n_, size=12.5, weight=700)
        s.text(bx + bw - 26, yy + 21.5, d_, size=11, fill=t["muted"], anchor="end")
        if i < 2:
            s.path(f"M{bx + 90},{yy + 35} L{bx + 90},{yy + 43}", t["arrow"], sw=1.6, marker="arrow")
            s.path(f"M{bx + 104},{yy + 43} L{bx + 104},{yy + 35}", t["arrow"], sw=1.6, marker="arrow")
    step(s, bx, ys[4], bw, 84, "2d", "Export the mod",
         [".pim / .pmd / .tobj / .dds + .sii definitions", "packed into the mod folder or .scs"], "builder")

    gx, gw = Z3[0] + 16, Z3[1] - 32
    step(s, gx, ys[0], gw, 84, "3a", "Load the mod", ["in your profile, restart", "the game if needed"], "game")
    step(s, gx, ys[1], gw, 84, "3b", "You take views V1–V5", ["same head position", "F12 = screenshot"], "game")
    step(s, gx, ys[2], gw, 84, "3c", "Screenshots folder", ["Documents/Euro Truck", "Simulator 2/screenshot/"], "game")
    # decision
    dy = ys[3]
    s.add('<g filter="url(#shadow)">')
    s.rect(gx, dy, gw, 182, t["bg"], stroke=t["border"], r=10)
    s.add("</g>")
    s.rect(gx, dy, 4, 182, G, r=2)
    afg, ffg = tint("game", theme)
    s.rect(gx + 14, dy + 12, 30, 20, ffg, r=6)
    s.text(gx + 29, dy + 26.5, "3d", size=11, weight=700, fill=afg, anchor="middle")
    s.text(gx + 54, dy + 27, "Compare with the photo", size=14, weight=700)
    s.text(gx + 54, dy + 47, "side by side, same framing", size=11.8, fill=t["muted"])
    s.rect(gx + 16, dy + 66, gw - 32, 44, ffg, stroke=G, r=8)
    s.text(gx + 30, dy + 85, "✓  matches the reference", size=12.5, weight=700, fill=G)
    s.text(gx + 30, dy + 101, "keep it, next defect", size=11.5, fill=t["muted"])
    s.rect(gx + 16, dy + 120, gw - 32, 44, fill, stroke=B, r=8)
    s.text(gx + 30, dy + 139, "✗  differs or got worse", size=12.5, weight=700, fill=B)
    s.text(gx + 30, dy + 155, "iterate in step 2, or revert", size=11.5, fill=t["muted"])

    # inner-zone flow arrows
    for xx, ww in ((sx, sw), (bx, bw), (gx, gw)):
        pass
    for i in range(4):
        cx_ = sx + 30
        s.path(f"M{cx_},{ys[i] + 86} L{cx_},{ys[i + 1] - 4}", t["arrow"], sw=1.6)
    for a_, b_ in ((ys[0], ys[1]), (ys[1], ys[2]), (ys[2] + 98, ys[4])):
        s.path(f"M{bx + 30},{a_ + 86} L{bx + 30},{b_ - 4}", t["arrow"], sw=1.6)
    for i in range(3):
        s.path(f"M{gx + 30},{ys[i] + 86} L{gx + 30},{ys[i + 1] - 4}", t["arrow"], sw=1.6)

    # sources -> zone 1 / zone 2
    s.path(f"M{Z1[0] + Z1[1] / 2},{190} L{Z1[0] + Z1[1] / 2},{zy - 4}", P, sw=2)
    s.path(f"M{Z2[0] + Z2[1] / 2 + 60},{190} L{Z2[0] + Z2[1] / 2 + 60},{zy - 4}", B, sw=1.6, dash="5 4")

    # zone 1 -> zone 2 (prompt) ; zone 2 -> zone 3 (mod): routed through the gaps, vertical labels
    def vlabel(cx, cy, text, color):
        w = len(text) * 6.7 + 22
        s.add(f'<g transform="rotate(-90 {cx} {cy})">')
        s.rect(cx - w / 2, cy - 12, w, 24, t["bg"], stroke=color, r=12)
        s.text(cx, cy + 4, text, size=11, weight=700, fill=color, anchor="middle")
        s.add("</g>")

    g1 = (Z1[0] + Z1[1] + Z2[0]) / 2
    y_from, y_to = ys[4] + 42, ys[0] + 42
    s.path(f"M{sx + sw + 2},{y_from} L{g1 - 8},{y_from} Q{g1},{y_from} {g1},{y_from - 8} "
           f"L{g1},{y_to + 8} Q{g1},{y_to} {g1 + 8},{y_to} L{bx - 6},{y_to}", R, sw=2.4)
    vlabel(g1, (y_from + y_to) / 2, "round-prompt.md + reference URLs", R)
    g2 = (Z2[0] + Z2[1] + Z3[0]) / 2
    s.path(f"M{bx + bw + 2},{y_from} L{g2 - 8},{y_from} Q{g2},{y_from} {g2},{y_from - 8} "
           f"L{g2},{y_to + 8} Q{g2},{y_to} {g2 + 8},{y_to} L{gx - 6},{y_to}", B, sw=2.4)
    vlabel(g2, (y_from + y_to) / 2, "exported mod files", B)

    # feedback loops below the zones
    yl1 = zy + zh + 34
    xs3 = Z3[0] + Z3[1] / 2
    xs2 = Z2[0] + Z2[1] / 2
    s.path(f"M{xs3},{zy + zh + 2} L{xs3},{yl1 - 10} Q{xs3},{yl1} {xs3 - 10},{yl1} L{xs2 + 10},{yl1} "
           f"Q{xs2},{yl1} {xs2},{yl1 - 10} L{xs2},{zy + zh + 6}", G, sw=2.4)
    label_box(s, (xs3 + xs2) / 2, yl1, "F12 screenshots → Claude Code compares and iterates", G, size=11.5)
    yl2 = yl1 + 58
    xs1 = Z1[0] + Z1[1] / 2
    s.path(f"M{xs3 + 60},{zy + zh + 2} L{xs3 + 60},{yl2 - 10} Q{xs3 + 60},{yl2} {xs3 + 50},{yl2} L{xs1 + 10},{yl2} "
           f"Q{xs1},{yl2} {xs1},{yl2 - 10} L{xs1},{zy + zh + 6}", Y, sw=2.4)
    label_box(s, (xs3 + xs1) / 2 + 40, yl2, "You → Claude: new screenshots + “what still looks wrong” = next round", Y,
              size=11.5)

    # footer legend
    fy = yl2 + 40
    s.text(40, fy + 14, "Inner loop (green): runs many times inside one round until the in-game view matches the photo.   "
                        "Outer loop (teal): one turn per round.", size=12, fill=t["muted"])
    return s


# ---------------------------------------------------------------- research detail
def research(theme):
    s = Svg(1280, 490, theme, "How Claude in Chrome finds and verifies reference photos")
    t = s.t
    R, P, B = ROLE["director"][0], ROLE["truth"][0], ROLE["builder"][0]
    s.text(40, 46, "scs-mod-forge · step 1 in detail", size=13, weight=700, fill=t["muted"], ls=0.5)
    s.text(40, 74, "How Claude in Chrome turns “the vents look fake” into verified reference photos", size=22,
           weight=700)
    W, H, gap = 220, 206, 20
    cards = [
        ("Search", ["image search with precise", "words: model, generation,", "part, view", "", "e.g. “honda civic 10th gen", "center air vent close up”"]),
        ("Extract URLs", ["script on the results page", "reads each hit’s direct", "image URL + source page", "(query strings stripped)", "", "→ a list, not thumbnails"]),
        ("Open & look", ["opens every candidate,", "takes a screenshot,", "zooms on the details that", "matter (louvers, labels,", "stitching, lamp layout)", ""]),
        ("Accept / reject", ["✗ aftermarket parts", "✗ other market / trim", "✗ wrong generation", "✓ OEM, manual, review", "✓ photo of the part", "     in use (lit, driving)"]),
        ("Reference table", ["id · what it shows ·", "caveats · URL", "", "scale anchors (known", "dimensions) for", "measuring from photos"]),
    ]
    x = 40
    for i, (title, lines) in enumerate(cards):
        accent = R if i != 3 else P
        a_, f_ = (tint("director", theme) if i != 3 else tint("truth", theme))
        s.add('<g filter="url(#shadow)">')
        s.rect(x, 110, W, H, t["bg"], stroke=t["border"], r=12)
        s.add("</g>")
        s.rect(x, 110, W, 5, a_, r=2)
        s.badge(x + 24, 142, i + 1, a_)
        s.text(x + 44, 147, title, size=15.5, weight=700)
        for k, l in enumerate(lines):
            s.text(x + 18, 180 + k * 20, l, size=12.2, fill=t["muted"])
        if i < len(cards) - 1:
            s.path(f"M{x + W + 3},{110 + H / 2} L{x + W + gap - 4},{110 + H / 2}", t["arrow"], sw=2)
        x += W + gap
    # outputs
    s.rect(40, 348, 1200, 112, t["panel"], stroke=t["border"], r=12)
    s.text(60, 376, "What ends up in the prompt for Claude Code", size=14, weight=700)
    rows = [
        ("Reference table", "only images that were opened and checked, each with caveats"),
        ("“Now” vs “real”", "what your screenshot shows vs how the real part looks, citing the image ids"),
        ("Numbers", "dimensions with sources (e.g. mirror protrusion from width with / without mirrors)"),
    ]
    for k, (a, b) in enumerate(rows):
        yy = 404 + k * 22
        s.add(f'<circle cx="{66}" cy="{yy - 4}" r="3" fill="{R}"/>')
        s.text(78, yy, a, size=12.5, weight=700)
        s.text(240, yy, b, size=12.5, fill=t["muted"])
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
        for name, fn in (("architecture", pipeline), ("research-step", research), ("sources-of-truth", truth)):
            print(save(name, theme, fn(theme)))


if __name__ == "__main__":
    main()
