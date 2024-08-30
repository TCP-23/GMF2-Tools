from collections import namedtuple
import os
from pathlib import Path
import struct
import sys
from lib.kaitai_defs.gmf2 import Gmf2
from glob import glob

import unpack_gct0

TOOL_NAME = "Jyl's GMF2 exporter"

DIR = "filesystem/DATA/files/STG_HI"
OUT_DIR = "out/STG_HI"

Vec3 = namedtuple("Vec3", "x y z")

Gm2Idx = namedtuple("Gm2Idx", "i u v")

def extract_models(in_path: str, out_dir: str):
    print(f"\nExtracting objects:")
    gm2: Gmf2 = Gmf2.from_file(in_path)

    # Meshes

    # Create a dic containing each object, key is its offset.
    objects = {}
    for i, world_object in enumerate(gm2.world_objects):
        objects[world_object.off] = world_object

    print(f"{"off".ljust(8)}", end="")
    print(f"{"name".ljust(10)}", end="")
    print("surface progress", end="")
    print(" ")
    for i, key in enumerate(objects):
        print(f"{hex(world_object.off).ljust(8)}", end="")
        print(f"{world_object.name.ljust(10)}", end="")
        print(f"{hex(world_object.off_prev).ljust(12)}", end="")

        world_object = objects[key]

        # Go through every parent and sum their positions
        origin_x = 0
        origin_y = 0
        origin_z = 0
        scale_x = 1
        scale_y = 1
        scale_z = 1
        object = world_object
        while object != None:
            origin_x += object.origin.x
            origin_y += object.origin.y
            origin_z += object.origin.z
            scale_x *= object.scale.x
            scale_y *= object.scale.y
            scale_z *= object.scale.z
            object = objects.get(object.off_parent)

        out_path = os.path.join(
            out_dir, f"{world_object.name}_{i}.obj"
        )

        with open(out_path, "w") as f:
            f.write("# OBJ file\n")
            f.write(f"# Generated by {TOOL_NAME}\n")

            if world_object.surfaces == None:
                f.write(f"# Skipped empty object:\n#o {world_object.name}_{i}\n")
                print("No geometry.")
                continue

            f.write(f"o {Path(in_path).stem}_{i}_{world_object.name}\n")

            last_index = 0
            for ii, surf in enumerate(world_object.surfaces):
                f.write(f"usemtl {hex(surf.off_material)}\n")
                print(f"{ii}..", end="")

                if gm2.nmh2_identifier == 4294967295:
                    strips = get_strips(surf, world_object, True)
                else:
                    strips = get_strips(surf, world_object, False)

                # Write Vs (once)
                if ii == 0:
                    vertices = []
                    for v in surf.v_buf:
                        vertices.append(Vec3(v.x, v.y, v.z))

                    for v in vertices:
                        if gm2.nmh2_identifier == 4294967295:
                            x = (v.x / scale_x + origin_x) * 0.1,
                            y = (v.y / scale_y + origin_y) * 0.1,
                            z = (v.z / scale_z + origin_z) * 0.1,
                        else:
                            x = (v.x / pow(2, world_object.v_divisor) * scale_x + origin_x) * 0.1,
                            y = (v.y / pow(2, world_object.v_divisor) * scale_y + origin_y) * 0.1,
                            z = (v.z / pow(2, world_object.v_divisor) * scale_z + origin_z) * 0.1,

                        f.write(f"v {x[0]} {y[0]} {z[0]}\n")

                # Exit if something went wrong.
                if strips == []:
                    continue

                # Write UVs
                for indices in strips:
                    for i in range(len(indices)):
                        u = indices[i].u / pow(2, 10)
                        v = indices[i].v / pow(2, 10)
                        f.write(f"vt {u} {v}\n")

                # Write strips

                for indices in strips:
                    for i in range(len(indices)-2):
                        va = indices[i].i + 1
                        vb = indices[i+1].i + 1
                        vc = indices[i+2].i + 1
                        vta = last_index + i + 1
                        vtb = last_index + i + 1 + 1
                        vtc = last_index + i + 1 + 2
                        #if gm2.nmh2_identifier == 4294967295:
                            #f.write(f"f {vta}/{va} {vtb}/{vb} {vtc}/{vc}\n")
                        #else:
                            #f.write(f"f {va}/{vta} {vb}/{vtb} {vc}/{vtc}\n")

                        f.write(f"f {va}/{vta} {vb}/{vtb} {vc}/{vtc}\n")

                    last_index += len(indices)

            print("Done")


