"""Mesh audit for Blender (run in Blender's Python console / text editor, or via MCP).

Reports, per selected mesh object (or all meshes if nothing is selected):
  - boundary edges (open borders: fine for some trims, fatal for closed parts)
  - non-manifold edges (shared by 3+ faces)
  - inconsistent normals (adjacent faces with opposite winding)
  - concave n-gons (5+ verts, non-convex -> risky triangulation at export: "sawtooth" edges)
  - zero-area faces
  - loose vertices
  - near-duplicate vertices (within MERGE_DIST)

Writes a Markdown report next to the .blend (mesh_audit.md) and prints a summary.
Does not modify the mesh.
"""
import os

import bmesh
import bpy
from mathutils import kdtree

MERGE_DIST = 0.0001  # metres
AREA_EPS = 1e-10


def face_is_concave(f):
    if len(f.verts) < 5:
        return False
    n = f.normal
    if n.length < 1e-9:
        return False
    vs = [v.co for v in f.verts]
    sign = 0
    for i in range(len(vs)):
        a, b, c = vs[i - 1], vs[i], vs[(i + 1) % len(vs)]
        cross = (b - a).cross(c - b).dot(n)
        if abs(cross) < 1e-12:
            continue
        s = 1 if cross > 0 else -1
        if sign == 0:
            sign = s
        elif s != sign:
            return True
    return False


def audit(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.normal_update()
    r = {"boundary": 0, "non_manifold": 0, "flipped": 0, "concave_ngons": 0,
         "zero_area": 0, "loose_verts": 0, "near_dupes": 0}
    for e in bm.edges:
        n = len(e.link_faces)
        if n == 1:
            r["boundary"] += 1
        elif n > 2:
            r["non_manifold"] += 1
        elif n == 2:
            l0, l1 = e.link_loops[0], e.link_loops[1]
            if l0.vert == l1.vert:  # same direction -> inconsistent winding
                r["flipped"] += 1
    for f in bm.faces:
        if f.calc_area() < AREA_EPS:
            r["zero_area"] += 1
        if face_is_concave(f):
            r["concave_ngons"] += 1
    r["loose_verts"] = sum(1 for v in bm.verts if not v.link_edges)
    kd = kdtree.KDTree(len(bm.verts))
    for i, v in enumerate(bm.verts):
        kd.insert(v.co, i)
    kd.balance()
    seen = set()
    for i, v in enumerate(bm.verts):
        for (_, j, _) in kd.find_range(v.co, MERGE_DIST):
            if j != i and (j, i) not in seen:
                seen.add((i, j))
    r["near_dupes"] = len(seen)
    bm.free()
    return r


def main():
    objs = [o for o in bpy.context.selected_objects if o.type == "MESH"] or \
           [o for o in bpy.data.objects if o.type == "MESH"]
    lines = ["# Mesh audit", "",
             "| object | boundary | non-manifold | flipped | concave n-gons | zero-area | loose verts | near-dupes |",
             "|---|---|---|---|---|---|---|---|"]
    problems = 0
    for o in objs:
        r = audit(o)
        bad = r["non_manifold"] + r["flipped"] + r["concave_ngons"] + r["zero_area"] + r["loose_verts"] + r["near_dupes"]
        problems += bool(bad)
        lines.append(f"| {o.name} | {r['boundary']} | {r['non_manifold']} | {r['flipped']} | {r['concave_ngons']} | "
                     f"{r['zero_area']} | {r['loose_verts']} | {r['near_dupes']} |")
    lines += ["", f"{problems} of {len(objs)} objects have issues (boundary edges are reported but not counted)."]
    text = "\n".join(lines)
    print(text)
    if bpy.data.filepath:
        path = os.path.join(os.path.dirname(bpy.data.filepath), "mesh_audit.md")
        with open(path, "w") as f:
            f.write(text + "\n")
        print(f"report written to {path}")


main()
