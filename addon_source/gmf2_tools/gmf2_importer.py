import bpy
import struct
import random
from collections import namedtuple
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .gmf2 import Gmf2
from .mesh_creator import GM2MeshCreator

Vec3 = namedtuple("Vec3", "x y z")
Gm2Idx = namedtuple("Gm2Idx", "i u v")


def import_models(self, context, filepath):
    gm2: Gmf2 = Gmf2.from_file(filepath)

    objects = {}
    for i, world_object in enumerate(gm2.world_objects):
        objects[world_object.off] = world_object

    for i, key in enumerate(objects):
        world_object = objects[key]

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

        if world_object.surfaces == None:
            print("No geometry.")
            continue

        rng_key = random.randint(1, 65535)
        GM2MeshCreator.create_mesh(self, context, f'{key}_{world_object.name}_{rng_key}')

        last_index = 0
        for ii, surf in enumerate(world_object.surfaces):
            strips = get_strips(surf, world_object)
            verts = []
            indices = []
            uvs = []

            if ii == 0:
                temp_vertices = []
                for v in surf.v_buf:
                    temp_vertices.append(Vec3(v.x, v.y, v.z))

                for v in temp_vertices:
                    if gm2.nmh2_identifier == 4294967295:
                        x = (v.x / scale_x + origin_x) * 0.1,
                        y = (v.y / scale_y + origin_y) * 0.1,
                        z = (v.z / scale_z + origin_z) * 0.1,
                    else:
                        x = (v.x / pow(2, world_object.v_divisor) * scale_x + origin_x) * 0.1,
                        y = (v.y / pow(2, world_object.v_divisor) * scale_y + origin_y) * 0.1,
                        z = (v.z / pow(2, world_object.v_divisor) * scale_z + origin_z) * 0.1,

                    verts.append(tuple((x, y, z)))

            if strips == []:
                continue

            for idxs in strips:
                for iii in range(len(idxs)):
                    u = idxs[iii].u / pow(2, 10)
                    v = idxs[iii].v / pow(2, 10)

                    uvs.append(tuple((u, v)))

                for iii in range(len(idxs) - 2):
                    va = idxs[iii].i + 1
                    vb = idxs[iii + 1].i + 1
                    vc = idxs[iii + 2].i + 1

                    indices.append(tuple((va, vb, vc)))

                last_index += len(idxs)

            GM2MeshCreator.create_mesh_surface(self, context, f'{key}_{world_object.name}_{rng_key}',
                                             GM2MeshCreator.SurfData(verts, indices, uvs))

            #processed_models[key] = tuple((world_object.name, verts, indices, uvs))


def get_strips(surf, obj) -> list:
    surfbuf = surf.data.data
    strips = []

    head = 0
    i_remaining = surf.data.num_v_smthn_total

    while i_remaining > 0:
        command = struct.unpack('>H', surfbuf[head:head + 2])[0]
        num_idx = struct.unpack('>H', surfbuf[head + 2:head + 4])[0]
        head += 4

        indices = []
        match command:
            case 0x99:
                for _ in range(num_idx):
                    if obj.data_c != None:
                        ibuf = surfbuf[head:head + 11]
                        head += 11

                        idx = struct.unpack('>H', ibuf[0:2])[0]
                        _normal = ibuf[2:5]
                        _color = ibuf[5:7]
                        u = struct.unpack('>h', ibuf[7:9])[0]
                        v = struct.unpack('>h', ibuf[9:11])[0]
                        indices.append(Gm2Idx(idx, u, v))
                    else:
                        if surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 153\
                                or (surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 0
                                    and num_idx == surf.data.num_v_smthn_total):
                            ibuf = surfbuf[head+2:head+11]
                            head += 11
                        else:
                            ibuf = surfbuf[head:head + 9]
                            head += 9

                        idx = struct.unpack('>H', ibuf[0:2])[0]
                        u = struct.unpack('>h', ibuf[5:7])[0]
                        v = struct.unpack('>h', ibuf[7:9])[0]

                        indices.append(Gm2Idx(idx, u, v))

            case _:
                print(f"ERR: unk_0 == {hex(command)}")
                #return []

        if len(indices) <= 0:
            return []

        new_indices = []
        for i in range(num_idx - 2):
            if indices[i] != indices[i + 1] and indices[i] != indices[i + 2] and indices[i + 1] != indices[i + 2]:
                if i % 2 == 0:
                    new_indices.append(indices[i])
                    new_indices.append(indices[i + 1])
                    new_indices.append(indices[i + 2])
                else:
                    new_indices.append(indices[i])
                    new_indices.append(indices[i + 2])
                    new_indices.append(indices[i + 1])

        strips.append(new_indices)
        i_remaining -= num_idx

    return strips


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
        ret_str += f"{'    ' * depth}{key.ljust(7)} {node.name.ljust(10)}"

        ret_str += "["
        ret_str += "G" if node.surfaces != None else "-"  # Has geometry
        ret_str += "C" if node.data_c != None else "-"  # Has data_c
        ret_str += "]"

        ret_str += "\n"
        ret_str += get_nodetree_str(children[key], nodes, depth + 1)
    return ret_str


def log_tree(log_path: str):
    in_path = ""
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


class GM2ModelImporter(Operator, ImportHelper):
    """Import mesh data from a GMF2 file"""
    bl_idname = "gm2_importer.model_data"
    bl_label = "Import GMF2 model"

    def execute(self, context):
        import_models(self, context, self.filepath)

        return {'FINISHED'}
