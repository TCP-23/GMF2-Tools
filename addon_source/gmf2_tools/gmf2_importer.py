import bpy
import struct
from collections import namedtuple
from bpy.types import Operator

from .target_game import GameTarget_Enum
from .target_game import TargetGame

from .gmf2 import Gmf2
from .object_creator import GM2ObjectCreator
from .gct0_handler import GCTTextureHandler

Vec3 = namedtuple("Vec3", "x y z")
Gm2Idx = namedtuple("Gm2Idx", "i u v n")


class ProcessedObject:
    obj = None
    parent_obj = None
    first_child_obj = None
    prev_obj = None
    next_obj = None

    def __init__(self, _obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj):
        self.obj = _obj
        self.parent_obj = _parent_obj
        self.first_child_obj = _first_child_obj
        self.prev_obj = _prev_obj
        self.next_obj = _next_obj


def sort_objects(objs):
    sorted_objs = []
    sorted_bones = []

    bone_world_objects = []

    for i, world_object in objs.items():
        parent, first_child, prev_obj, next_obj = None, None, None, None

        if world_object.off_parent in objs:
            parent = objs[world_object.off_parent]
        if world_object.off_first_child in objs:
            first_child = objs[world_object.off_first_child]
        if world_object.off_prev in objs:
            prev_obj = objs[world_object.off_prev]
        if world_object.off_next in objs:
            next_obj = objs[world_object.off_next]

        processed_obj = ProcessedObject(world_object, parent, first_child, prev_obj, next_obj)
        if processed_obj.obj.name == "ROOT" and processed_obj.obj.surfaces is None:
            processed_obj.obj.isBone = True
            sorted_bones.append(processed_obj)
            bone_world_objects.append(processed_obj.obj)
        elif processed_obj.parent_obj in bone_world_objects and processed_obj.obj.surfaces is None:
            processed_obj.obj.isBone = True
            sorted_bones.append(processed_obj)
            bone_world_objects.append(processed_obj.obj)
        else:
            processed_obj.obj.isBone = False
            sorted_objs.append(processed_obj)

    return sorted_objs, sorted_bones


def get_tristrip_format(surface, num_idx):
    surfbuf = surface.surface_data.strip_data

    if surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 153 \
            or (surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 0
                # and surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 4] != 0
                and num_idx == surface.surface_data.num_vertices):
        return 1
    else:
        return 0


