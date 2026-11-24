"""Colour-tag diagnostics (run on a COPY of your .blend, export as a separate *_diag mod).

For each selected object:
  - generates a 4x4 PNG of a unique flat colour in //diag_textures/
  - duplicates each of the object's materials as DIAG_<n>_<name> and assigns the copies
  - tries to point the SCS base texture of the copy to the colour PNG
    (SCS Blender Tools property `scs_props.shader_texture_base`; if your version
    names it differently, the script tells you and you set the texture by hand)
  - for plain Blender preview, also wires the colour into the node tree (emission)

Writes //diag_colors.md with colour -> object -> original materials.

Use it, screenshot the standard views in game, read the colours, then throw the copy away.
Anything that does NOT change colour in game is not coming from the tagged objects.
"""
import os
import struct
import zlib

import bpy

PALETTE = [
    ("red", (1, 0, 0)), ("green", (0, 1, 0)), ("blue", (0, 0, 1)), ("yellow", (1, 1, 0)),
    ("magenta", (1, 0, 1)), ("cyan", (0, 1, 1)), ("orange", (1, 0.5, 0)), ("white", (1, 1, 1)),
    ("purple", (0.5, 0, 1)), ("lime", (0.5, 1, 0)), ("pink", (1, 0.4, 0.7)), ("teal", (0, 0.5, 0.5)),
]


def write_png(path, rgb, size=4):
    r, g, b = (int(c * 255) for c in rgb)
    raw = b"".join(b"\x00" + bytes([r, g, b]) * size for _ in range(size))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def preview_nodes(mat, rgb):
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = (*rgb, 1)
    nt.links.new(em.outputs[0], out.inputs[0])


def main():
    if not bpy.data.filepath:
        raise SystemExit("Save the COPY of your .blend first (paths are relative to it).")
    base = os.path.dirname(bpy.data.filepath)
    tex_dir = os.path.join(base, "diag_textures")
    os.makedirs(tex_dir, exist_ok=True)
    objs = [o for o in bpy.context.selected_objects if o.type == "MESH"]
    if not objs:
        raise SystemExit("Select the suspect mesh objects first.")
    if len(objs) > len(PALETTE):
        print(f"Only {len(PALETTE)} colours: tagging the first {len(PALETTE)} objects; run again for the rest.")
    rows, scs_ok = [], True
    for i, (obj, (cname, rgb)) in enumerate(zip(objs, PALETTE)):
        png = os.path.join(tex_dir, f"diag_{cname}.png")
        write_png(png, rgb)
        originals = []
        for slot in obj.material_slots:
            src = slot.material
            originals.append(src.name if src else "<empty>")
            new = src.copy() if src else bpy.data.materials.new("DIAG")
            new.name = f"DIAG_{i}_{cname}_{originals[-1]}"
            preview_nodes(new, rgb)
            try:
                new.scs_props.shader_texture_base = "//" + os.path.relpath(png, base).replace(os.sep, "/")
            except AttributeError:
                scs_ok = False
            slot.material = new
        if not obj.material_slots:
            new = bpy.data.materials.new(f"DIAG_{i}_{cname}")
            preview_nodes(new, rgb)
            obj.data.materials.append(new)
        hexv = "#%02X%02X%02X" % tuple(int(c * 255) for c in rgb)
        rows.append(f"| {cname} | {hexv} | {obj.name} | {', '.join(originals) or '-'} | | |")
    md = ["# Colour-tag map", "", f"Blend: {bpy.data.filepath}", "",
          "| colour | hex | object | original materials | seen in game? | conclusion |",
          "|---|---|---|---|---|---|", *rows, "",
          "Untagged defects (did not change colour) come from elsewhere: inherited accessory, exterior model, other mods."]
    with open(os.path.join(base, "diag_colors.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))
    if not scs_ok:
        print("\n!! Could not set scs_props.shader_texture_base automatically. Set each DIAG material's base "
              "texture to the matching PNG in //diag_textures/ via the SCS material panel before export.")


main()
