import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 440
F = "/usr/share/fonts/opentype/inter/"
def font(name, size):
    try: return ImageFont.truetype(F + name, size)
    except OSError: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
f_title = font("Inter-Bold.otf", 62)
f_sub = font("Inter-Medium.otf", 21)
f_kick = font("Inter-SemiBold.otf", 14)
f_chip = font("Inter-SemiBold.otf", 15)
f_cap = font("Inter-Regular.otf", 12)

def base():
    im = Image.new("RGB", (W, H), (13, 17, 23))
    d = ImageDraw.Draw(im)
    for y in range(H):  # subtle vertical gradient
        t = y / H
        c = (int(13 + 6 * t), int(17 + 7 * t), int(23 + 12 * t))
        d.line([(0, y), (W, y)], fill=c)
    return im

def text_layer():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = 56
    d.text((x, 92), "FOR EURO TRUCK SIMULATOR 2 & AMERICAN TRUCK SIMULATOR MODDERS", font=f_kick, fill=(145, 152, 161))
    d.text((x - 3, 116), "scs-mod-forge", font=f_title, fill=(230, 237, 243))
    d.text((x, 200), "Research in the browser → build in Blender", font=f_sub, fill=(200, 208, 216))
    d.text((x, 228), "→ verify in the game", font=f_sub, fill=(200, 208, 216))
    chips = [("1", "Claude in Chrome", (99, 102, 241)), ("2", "Claude Code + Blender MCP", (224, 138, 30)),
             ("3", "ETS2 / ATS", (34, 165, 91))]
    y = 290
    for n, lab, col in chips:
        tw = d.textlength(lab, font=f_chip)
        w = tw + 52
        d.rounded_rectangle([x, y, x + w, y + 34], radius=17, fill=(22, 27, 34), outline=(48, 54, 61))
        d.ellipse([x + 9, y + 7, x + 29, y + 27], fill=col)
        d.text((x + 19, y + 17), n, font=font("Inter-Bold.otf", 12), fill=(255, 255, 255), anchor="mm")
        d.text((x + 38, y + 8), lab, font=f_chip, fill=(230, 237, 243))
        x += w + 10
    d.text((56, 350), "Car: original 3D model, built and rendered in Blender", font=f_cap, fill=(110, 118, 129))
    return lay

def car_frame(path):
    c = Image.open(path).convert("RGB").resize((780, 440))
    import numpy as np
    w_, h_ = c.size
    xs = np.clip(np.arange(w_) / 170.0, 0, 1) ** 1.4
    ys_top = np.clip(np.arange(h_) / 70.0, 0, 1)
    ys_bot = np.clip((h_ - 1 - np.arange(h_)) / 50.0, 0, 1)
    m = np.outer(ys_top * ys_bot, xs) * 255
    mask = Image.fromarray(m.astype("uint8"), "L")
    return c, mask

frames = sorted(glob.glob(os.path.join(HERE, "frames", "f*.png")))
bg = base(); tl = text_layer()
out = []
for p in frames:
    im = bg.copy()
    c, m = car_frame(p)
    im.paste(c, (W - 780, 0), m)
    im.paste(tl, (0, 0), tl)
    out.append(im)
# shared palette built from every frame (downscaled) + the text layer at full size
thumbs = [fr.resize((W // 4, H // 4)) for fr in out]
mos = Image.new("RGB", (W, H + (H // 4) * ((len(thumbs) + 3) // 4)))
mos.paste(out[0], (0, 0))
for i, th in enumerate(thumbs):
    mos.paste(th, ((i % 4) * (W // 4), H + (i // 4) * (H // 4)))
base_pal = mos.quantize(colors=244, method=Image.Quantize.MEDIANCUT).getpalette()[:244 * 3]
extra = [(99, 102, 241), (224, 138, 30), (34, 165, 91), (255, 255, 255), (230, 237, 243), (200, 208, 216),
         (145, 152, 161), (110, 118, 129), (22, 27, 34), (48, 54, 61), (13, 17, 23), (235, 60, 40)]
pal = Image.new("P", (1, 1))
pal.putpalette(base_pal + [c for rgb in extra for c in rgb])
q = [fr.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG) for fr in out]
q[0].save(os.path.join(HERE, "..", "..", "banner.gif"), save_all=True, append_images=q[1:], duration=90, loop=0, optimize=True, disposal=1)
out[0].save(os.path.join(HERE, "banner_still.png"))
print(len(out), "frames")
