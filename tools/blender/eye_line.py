"""Project a contact line from the driver's eye onto glass (e.g. to size a windshield frit band).

Setup:
  - EYE: an Empty placed at the driver's eye point (match the game's interior camera head position).
  - SOURCE: object containing the contact line (e.g. the dashboard), with the line's vertices
    in vertex group GROUP (e.g. "contact_line" = where the dash meets the glass, as seen from the eye).
  - GLASS: the windshield object.
  - MARGIN: how far above the projected line the OPAQUE part of the frit must reach (metres, along the glass).

For every contact vertex, a ray from the eye through the vertex is continued until it hits the glass.
The hit points + MARGIN (moved "up" along the glass) form the top of the opaque band.
Creates a polyline object FRIT_TOP_LINE you can use to cut/shape the frit mesh, and prints the heights.
"""
import bpy
from mathutils import Vector

EYE = "DriverEye"
SOURCE = "Dashboard"
GROUP = "contact_line"
GLASS = "Windshield"
MARGIN = 0.02
UP = Vector((0, 0, 1))  # world up; the script slides along the glass in this direction


def ray_hit(obj, origin_w, direction_w):
    inv = obj.matrix_world.inverted()
    o = inv @ origin_w
    d = (inv.to_3x3() @ direction_w).normalized()
    ok, loc, nrm, _ = obj.ray_cast(o, d)
    if not ok:
        return None, None
    return obj.matrix_world @ loc, (obj.matrix_world.to_3x3() @ nrm).normalized()


def main():
    eye = bpy.data.objects[EYE].matrix_world.translation
    src = bpy.data.objects[SOURCE]
    glass = bpy.data.objects[GLASS]
    gi = src.vertex_groups[GROUP].index
    pts = [src.matrix_world @ v.co for v in src.data.vertices if any(g.group == gi for g in v.groups)]
    if not pts:
        raise SystemExit("contact_line group is empty")
    pts.sort(key=lambda p: p.x)
    tops = []
    for p in pts:
        d = (p - eye).normalized()
        hit, nrm = ray_hit(glass, p - d * 0.001, d)  # start just before the contact point
        if hit is None:
            hit, nrm = ray_hit(glass, eye, d)
        if hit is None:
            print(f"  no glass hit behind {tuple(round(c, 3) for c in p)}")
            continue
        slide = (UP - nrm * UP.dot(nrm)).normalized()  # 'up' tangent to the glass
        top = hit + slide * MARGIN
        tops.append(top)
        print(f"  contact z={p.z:.3f} -> glass hit z={hit.z:.3f} -> opaque top z={top.z:.3f}")
    if not tops:
        raise SystemExit("no hits: check EYE position and GLASS normals")
    me = bpy.data.meshes.new("FRIT_TOP_LINE")
    me.from_pydata([tuple(t) for t in tops], [(i, i + 1) for i in range(len(tops) - 1)], [])
    ob = bpy.data.objects.new("FRIT_TOP_LINE", me)
    bpy.context.collection.objects.link(ob)
    print(f"created FRIT_TOP_LINE with {len(tops)} points")


main()
