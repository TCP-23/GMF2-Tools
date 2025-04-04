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

    try:
        if surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 153 \
                or (surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 0
                    # and surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 4] != 0
                    and num_idx == surface.surface_data.num_vertices):
            return 1
    except IndexError:
        pass
        #print("Error in detecting tristrip format!")
        #print(f"Surface buffer length: {len(surfbuf)}")

    return 0


class GM2ModelImporter(Operator):
    """Import mesh data from a GMF2 file"""
    bl_idname = "gm2_importer.model_data"
    bl_label = "Import GMF2 model"

    obj_list = {}
    junk_objs = {}
    temp_arm_list = {}

    def load_file_data(self, context, filepath):
        GM2ModelImporter.obj_list.clear()
        GM2ModelImporter.junk_objs.clear()

        gm2: Gmf2 = Gmf2.from_file(filepath)

        if gm2.game_identifier == 4294967295 or gm2.game_identifier == 8:
            TargetGame.gameId = GameTarget_Enum.NMH2
        else:
            TargetGame.gameId = GameTarget_Enum.NMH1

        unsorted_objects = {}
        for i, world_object in enumerate(gm2.world_objects):
            unsorted_objects[world_object.offset] = world_object

        objects, bones = sort_objects(unsorted_objects)
        obj_armature = None

        if self.import_mats:
            if len(gm2.textures) > 0:
                GCTTextureHandler.import_textures(self, context, gm2.textures)
            if len(gm2.materials) > 0:
                GCTTextureHandler.import_materials(self, context, gm2.materials)

        if self.import_models:
            if len(bones) > 0:
                obj_armature = GM2ModelImporter.import_bones(self, context, bones)
            if len(objects) > 0:
                GM2ModelImporter.import_objects(self, context, objects)

        GM2ModelImporter.cleanup_imported(self, context, objects, obj_armature)

    """def import_objects(self, context, objects):
        for i, processed_obj in enumerate(objects):
            new_obj = GM2ObjectCreator.create_object(self, context, processed_obj, self.up_axis)
            GM2ModelImporter.obj_list[processed_obj.obj] = new_obj

            if processed_obj.parent_obj is not None:
                new_obj.parent = GM2ModelImporter.obj_list[processed_obj.parent_obj]

            if processed_obj.obj.surfaces is not None:
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

                new_obj.data.polygons.foreach_set('use_smooth', [True] * len(new_obj.data.polygons))

                if len(GM2ObjectCreator.normals) > 0:
                    GM2ObjectCreator.apply_normals(self, new_obj.data)"""

    def import_objects(self, context, objects):
        for processed_obj in objects:
            if processed_obj.obj.surfaces is not None:
                obj_data = [[], [], [], [], [], []]

                obj_data[0] += GM2ModelImporter.get_surface_verts(self, processed_obj, processed_obj.obj.surfaces[0])
                for surf in processed_obj.obj.surfaces:
                    surf_idxs, surf_uvs, surf_norms = GM2ModelImporter.get_surface_data(self, processed_obj, surf)

                    obj_data[1].append(surf_idxs)
                    obj_data[2] += surf_uvs
                    obj_data[3] += surf_norms
                    obj_data[5].append(surf.off_material)

                new_mesh = GM2ObjectCreator.create_mesh(self, context, processed_obj, obj_data)
                GM2ModelImporter.obj_list[processed_obj.obj] = new_mesh

                if processed_obj.parent_obj is not None:
                    new_mesh.parent = GM2ModelImporter.obj_list[processed_obj.parent_obj]

                if len(GM2ObjectCreator.normals) > 0:
                    GM2ObjectCreator.apply_normals(self, new_mesh.data)

                #if self.import_mats:
                    #GM2ObjectCreator.apply_materials(self, new_mesh, processed_obj.obj, GCTTextureHandler.mat_list)

                #new_mesh.data.polygons.foreach_set('use_smooth', [True] * len(new_mesh.data.polygons))
            else:
                new_obj = GM2ObjectCreator.create_object(self, context, processed_obj, self.up_axis)
                GM2ModelImporter.obj_list[processed_obj.obj] = new_obj

                if processed_obj.parent_obj is not None:
                    new_obj.parent = GM2ModelImporter.obj_list[processed_obj.parent_obj]

    def get_surface_verts(self, processed_obj, surf):
        mesh_strips = GM2ModelImporter.get_mesh_strips(self, surf, processed_obj)

        if not mesh_strips:
            return []

        verts = []

        for v in surf.v_buf:
            if TargetGame.gameId == GameTarget_Enum.NMH1:
                try:
                    vertPos = Vec3((v.x / pow(2, processed_obj.obj.v_divisor)) * 0.1,
                               (v.y / pow(2, processed_obj.obj.v_divisor)) * 0.1,
                               (v.z / pow(2, processed_obj.obj.v_divisor)) * 0.1)
                except OverflowError:
                    vertPos = Vec3(1 * 0.1,
                               1 * 0.1,
                               1 * 0.1)
                    print(len(surf.v_buf))
                    return []
            elif TargetGame.gameId == GameTarget_Enum.NMH2:
                vertPos = Vec3(v.x * 0.1, v.y * 0.1, v.z * 0.1)
            else:
                return []

            verts.append(vertPos)

        return verts

    def get_surface_data(self, processed_obj, surf):
        mesh_strips = GM2ModelImporter.get_mesh_strips(self, surf, processed_obj)

        if not mesh_strips:
            return [], [], []

        indices = []
        uvs = []
        normals = []

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

        return indices, uvs, normals

    def import_bones(self, context, bones):
        root_key = ""
        bone_model = None

        combined_armature = None

        if not self.display_tails:
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1)
            bone_model = bpy.context.active_object

        for i, bone in enumerate(bones):
            new_bone = GM2ObjectCreator.create_object(self, context, bone, self.up_axis)
            GM2ModelImporter.junk_objs[bone.obj] = new_bone
            GM2ModelImporter.obj_list[bone.obj] = new_bone

            if bone.parent_obj is not None:
                new_bone.parent = GM2ModelImporter.obj_list[bone.parent_obj]
                new_bone.parent = GM2ModelImporter.junk_objs[bone.parent_obj]

            temp_arm = GM2ObjectCreator.create_bone(self, context, bone, new_bone)
            GM2ModelImporter.temp_arm_list[temp_arm.name] = temp_arm

        for obj in context.selected_objects:
            obj.select_set(False)

        for j, arm_obj in GM2ModelImporter.temp_arm_list.items():
            root_key = j
            arm_obj.select_set(True)

        context.view_layer.objects.active = GM2ModelImporter.temp_arm_list[root_key]
        bpy.ops.object.join()

        combined_armature = context.view_layer.objects.active
        combined_armature.name = "ROOT_armature"
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        if context.active_object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        all_bones = context.view_layer.objects.active.data.edit_bones
        for bone in bones:
            if bone.parent_obj is not None:
                all_bones[bone.obj.name].parent = all_bones[bone.parent_obj.name]

        GM2ModelImporter.temp_arm_list = {}
        bpy.ops.object.mode_set(mode="OBJECT")

        if not self.display_tails:
            pose_bones = bpy.context.object.pose.bones

            for bone in pose_bones:
                bone.custom_shape = bone_model
                bone.custom_shape_scale_xyz = tuple((0.005, 0.005, 0.005))
                bone.use_custom_shape_bone_size = False

            bpy.ops.object.mode_set(mode="OBJECT")

            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[bone_model.name].select_set(True)
            bpy.ops.object.delete(use_global=False, confirm=False)

        return combined_armature

    def cleanup_imported(self, context, process_obj_list, root_armature):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')

        if self.import_models:
            for obj in process_obj_list:
                if obj.parent_obj is not None and obj.parent_obj in GM2ModelImporter.junk_objs:
                    bpy.data.objects[GM2ModelImporter.obj_list[obj.obj].name].select_set(True)

                    parent_name = GM2ModelImporter.obj_list[obj.parent_obj].name
                    context.view_layer.objects.active = root_armature
                    root_armature.data.bones.active = root_armature.data.bones[parent_name]

                    bpy.ops.object.parent_set(type='BONE', keep_transform=True)

                    bpy.data.objects[GM2ModelImporter.obj_list[obj.obj].name].select_set(False)

            for junk_obj in GM2ModelImporter.junk_objs:
                GM2ModelImporter.junk_objs[junk_obj].data.user_clear()
                bpy.data.objects[junk_obj.name].select_set(True)

            bpy.ops.object.delete(use_global=False, confirm=False)

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

    """def get_surface_data(self, processed_obj, surf, surf_id):
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

        return verts, indices, uvs, normals"""