class GM2ModelImporter(Operator):
    """Import mesh data from a GMF2 file"""
    bl_idname = "gm2_importer.model_data"
    bl_label = "Import GMF2 model"

    obj_list = {}

    def load_file_data(self, context, filepath):
        GM2ModelImporter.obj_list.clear()

        gm2: Gmf2 = Gmf2.from_file(filepath)

        if gm2.game_identifier == 4294967295:
            TargetGame.gameId = GameTarget_Enum.NMH2
        else:
            TargetGame.gameId = GameTarget_Enum.NMH1

        unsorted_objects = {}
        for i, world_object in enumerate(gm2.world_objects):
            unsorted_objects[world_object.offset] = world_object

        objects, bones = sort_objects(unsorted_objects)

        if self.import_mats:
            GCTTextureHandler.import_textures(self, context, gm2.textures)
            GCTTextureHandler.import_materials(self, context, gm2.materials)

        if self.import_models:
            GM2ModelImporter.import_bones(self, context, bones)
            GM2ModelImporter.import_objects(self, context, objects)

    def import_objects(self, context, objects):
        for i, processed_obj in enumerate(objects):
            new_obj = GM2ObjectCreator.create_object(self, context, processed_obj, self.up_axis)
            GM2ModelImporter.obj_list[processed_obj.obj] = new_obj

            if processed_obj.parent_obj is not None:
                new_obj.parent = GM2ModelImporter.obj_list[processed_obj.parent_obj]

            if processed_obj.obj.surfaces is not None:
                #new_mesh = GM2ObjectCreator.create_mesh(self, processed_obj)
                if self.import_mats:
                    GM2ObjectCreator.apply_materials(self, new_obj, processed_obj.obj, GCTTextureHandler.mat_list)

                for ii, surf in enumerate(processed_obj.obj.surfaces):
                    verts, idxs, uvs, normals = GM2ModelImporter.get_surface_data(self, processed_obj, surf, ii)
                    if self.import_mats:
                        GM2ObjectCreator.create_mesh_surface(self, new_obj.data,
                                                             GM2ObjectCreator.SurfData(verts, idxs, uvs, normals),
                                                             surf.off_material)
                    else:
                        GM2ObjectCreator.create_mesh_surface(self, new_obj.data,
                                                             GM2ObjectCreator.SurfData(verts, idxs, uvs, normals), -1)

                if self.smooth_shading:
                    new_obj.data.polygons.foreach_set('use_smooth', [True] * len(new_obj.data.polygons))

                if len(GM2ObjectCreator.normals) > 0:
                    GM2ObjectCreator.apply_normals(self, new_obj.data)

    def import_meshes(self, context, meshes):
        pass

    def import_bones(self, context, bones):
        for i, bone in enumerate(bones):
            new_bone = GM2ObjectCreator.create_object(self, context, bone, self.up_axis)
            GM2ModelImporter.obj_list[bone.obj] = new_bone

            if bone.parent_obj is not None:
                new_bone.parent = GM2ModelImporter.obj_list[bone.parent_obj]

        for key, bone in GM2ModelImporter.obj_list.items():
            if key.isBone:
                pass
                #GM2ObjectCreator.create_bone(self, context, bone)


    def get_mesh_strips(self, surf, processed_obj):
        surfbuf = surf.surface_data.strip_data
        mesh_strips = []

        head = 0
        i_remaining = surf.surface_data.num_vertices

        while i_remaining > 0:
            command = struct.unpack('>H', surfbuf[head:head + 2])[0]
            num_idx = struct.unpack('>H', surfbuf[head + 2:head + 4])[0]
            head += 4

            idxs = []
            match command:
                case 0x96:
                    # unknown what this does, appears in some models
                    return []
                case 0x99:
                    for _ in range(num_idx):
                        if (self.index_override == "OPT_D" or
                                (self.index_override == "OPT_A" and processed_obj.obj.v_format is not None)):
                            ibuf = surfbuf[head:head + 11]
                            head += 11

                            idx = struct.unpack('>H', ibuf[0:2])[0]
                            norm = tuple((ibuf[2], ibuf[3], ibuf[4]))
                            u = struct.unpack('>h', ibuf[7:9])[0]
                            v = struct.unpack('>h', ibuf[9:11])[0]
                        else:
                            if (self.index_override == "OPT_C" or
                                    (self.index_override == "OPT_A" and get_tristrip_format(surf, num_idx) == 1)):
                                ibuf = surfbuf[head + 2:head + 11]
                                head += 11
                            else:
                                ibuf = surfbuf[head:head + 9]
                                head += 9

                            idx = struct.unpack('>H', ibuf[0:2])[0]
                            norm = tuple((ibuf[2], ibuf[3], ibuf[4]))
                            u = struct.unpack('>h', ibuf[5:7])[0]
                            v = struct.unpack('>h', ibuf[7:9])[0]

                        if len(surf.v_buf) >= idx - 1:
                            idxs.append(Gm2Idx(idx, u, v, norm))
                        else:
                            return []
                case _:
                    print(f"ERR: unk_0 == {hex(command)}")
                    return []

            if len(idxs) <= 0:
                return []

            for i in range(num_idx - 2):
                if idxs[i] != idxs[i + 1] and idxs[i] != idxs[i + 2] and idxs[i + 1] != idxs[i + 2]:
                    if i % 2 == 0:
                        mesh_strips.append(idxs[i])
                        mesh_strips.append(idxs[i + 1])
                        mesh_strips.append(idxs[i + 2])
                    else:
                        mesh_strips.append(idxs[i])
                        mesh_strips.append(idxs[i + 2])
                        mesh_strips.append(idxs[i + 1])

            i_remaining -= num_idx

        return mesh_strips

    def get_surface_data(self, processed_obj, surf, surf_id):
        mesh_strips = GM2ModelImporter.get_mesh_strips(self, surf, processed_obj)

        if not mesh_strips:
            return [], [], [], []

        verts = []
        indices = []
        uvs = []
        normals = []

        if surf_id == 0:
            for v in surf.v_buf:
                if TargetGame.gameId == GameTarget_Enum.NMH1:
                    vertPos = Vec3((v.x / pow(2, processed_obj.obj.v_divisor)) * 0.1,
                                   (v.y / pow(2, processed_obj.obj.v_divisor)) * 0.1,
                                   (v.z / pow(2, processed_obj.obj.v_divisor)) * 0.1)
                elif TargetGame.gameId == GameTarget_Enum.NMH2:
                    vertPos = Vec3(v.x * 0.1, v.y * 0.1, v.z * 0.1)
                else:
                    return [], [], [], []

                verts.append(vertPos)

        for idx in mesh_strips:
            normals.append(idx.n)
            uvs.append(tuple((idx.u / pow(2, 10), -(idx.v / pow(2, 10)) + 1)))

        valid_idx_count = 0
        for iii in range(len(mesh_strips) - 2):
            valid_idx_count += 1
            if valid_idx_count >= 4:
                valid_idx_count = 1

            if valid_idx_count == 1:
                va = mesh_strips[iii].i + 1
                vb = mesh_strips[iii + 1].i + 1
                vc = mesh_strips[iii + 2].i + 1

                indices.append(tuple((va, vb, vc)))

        return verts, indices, uvs, normals
