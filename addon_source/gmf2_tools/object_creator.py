import bpy
import bmesh
from collections import namedtuple
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import math
import random

from .target_game import GameTarget_Enum
from .target_game import TargetGame


class GM2ObjectCreator(Operator, AddObjectHelper):
    """Creates object data from a GMF2 file"""
    bl_idname = "gm2_importer.object_creation"
    bl_label = "Create GMF2 Object"

    SurfData = namedtuple("SurfData", "verts idxs uvs norms")

    normals = {}

    def create_object(self, context, objData, upAxis):
        #print(f"{objData.obj.name}.isBone == {objData.obj.isBone}")

        obj_mesh = bpy.data.meshes.new(objData.obj.name)
        new_obj = object_utils.object_data_add(context, obj_mesh, operator=None)

        position = tuple((objData.obj.position.x * 0.1, objData.obj.position.y * 0.1, objData.obj.position.z * 0.1))

        new_obj.location = position

        if (objData.parent_obj is None) and (self.up_axis != 'OPT_C'):
            if self.up_axis == 'OPT_A':
                rotation = tuple((0, objData.obj.rotation.y + math.radians(90), objData.obj.rotation.z))
            else:
                rotation = tuple((math.radians(90), objData.obj.rotation.y, objData.obj.rotation.z))
        else:
            if TargetGame.gameId == GameTarget_Enum.NMH2 and objData.obj.isBone is False:
                if not objData.parent_obj.isBone:
                    rotation = tuple((0, objData.obj.rotation.y, objData.obj.rotation.z))
                else:
                    rotation = tuple((objData.obj.rotation.x, objData.obj.rotation.y, objData.obj.rotation.z))
            else:
                rotation = tuple((objData.obj.rotation.x, objData.obj.rotation.y, objData.obj.rotation.z))

        new_obj.rotation_euler = rotation

        return new_obj

    def create_mesh(self, meshData):
        pass

    def create_bone(self, context, boneData, parent_empty):
        new_arm = bpy.data.armatures.new(f"temp_arm_{boneData.name}")
        arm_obj = object_utils.object_data_add(context, new_arm, operator=None)

        arm_obj.parent = parent_empty

        context.view_layer.objects.active = arm_obj
        if context.active_object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        new_bone = new_arm.edit_bones.new(boneData.name)
        new_bone.head = tuple((0, 0, 0))
        new_bone.tail = tuple((0, 0, 0.1))
        #if boneData.parent is not None:
            #pass

        bpy.ops.object.mode_set(mode="OBJECT")

        return arm_obj


    def create_mesh_vertices(self):
        pass

    def create_mesh_surface(self, mesh, sdata: SurfData, mat_index):
        bm = bmesh.new()
        bm.from_mesh(mesh)

        if len(sdata.verts) > 0:
            for vert in sdata.verts:
                bm.verts.new([vert[0], vert[1], vert[2]])
            bm.to_mesh(mesh)

        bm.verts.ensure_lookup_table()

        uv_layer = bm.loops.layers.uv.verify()

        iteration = 0
        for idx_group in sdata.idxs:
            if idx_group.count(idx_group[0]) == 1 and idx_group.count(idx_group[1]) == 1 and idx_group.count(
                    idx_group[2]) == 1:
                if not bm.faces.get([bm.verts[j - 1] for j in idx_group]):
                    face = bm.faces.new([bm.verts[j - 1] for j in idx_group])
                    for loop in face.loops:
                        vert = loop.vert
                        if GM2ObjectCreator.normals.get(vert.index) is None and vert.index >= 0:
                            GM2ObjectCreator.normals[vert.index] = sdata.norms[iteration]

                        loop_uv = loop[uv_layer]
                        loop_uv.uv = sdata.uvs[iteration]
                        iteration += 1

                    if self.import_mats:
                        face.material_index = mesh["MatIdxs"][str(mat_index)]

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

    def apply_normals(self, mesh):
        normals = []

        for i in range(len(mesh.vertices)):
            if i < 0 or i > len(GM2ObjectCreator.normals):
                return

            normals.append(GM2ObjectCreator.normals[i])

        mesh.normals_split_custom_set_from_vertices(normals)
        GM2ObjectCreator.normals = {}

    def apply_materials(self, mesh, objData, mat_list):
        mat_idx_chart = {}

        for i, surf in enumerate(objData.surfaces):
            if mat_list[surf.off_material].name not in mesh.data.materials:
                mesh.data.materials.append(mat_list[surf.off_material])
                mat_idx_chart[str(surf.off_material)] = len(mesh.data.materials) - 1

        mesh.data["MatIdxs"] = mat_idx_chart
