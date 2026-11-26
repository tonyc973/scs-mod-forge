"""Original stylised sedan, modelled procedurally and rendered with Cycles.

Run with Blender (or the bpy module):
    blender -b -P car.py -- 36 frames
    python compose.py   # builds ../../banner.gif
"""
import bpy, bmesh, math, sys
from mathutils import Vector

FRAMES = int(sys.argv[-2]) if len(sys.argv) > 2 and sys.argv[-2].isdigit() else 1
OUT = sys.argv[-1]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def lerp_profile(pts, x):
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0) if x1 != x0 else 0
            return z0 + t * (z1 - z0)
    return pts[0][1] if x < pts[0][0] else pts[-1][1]

L0, L1 = -2.32, 2.32
# lower body: top line (beltline/hood/deck) and bottom
belt = [(-2.32, 0.60), (-2.20, 0.74), (-1.70, 0.84), (-0.95, 0.94), (0.0, 0.97), (1.6, 1.00), (2.15, 0.98), (2.32, 0.82)]
bottom = [(-2.32, 0.34), (-2.0, 0.24), (2.0, 0.24), (2.32, 0.34)]
# greenhouse: windshield base to roof to deck
gh_x0, gh_x1 = -1.0, 1.75
roof = [(-1.0, 0.94), (-0.25, 1.40), (0.85, 1.41), (1.75, 1.0)]

def superellipse_ring(xc, zb, zt, half_w, n=26, p=4.0, flat_top=False):
    pts = []
    zc, hz = (zb + zt) / 2, (zt - zb) / 2
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        y = half_w * math.copysign(abs(c) ** (2 / p), c)
        z = zc + hz * math.copysign(abs(s) ** (2 / p), s)
        pts.append(Vector((xc, y, z)))
    return pts

def loft(name, stations, ring_fn):
    bm = bmesh.new()
    rings = []
    for x in stations:
        rings.append([bm.verts.new(v) for v in ring_fn(x)])
    n = len(rings[0])
    for r0, r1 in zip(rings, rings[1:]):
        for i in range(n):
            bm.faces.new((r0[i], r0[(i + 1) % n], r1[(i + 1) % n], r1[i]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    return ob

def ease_w(x, full, span=(L0, L1), taper=0.35):
    # narrower at the very ends
    d = min(x - span[0], span[1] - x)
    k = min(1.0, max(0.0, d / taper))
    return full * (0.78 + 0.22 * math.sin(k * math.pi / 2))

N = 48
xs = [L0 + (L1 - L0) * (i / (N - 1)) for i in range(N)]
body = loft("Body", xs, lambda x: superellipse_ring(x, lerp_profile(bottom, x), lerp_profile(belt, x), ease_w(x, 0.90), p=5.0))
gxs = [gh_x0 + (gh_x1 - gh_x0) * (i / 31) for i in range(32)]
def gh_ring(x):
    zt = lerp_profile(roof, x); zb = lerp_profile(belt, x) - 0.06
    zt = max(zt, zb + 0.02)
    return superellipse_ring(x, zb, zt, ease_w(x, 0.70, (gh_x0, gh_x1), 0.5), p=3.2)
cabin = loft("Cabin", gxs, gh_ring)

for ob, lv in ((body, 2), (cabin, 2)):
    m = ob.modifiers.new("sub", "SUBSURF"); m.levels = lv; m.render_levels = lv

# wheel arches (boolean) + wheels
WX, WY, WR, WW = (-1.38, 1.36), 0.80, 0.335, 0.24
bpy.context.view_layer.objects.active = body
for wx in WX:
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=WR + 0.05, depth=2.2, location=(wx, 0, WR + 0.02), rotation=(math.pi / 2, 0, 0))
    cut = bpy.context.active_object; cut.display_type = "WIRE"; cut.hide_render = True
    b = body.modifiers.new("arch", "BOOLEAN"); b.object = cut; b.operation = "DIFFERENCE"; b.solver = "EXACT"

def mat(name, color, metal=0.0, rough=0.4, emit=None, emit_str=0, coat=0.0, alpha=1.0, trans=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    if "Coat Weight" in p.inputs: p.inputs["Coat Weight"].default_value = coat
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1); p.inputs["Emission Strength"].default_value = emit_str
    return m

paint = mat("Paint", (0.86, 0.87, 0.89), rough=0.25, coat=1.0)
glass = mat("Glass", (0.015, 0.02, 0.03), rough=0.05, coat=1.0)
tyre = mat("Tyre", (0.02, 0.02, 0.02), rough=0.85)
rim = mat("Rim", (0.75, 0.76, 0.78), metal=1.0, rough=0.22)
rimdark = mat("RimDark", (0.06, 0.06, 0.07), metal=0.6, rough=0.4)
head = mat("Head", (1, 1, 1), emit=(0.85, 0.92, 1.0), emit_str=18)
tail = mat("Tail", (0.6, 0.02, 0.02), emit=(1.0, 0.05, 0.03), emit_str=14)
trim = mat("Trim", (0.03, 0.03, 0.035), rough=0.5)
body.data.materials.append(paint)
cabin.data.materials.append(glass); cabin.data.materials.append(paint)
# roof panel in paint
for p in cabin.data.polygons:
    c = p.center
    if c.z > lerp_profile(roof, c.x) - 0.06 and abs(c.y) < 0.5 and -0.35 < c.x < 1.2:
        p.material_index = 1

for wx in WX:
    for wy in (-WY, WY):
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=WR, depth=WW, location=(wx, wy, WR), rotation=(math.pi / 2, 0, 0))
        t = bpy.context.active_object; t.data.materials.append(tyre)
        bv = t.modifiers.new("bv", "BEVEL"); bv.width = 0.06; bv.segments = 6
        for p in t.data.polygons: p.use_smooth = True
        side = 1 if wy > 0 else -1
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=WR * 0.66, depth=0.04,
            location=(wx, wy + side * (WW / 2 + 0.01), WR), rotation=(math.pi / 2, 0, 0))
        d = bpy.context.active_object; d.data.materials.append(rimdark)
        for k in range(5):  # twin spokes
            for off in (-0.09, 0.09):
                ang = k * 2 * math.pi / 5 + off
                bpy.ops.mesh.primitive_cube_add(size=1, location=(wx + math.cos(ang) * WR * 0.36, wy + side * (WW / 2 + 0.03), WR + math.sin(ang) * WR * 0.36))
                s = bpy.context.active_object
                s.scale = (WR * 0.66, 0.03, 0.05); s.rotation_euler = (0, -ang, 0)
                s.data.materials.append(rim)
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.055, depth=0.05, location=(wx, wy + side * (WW / 2 + 0.045), WR), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(rim)

