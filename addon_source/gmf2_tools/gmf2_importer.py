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
    rng_key_dic = {}

    for i, world_object in enumerate(gm2.world_objects):
        objects[world_object.off] = world_object
        rng_key_dic[world_object.off] = random.randint(1, 65535)

    for i, key in enumerate(objects):
        world_object = objects[key]

        origin_x = world_object.origin.x * 0.1
        origin_y = world_object.origin.y * 0.1
        origin_z = world_object.origin.z * 0.1

        rot_x = world_object.unk_b
        rot_y = world_object.rot_y
        rot_z = world_object.rot_z
        rot_w = world_object.unkf_11

        scale_x = world_object.scale.x
        scale_y = world_object.scale.y
        scale_z = world_object.scale.z

        GM2MeshCreator.create_mesh(self, context, f'{key}_{world_object.name}_{rng_key_dic[key]}',
                                   tuple((origin_x, origin_y, origin_z)), tuple((rot_x, rot_y, rot_z, rot_w)))

        if world_object.surfaces == None:
            continue

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
                        #x = (v.x / scale_x + origin_x) * 0.1,
                        #y = (v.y / scale_y + origin_y) * 0.1,
                        #z = (v.z / scale_z + origin_z) * 0.1,
                        x = (v.x / scale_x) * 0.1,
                        y = (v.y / scale_y) * 0.1,
                        z = (v.z / scale_z) * 0.1,
                    else:
                        #x = (v.x / pow(2, world_object.v_divisor) * scale_x + origin_x) * 0.1,
                        #y = (v.y / pow(2, world_object.v_divisor) * scale_y + origin_y) * 0.1,
                        #z = (v.z / pow(2, world_object.v_divisor) * scale_z + origin_z) * 0.1,
                        x = (v.x / pow(2, world_object.v_divisor) * scale_x) * 0.1,
                        y = (v.y / pow(2, world_object.v_divisor) * scale_y) * 0.1,
                        z = (v.z / pow(2, world_object.v_divisor) * scale_z) * 0.1,

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

            GM2MeshCreator.create_mesh_surface(self, context, f'{key}_{world_object.name}_{rng_key_dic[key]}',
                                               GM2MeshCreator.SurfData(verts, indices, uvs))

    for i, key in enumerate(objects):
        world_object = objects[key]

        if world_object.off_parent != 0:
            parent_id = f'{world_object.off_parent}_{objects.get(world_object.off_parent).name}_{rng_key_dic[world_object.off_parent]}'
            GM2MeshCreator.set_mesh_parent(self, context, f'{key}_{world_object.name}_{rng_key_dic[key]}',
                                           parent_id)


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
                        if get_tristrip_format(surf, num_idx) == 1:
                            ibuf = surfbuf[head+2:head+11]
                            head += 11
                        else:
                            ibuf = surfbuf[head:head+9]
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


def get_tristrip_format(surface, num_idx):
    surfbuf = surface.data.data

    if surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 153 \
            or (surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 0
                and surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 4] != 0
                and num_idx == surface.data.num_v_smthn_total):
        return 1
    else:
        return 0


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
