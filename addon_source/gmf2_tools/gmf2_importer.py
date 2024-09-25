import bpy
import struct
from collections import namedtuple
from bpy.types import Operator

from .gmf2 import Gmf2
from .mesh_creator import GM2MeshCreator

Vec3 = namedtuple("Vec3", "x y z")
Gm2Idx = namedtuple("Gm2Idx", "i u v")

class GM2ModelImporter(Operator):
    """Import mesh data from a GMF2 file"""
    bl_idname = "gm2_importer.model_data"
    bl_label = "Import GMF2 model"

    idx_mode = 'OPT_A'
    fix_coord = False
    smooth_shading = False
    testing_features = False

    def set_import_variables(self, indexOverride, fixCoordinateSpace, useSmoothShading, devFeatures):
        self.idx_mode = indexOverride
        self.fix_coord = fixCoordinateSpace
        self.smooth_shading = useSmoothShading
        self.testing_features = devFeatures

    def load_model_data(self, context, filepath):
        gm2: Gmf2 = Gmf2.from_file(filepath)

        isNmh2 = False
        if gm2.nmh2_identifier == 4294967295:
            isNmh2 = True

        objects = {}

        for i, world_object in enumerate(gm2.world_objects):
            objects[world_object.off] = world_object

        #order of operations:
        #create object
        #set name

        #if we have a parent, set it
        #set our position
        #set our rotation
        #load geometry
        #load children of our object

        GM2ModelImporter.import_objects(self, context, objects, gm2.world_objects[0].off,
                                        None, isNmh2)

    def import_objects(self, context, model_data, _off, parent, isNmh2):
        next_offset = _off

        while next_offset != 0:
            obj_data = model_data[next_offset]
            new_obj = GM2MeshCreator.create_object(self, context, obj_data, parent, self.fix_coord)

            if obj_data.surfaces != None:
                last_index = 0
                for ii, surf in enumerate(obj_data.surfaces):
                    strips = GM2ModelImporter.get_strips(self, surf, obj_data, self.idx_mode)
                    verts = []
                    indices = []
                    uvs = []

                    if ii == 0:
                        temp_vertices = []
                        for v in surf.v_buf:
                            temp_vertices.append(Vec3(v.x, v.y, v.z))

                        for v in temp_vertices:
                            if isNmh2:
                                x = (v.x / 1) * 0.1
                                y = (v.y / 1) * 0.1
                                z = (v.z / 1) * 0.1
                            else:
                                x = (v.x / pow(2, obj_data.v_divisor)) * 0.1
                                y = (v.y / pow(2, obj_data.v_divisor)) * 0.1
                                z = (v.z / pow(2, obj_data.v_divisor)) * 0.1

                            verts.append(tuple((x, y, z)))

                    if strips == []:
                        continue

                    for idxs in strips:
                        for iii in range(len(idxs)):
                            u = idxs[iii].u / pow(2, 10)
                            v = idxs[iii].v / pow(2, 10)

                            uvs.append(tuple((u, v)))

                        validCount = 0
                        flipIdxs = 0
                        for iii in range(len(idxs) - 2):
                            validCount = validCount + 1
                            if validCount >= 4:
                                validCount = 1

                            if validCount == 1:
                                #flipIdxs = flipIdxs + 1

                                va = idxs[iii].i + 1
                                vb = idxs[iii + 1].i + 1
                                vc = idxs[iii + 2].i + 1

                                #if flipIdxs % 2 == 0:
                                    #indices.append(tuple((vc, vb, va)))
                                #else:
                                    #indices.append(tuple((va, vb, vc)))

                                indices.append(tuple((va, vb, vc)))

                        last_index += len(idxs)

                    GM2MeshCreator.create_mesh_surface(self, context, new_obj,
                                                       GM2MeshCreator.SurfData(verts, indices, uvs))

                if self.smooth_shading:
                    new_obj.data.polygons.foreach_set('use_smooth', [True] * len(new_obj.data.polygons))

            if (obj_data.off_firstchild != 0):
                GM2ModelImporter.import_objects(self, context, model_data, obj_data.off_firstchild,
                                                new_obj, isNmh2)
            next_offset = obj_data.off_next

    def get_strips(self, surf, obj, idxMode) -> list:
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
                        if (idxMode == "OPT_D") or (idxMode == "OPT_A" and obj.data_c != None):
                            ibuf = surfbuf[head:head + 11]
                            head += 11

                            idx = struct.unpack('>H', ibuf[0:2])[0]
                            _normal = ibuf[2:5]
                            _color = ibuf[5:7]
                            u = struct.unpack('>h', ibuf[7:9])[0]
                            v = struct.unpack('>h', ibuf[9:11])[0]
                        else:
                            if (idxMode == "OPT_C") or (idxMode == "OPT_A" and
                                                        GM2ModelImporter.get_tristrip_format(self, surf, num_idx) == 1):
                                ibuf = surfbuf[head + 2:head + 11]
                                head += 11
                            else:
                                ibuf = surfbuf[head:head + 9]
                                head += 9

                            idx = struct.unpack('>H', ibuf[0:2])[0]
                            u = struct.unpack('>h', ibuf[5:7])[0]
                            v = struct.unpack('>h', ibuf[7:9])[0]

                        if len(surf.v_buf) >= idx - 1:
                            indices.append(Gm2Idx(idx, u, v))
                        else:
                            return []
                case _:
                    print(f"ERR: unk_0 == {hex(command)}")
                    return []

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

    def get_tristrip_format(self, surface, num_idx):
        surfbuf = surface.data.data

        if surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 153 \
                or (surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 0
                    # and surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 4] != 0
                    and num_idx == surface.data.num_v_smthn_total):
            return 1
        else:
            return 0

    def get_nodetree(self, node_id: str, nodes: list):
        """Recursively get node tree"""
        children = {}
        for node in nodes:
            parent = hex(node.off_parent)
            if parent == node_id:
                child = hex(node.off)
                children[child] = GM2ModelImporter.get_nodetree(self, child, nodes)
        return children

    def get_nodetree_str(self, children: dict, nodes: dict, depth: int = 1):
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
            ret_str += GM2ModelImporter.get_nodetree_str(self, children[key], nodes, depth + 1)
        return ret_str

    def log_tree(self, log_path: str):
        in_path = ""
        gm2: Gmf2 = Gmf2.from_file(in_path)
        with open(log_path, "w") as f:
            f.write(f"GMF2 info:\n{Path(in_path).stem}\n\n--- Scene Tree ---\n")

            nodes = {}
            for node in gm2.world_objects:
                key = hex(node.off)
                nodes[key] = node

            tree = GM2ModelImporter.get_nodetree(self, hex(0), gm2.world_objects)
            tree_str = GM2ModelImporter.get_nodetree_str(self, tree, nodes)

            print(tree_str)
            f.write(tree_str)

    def execute(self, context):
        return {'FINISHED'}