def bar(name, loc, size, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.active_object
    o.scale = size; o.data.materials.append(m); o.name = name
    bv = o.modifiers.new("bv", "BEVEL"); bv.width = 0.01; bv.segments = 3
    return o
for s_ in (-1, 1):
    bar("HL", (-2.175, s_ * 0.56, 0.695), (0.14, 0.40, 0.04), head)
    bar("TL", (2.27, s_ * 0.55, 0.88), (0.06, 0.5, 0.05), tail)
bar("TLc", (2.29, 0, 0.88), (0.04, 0.6, 0.02), tail)
# grille removed (caused reflection artifacts)
bar("Sill", (0, 0, 0.27), (3.0, 1.74, 0.05), trim)

# ground
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0))
g = bpy.context.active_object
gm = mat("Ground", (0.02, 0.025, 0.035), rough=0.28); g.data.materials.append(gm)

# parent everything car-related to an empty for turntable
root = bpy.data.objects.new("Root", None); sc.collection.objects.link(root)
for o in list(sc.objects):
    if o not in (g, root) and o.type in ("MESH",):
        o.parent = root

# world
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.016, 0.024, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def area(loc, rot, size, energy, color):
    l = bpy.data.lights.new("A", "AREA"); l.size = size; l.energy = energy; l.color = color
    o = bpy.data.objects.new("A", l); o.location = loc; o.rotation_euler = rot; sc.collection.objects.link(o)
area((0, 0, 6), (0, 0, 0), 6, 900, (1, 1, 1))
area((-5, -4, 2.5), (math.radians(70), 0, math.radians(-50)), 3, 900, (0.39, 0.4, 0.95))   # indigo rim
area((5, 4, 2.5), (math.radians(70), 0, math.radians(130)), 3, 900, (0.88, 0.54, 0.12))   # amber rim
area((-6, 3, 1.5), (math.radians(80), 0, math.radians(-120)), 4, 400, (0.05, 0.62, 0.56))  # teal kick

cam_d = bpy.data.cameras.new("C"); cam_d.lens = 50
cam = bpy.data.objects.new("C", cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (-6.4, -5.6, 2.1)
dirv = Vector((0.05, 0, 0.45)) - cam.location
cam.rotation_euler = dirv.to_track_quat("-Z", "Y").to_euler()

sc.render.engine = "CYCLES"
sc.cycles.samples = 32
sc.cycles.use_denoising = True
sc.cycles.device = "CPU"
sc.render.resolution_x, sc.render.resolution_y = 780, 440
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in sc.view_settings.bl_rna.properties["view_transform"].enum_items] else "Filmic"
sc.view_settings.look = "None"

for f in range(FRAMES):
    root.rotation_euler = (0, 0, 2 * math.pi * f / FRAMES)
    sc.render.filepath = f"{OUT}/f{f:03d}.png"
    bpy.ops.render.render(write_still=True)
print("done")
