#!/usr/bin/env python3
"""Compare an in-game screenshot with a reference image.

Outputs three files with the given prefix:
  <prefix>_side.png     side by side (screenshot | reference), same height
  <prefix>_overlay.png  50/50 blend (reference resized to the screenshot)
  <prefix>_diff.png     per-pixel difference heat map + mean difference printed

For meaningful overlays, crop both images to the same region first
(--crop-a / --crop-b take x0 y0 x1 y1 in pixels of each image).

Example:
    python compare_images.py ingame_v1.png refs/C10.jpg -o renders/compare_v1
"""
import argparse

import numpy as np
from PIL import Image, ImageDraw


def load(path, crop):
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(tuple(crop))
    return im


def label(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 8 + 7 * len(text), 18], fill=(0, 0, 0))
    d.text((4, 3), text, fill=(255, 255, 255))
    return im


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("screenshot")
    p.add_argument("reference")
    p.add_argument("-o", "--out", required=True, help="output prefix")
    p.add_argument("--crop-a", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--crop-b", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    a = p.parse_args()

    shot = load(a.screenshot, a.crop_a)
    ref = load(a.reference, a.crop_b)

    # side by side at equal height
    h = max(shot.height, ref.height)
    s1 = shot.resize((round(shot.width * h / shot.height), h))
    r1 = ref.resize((round(ref.width * h / ref.height), h))
    side = Image.new("RGB", (s1.width + r1.width + 10, h), (40, 40, 40))
    side.paste(label(s1.copy(), "GAME"), (0, 0))
    side.paste(label(r1.copy(), "REFERENCE"), (s1.width + 10, 0))
    side.save(f"{a.out}_side.png")

    # overlay + diff at screenshot resolution
    r2 = ref.resize(shot.size)
    Image.blend(shot, r2, 0.5).save(f"{a.out}_overlay.png")
    diff = np.abs(np.asarray(shot, dtype=np.int16) - np.asarray(r2, dtype=np.int16)).mean(axis=2)
    heat = np.clip(diff * 3, 0, 255).astype(np.uint8)
    rgb = np.stack([heat, np.zeros_like(heat), 255 - heat], axis=2)
    Image.fromarray(rgb).save(f"{a.out}_diff.png")
    print(f"mean abs difference: {diff.mean():.1f} / 255 (only meaningful for aligned crops)")
    print(f"wrote {a.out}_side.png, {a.out}_overlay.png, {a.out}_diff.png")


if __name__ == "__main__":
    main()