def get_strips(surf, obj, is_nmh2=False) -> list:
    # Indices
    surfbuf = surf.data.data
    strips = []

    head = 0
    i_remaining = surf.data.num_v_smthn_total

    while i_remaining > 0:
        command = struct.unpack('>H', surfbuf[head:head+2])[0]
        num_idx = struct.unpack('>H', surfbuf[head+2:head+4])[0]
        head += 4

        #print("Head: ", (head - 4))
        #print("Command: ", command)
        #print("Num_index: ", num_idx)
        #print("i_remaining_1: ", i_remaining)
        #print("i_remaining_2: ", i_remaining - num_idx)

        indices = []
        match command:
            case 0x99:
                for _ in range(num_idx):
                    if (obj.data_c != None):
                        ibuf = surfbuf[head:head + 11]
                        head += 11

                        idx = struct.unpack('>H', ibuf[0:2])[0]
                        _normal = ibuf[2:5]
                        _color = ibuf[5:7]
                        u = struct.unpack('>h', ibuf[7:9])[0]
                        v = struct.unpack('>h', ibuf[9:11])[0]
                        indices.append(Gm2Idx(idx, u, v))
                    else:

                        # Vertex format isn't defined, use default.
                        # 9B: iinnnuuuu

                        if surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 153:
                            ibuf = surfbuf[head+2:head+11]
                            head += 11
                        else:
                            ibuf = surfbuf[head:head + 9]
                            head += 9

                        # print("idx: ", ibuf[0:2])
                        # print("u: ", ibuf[5:7])
                        # print("v: ", ibuf[7:9])

                        idx = struct.unpack('>H', ibuf[0:2])[0]
                        # print("idx: ", idx)

                        # skip 3B normal

                        u = struct.unpack('>h', ibuf[5:7])[0]
                        v = struct.unpack('>h', ibuf[7:9])[0]

                        # print("u: ", u)
                        # print("v: ", v)

                        indices.append(Gm2Idx(idx, u, v))

            case _:
                print(f"ERR: unk_0 == {hex(command)}")
                #return []


        if len(indices) <= 0:
            return []

        new_indices = []
        for i in range(num_idx-2):
            if i % 2 == 0:
                new_indices.append(indices[i])
                new_indices.append(indices[i+1])
                new_indices.append(indices[i+2])
            else:
                new_indices.append(indices[i])
                new_indices.append(indices[i+2])
                new_indices.append(indices[i+1])
        strips.append(new_indices)
        i_remaining -= num_idx

    return strips


def extract_textures(in_path: str, out_dir: str):
    gm2: Gmf2 = Gmf2.from_file(in_path)
    print(f"\nExtracting {gm2.num_textures} textures...")

    for i, texture in enumerate(gm2.textures):

        filename = f"{texture.name}_{i}.GCT"
        print(f"{i}/{gm2.num_textures-1} {filename}")

        out_path = os.path.join(out_dir, filename)
        with open(out_path, "wb") as f:
            f.write(texture.data)

        unpack_gct0.unpack(out_path, out_dir)


def extract_armature(in_path: str, out_dir: str):
    print("Extracting armature...")
    gm2: Gmf2 = Gmf2.from_file(in_path)

    for i, world_objects in enumerate(gm2.world_objects):
        pass

    bones = {}


def get_nodetree(node_id: str, nodes: list):
    """Recursively get node tree"""
    children = {}
    for node in nodes:
        parent = hex(node.off_parent)
        if parent == node_id:
            child = hex(node.off)
            children[child] = get_nodetree(child, nodes)
    return children


def get_nodetree_str(children: dict, nodes: dict, depth: int = 1):
    """Recursively generate string from nodetree."""
    ret_str = ""
    keys = children.keys()
    for key in keys:
        node = nodes[key]
        ret_str += f"{"    " * depth}{key.ljust(7)} {node.name.ljust(10)}"

        ret_str +="["
        ret_str += "G" if node.surfaces != None else "-"    # Has geometry
        ret_str += "C" if node.data_c != None else "-"      # Has data_c
        ret_str +="]"

        ret_str += "\n"
        ret_str += get_nodetree_str(children[key], nodes, depth + 1)
    return ret_str


def log_tree(in_path: str, log_path: str):
    gm2: Gmf2 = Gmf2.from_file(in_path)
    with open(log_path, "w") as f:
        f.write(f"GMF2 info:\n{Path(in_path).stem}\n\n--- Scene Tree ---\n")

        nodes = {}
        for node in gm2.world_objects:
            key = hex(node.off)
            nodes[key] = node

        tree = get_nodetree(hex(0), gm2.world_objects)
        tree_str = get_nodetree_str(tree, nodes)

        print(tree_str)
        f.write(tree_str)


def log_textures(in_path: str, log_path: str):
    with open(log_path, "a") as f:
        f.write("\n--- Textures ---\n")

        f.write(f"{"Filename".ljust(20)}")
        f.write(f"{"Encoding".ljust(16)}")
        f.write(f"{"Size".ljust(8)}")
        f.write("\n")

        files = os.listdir(in_path)
        files.sort()
        for file in files:
            if not file.endswith(".GCT"):
                continue


            path = os.path.join(in_path, file)
            print("TEXTURE: ", path)

            gct0 = unpack_gct0.parse_file(path)

            f.write(f"{file.ljust(20)}")
            enc_str = f"{hex(gct0.encoding)} - {unpack_gct0.Encoding(gct0.encoding).name}"
            f.write(f"{enc_str.ljust(16)}")
            f.write(f"{str(gct0.w)}x{str(gct0.h)}".ljust(8))
            f.write("\n")



def unpack(path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "_info.txt")

    log_tree(path, log_path)
    extract_textures(path, out_dir)
    log_textures(out_dir, log_path)
    extract_models(path, out_dir)
    extract_armature(path, out_dir)


if __name__ == "__main__":
    match len(sys.argv):
        case 2:
            in_path = sys.argv[1]
            out_path = os.path.join(".", Path(in_path).stem + "_extracted")
            unpack(in_path, out_path)

        case 3:
            in_path = sys.argv[1]
            out_path = sys.argv[2]
            unpack(in_path, out_path)

        case _:
            print("Provide 1 or 2 args:\n    - input file path\n    - output dir path (optional)")

