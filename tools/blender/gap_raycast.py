"""Measure the gap between two surfaces along an edge (e.g. dashboard front edge -> windshield).

Setup:
  - SOURCE: object whose edge you want to check (e.g. the dashboard).
    Put the edge vertices in a vertex group named GROUP (e.g. "gap_edge").
  - TARGET: the surface to measure against (e.g. the windshield).
Edit the constants below, run in Blender. Edges between grouped vertices are sampled every STEP metres.

Output: max / mean / per-sample distances (printed and written to //gap_report.csv).
Target for a dash/windshield junction: max <= 3 mm.
"""
import csv
import os

import bpy

SOURCE = "Dashboard"
TARGET = "Windshield"
GROUP = "gap_edge"
STEP = 0.02  # metres


def main():
    src = bpy.data.objects[SOURCE]
    tgt = bpy.data.objects[TARGET]
    gi = src.vertex_groups[GROUP].index
    me = src.data
    in_group = {v.index for v in me.vertices if any(g.group == gi for g in v.groups)}
    if not in_group:
        raise SystemExit(f"vertex group {GROUP!r} on {SOURCE!r} is empty")
    mw_s, tgt_inv = src.matrix_world, tgt.matrix_world.inverted()
    samples = []
    for e in me.edges:
        a, b = e.vertices
        if a in in_group and b in in_group:
            pa, pb = mw_s @ me.vertices[a].co, mw_s @ me.vertices[b].co
            n = max(1, int((pb - pa).length / STEP))
            samples += [pa.lerp(pb, k / n) for k in range(n + 1)]
    if not samples:  # group without edges: use the vertices themselves
        samples = [mw_s @ me.vertices[i].co for i in in_group]
    rows = []
    for p in samples:
        ok, loc, _nrm, _idx = tgt.closest_point_on_mesh(tgt_inv @ p)
        if ok:
            d = (tgt.matrix_world @ loc - p).length
            rows.append((p.x, p.y, p.z, d))
    ds = [r[3] for r in rows]
    print(f"{len(ds)} samples | max {max(ds)*1000:.1f} mm | mean {sum(ds)/len(ds)*1000:.1f} mm")
    worst = sorted(rows, key=lambda r: -r[3])[:5]
    for x, y, z, d in worst:
        print(f"  worst: {d*1000:.1f} mm at ({x:.3f}, {y:.3f}, {z:.3f})")
    if bpy.data.filepath:
        path = os.path.join(os.path.dirname(bpy.data.filepath), "gap_report.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["x", "y", "z", "gap_m"])
            w.writerows(rows)
        print(f"written {path}")


main()
