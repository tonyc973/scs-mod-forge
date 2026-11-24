#!/usr/bin/env python3
"""Measure a part from a reference photo.

1. Perspective-correct a quadrilateral region (4 corners, clockwise from top-left)
   into a rectangle of the given real-world aspect (or of the quad's own aspect).
2. Detect contours (edges -> closed shapes) inside the rectified region.
3. Report each contour's bounding box relative to the region width
   (and in millimetres if --width-mm is given), plus an annotated image.

Example (vent panel whose real width you know or estimate):
    python photo_measure.py refs/R4.jpg --quad 205 118 750 118 752 212 203 210 \
        --width-mm 520 --out renders/vents_measure

Tips:
- Use a straight-on photo; the more perpendicular, the better.
- Tune --canny and --min-area until the parts you care about are found;
  check the annotated image, never trust numbers you haven't looked at.
"""
import argparse
import json

import cv2
import numpy as np


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("image")
    p.add_argument("--quad", nargs=8, type=float, required=True,
                   metavar=("X1", "Y1", "X2", "Y2", "X3", "Y3", "X4", "Y4"),
                   help="corners: top-left, top-right, bottom-right, bottom-left")
    p.add_argument("--out-width", type=int, default=1600, help="rectified width in pixels")
    p.add_argument("--aspect", type=float, help="real width/height of the region (default: from quad)")
    p.add_argument("--width-mm", type=float, help="real width of the region in mm (enables mm output)")
    p.add_argument("--canny", nargs=2, type=int, default=[50, 150])
    p.add_argument("--min-area", type=float, default=0.0005, help="min contour area as fraction of region")
    p.add_argument("--out", required=True, help="output prefix")
    a = p.parse_args()

    img = cv2.imread(a.image)
    if img is None:
        raise SystemExit(f"cannot read {a.image}")
    src = np.array(a.quad, dtype=np.float32).reshape(4, 2)

    if a.aspect:
        aspect = a.aspect
    else:
        w_top = np.linalg.norm(src[1] - src[0]); w_bot = np.linalg.norm(src[2] - src[3])
        h_l = np.linalg.norm(src[3] - src[0]); h_r = np.linalg.norm(src[2] - src[1])
        aspect = float(((w_top + w_bot) / 2) / ((h_l + h_r) / 2))
    W = a.out_width
    H = int(round(W / aspect))
    dst = np.array([[0, 0], [W - 1, 0], [W - 1, H - 1], [0, H - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(src, dst)
    rect = cv2.warpPerspective(img, M, (W, H))
    cv2.imwrite(f"{a.out}_rectified.png", rect)

    gray = cv2.GaussianBlur(cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    edges = cv2.Canny(gray, *a.canny)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    mm_per_px = float(a.width_mm / W) if a.width_mm else None
    min_area = a.min_area * W * H
    items = []
    annotated = rect.copy()
    kept_boxes = []

    def near_duplicate(b):
        # the same edge often yields an inner and an outer contour; keep one
        for k in kept_boxes:
            if all(abs(b[i] - k[i]) <= max(6, 0.03 * W) for i in range(4)):
                return True
        return False

    for c in sorted(contours, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(c) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(c)
        if near_duplicate((x, y, w, h)):
            continue
        kept_boxes.append((x, y, w, h))
        idx = len(items)
        item = {
            "id": idx,
            "x_rel": round(x / W, 4), "y_rel": round(y / W, 4),
            "w_rel": round(w / W, 4), "h_rel": round(h / W, 4),
            "area_rel": round(cv2.contourArea(c) / (W * H), 5),
        }
        if mm_per_px:
            item.update({k: round(v * mm_per_px, 1) for k, v in
                         {"x_mm": x, "y_mm": y, "w_mm": w, "h_mm": h}.items()})
        items.append(item)
        cv2.drawContours(annotated, [c], -1, (0, 255, 255), 2)
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 128, 255), 1)
        cv2.putText(annotated, str(idx), (x + 3, y + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imwrite(f"{a.out}_annotated.png", annotated)
    report = {"image": a.image, "region_px": [W, H], "aspect": round(aspect, 4),
              "mm_per_px": mm_per_px, "contours": items}
    with open(f"{a.out}.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"{len(items)} contours -> {a.out}.json, {a.out}_annotated.png, {a.out}_rectified.png")
    print("Relative values are fractions of the region WIDTH (both x/w and y/h).")


if __name__ == "__main__":
    main()
