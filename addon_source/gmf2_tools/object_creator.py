import bpy
import bmesh
from collections import namedtuple
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import math
import mathutils
import random

from .gct0_handler import GCTTextureHandler

from .target_game import GameTarget_Enum
from .target_game import TargetGame


class GM2ObjectCreator(Operator, AddObjectHelper):
    """Creates object data from a GMF2 file"""
    bl_idname = "gm2_importer.object_creation"
    bl_label = "Create GMF2 Object"

    SurfData = namedtuple("SurfData", "verts idxs uvs norms")

    normals = {}

    def create_object(self, context, objData, upAxis):
        obj_mesh = bpy.data.meshes.new(objData.obj.name)
        new_obj = object_utils.object_data_add(context, obj_mesh, operator=None)

        # Scale the position by 0.1
        position = tuple((objData.obj.position.x * 0.1, objData.obj.position.y * 0.1, objData.obj.position.z * 0.1))
        new_obj.location = position

        # i should rewrite this bit
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

    def create_mesh(self, context, objData, processedData, obj_arm):
        obj_mesh = bpy.data.meshes.new(objData.obj.name)
        new_obj = object_utils.object_data_add(context, obj_mesh, operator=None)

        # Scale the position by 0.1
        new_obj.location = tuple((objData.obj.position.x * 0.1, objData.obj.position.y * 0.1, objData.obj.position.z * 0.1))

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

        if self.import_mats:
            GM2ObjectCreator.apply_materials(self, new_obj, objData.obj, GCTTextureHandler.mat_list)

        GM2ObjectCreator.create_mesh_vertices(self, new_obj, processedData[0])

        # Check if the GM2 file contains an armature
        if obj_arm is not None:
            GM2ObjectCreator.create_skinned_partitions(self, context, new_obj, obj_arm, processedData[1])
        else:
            GM2ObjectCreator.create_weight_partitions(self, context, new_obj, processedData[1])
        GM2ObjectCreator.create_mesh_faces(self, context, new_obj, processedData[1], processedData[2], processedData[3], processedData[5])

        # Turn on smooth shading
        new_obj.data.polygons.foreach_set('use_smooth', [True] * len(new_obj.data.polygons))
        return new_obj

    def create_bone(self, context, boneData, parent_empty):
        # Create a new temporary armature
        new_arm = bpy.data.armatures.new(f"temp_arm_{boneData.obj.name}")
        arm_obj = object_utils.object_data_add(context, new_arm, operator=None)

        arm_obj.parent = parent_empty

        # Set the active object to the armature
        context.view_layer.objects.active = arm_obj

        # Switch to edit mode
        if context.active_object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        # Create a new bone on the temporary armature
        new_bone = new_arm.edit_bones.new(boneData.obj.name)

        new_bone.head = tuple((0, 0, 0))
        new_bone.tail = tuple((0, 0, 0.025))

        # Set the tail position of the bone (bones in GM2 models don't have head positions)
        if boneData.first_child_obj is not None and boneData.first_child_obj.isBone:
            new_bone.tail = tuple((boneData.first_child_obj.position.x * 0.1, boneData.first_child_obj.position.y * 0.1, boneData.first_child_obj.position.z * 0.1))

        # Make sure the bone can't be below the minimum length
        if new_bone.head == new_bone.tail or new_bone.length <= 0.01:
            new_bone.tail = tuple((0, 0, 0.025))

        # Switch to object mode
        bpy.ops.object.mode_set(mode="OBJECT")

        return arm_obj

    def create_mesh_vertices(self, obj, verts):
        mesh = obj.data
        bm = bmesh.new()

        if len(verts) > 0:
            for vert in verts:
                bm.verts.new([vert[0], vert[1], vert[2]])

            bm.to_mesh(mesh)
        # No need to return anything, because we directly modify the mesh data block

    # Creates vertex groups on a model
    def create_weight_partitions(self, context, obj, idxs):
        bpy.ops.object.mode_set(mode="OBJECT")
        mesh = obj.data

        bm = bmesh.new()
        bm.from_mesh(mesh)

        for i, surf in enumerate(idxs):
            obj.vertex_groups.new(name=f"surface_{i+1}")
            for idx in surf:
                try:
                    mesh.vertices[idx[0] - 1].select = True
                    mesh.vertices[idx[1] - 1].select = True
                    mesh.vertices[idx[2] - 1].select = True
                except:
                    pass

            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.object.vertex_group_assign()
            bpy.ops.object.mode_set(mode="OBJECT")

            for idx in surf:
                mesh.vertices[idx[0] - 1].select = False
                mesh.vertices[idx[1] - 1].select = False
                mesh.vertices[idx[2] - 1].select = False

    # Binds a model to an armature
    def create_skinned_partitions(self, context, obj, arm, idxs):
        GM2ObjectCreator.create_weight_partitions(self, context, obj, idxs)

        armMod = obj.modifiers.new(name="Armature", type="ARMATURE")
        armMod.object = arm

    def create_mesh_faces(self, context, obj, idxs, uvs, norms, mat_index):
        bpy.ops.object.mode_set(mode="OBJECT")
        mesh = obj.data

        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()

        uv_layer = bm.loops.layers.uv.verify()

        # Have to iterate outside the loop because of the way UVs are stored in the GM2
        uv_iter = 0
        mat_iter = 0
        for surf in idxs:
            for tri in surf:
                poly_group = [bm.verts[tri[0] - 1], bm.verts[tri[1] - 1], bm.verts[tri[2] - 1]]

                if not bm.faces.get(poly_group):
                    new_face = bm.faces.new(poly_group)
                else:
                    new_face = bm.faces.get(poly_group)

                for mesh_loop in new_face.loops:
                    vert = mesh_loop.vert
                    if GM2ObjectCreator.normals.get(vert.index) is None and vert.index >= 0:
                        GM2ObjectCreator.normals[vert.index] = norms[uv_iter]

                    uv_loop = mesh_loop[uv_layer]
                    uv_loop.uv = uvs[uv_iter]
                    uv_iter += 1

                # Set the material index of the face
                if self.import_mats:
                    new_face.material_index = mesh["MatIdxs"][str(mat_index[mat_iter])]

            mat_iter += 1

        # Apply the faces to the mesh
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()

    # Applies stored normals to a mesh
    def apply_normals(self, mesh):
        normals = []

        for i in range(len(mesh.vertices)):
            idx = i

            if idx < 0 or idx > len(GM2ObjectCreator.normals):
                return

            try:
                normals.append(GM2ObjectCreator.normals[idx])
            except KeyError:
                print("Couldn't apply normals to model. ", idx, " was greater than the normal count of ", len(GM2ObjectCreator.normals))
                #normals.append(GM2ObjectCreator.normals[idx - 1])

        if len(mesh.vertices) == len(normals):
            mesh.normals_split_custom_set_from_vertices(normals)
        GM2ObjectCreator.normals = {}

    # Applies a material to an object
    def apply_materials(self, mesh, objData, mat_list):
        mat_idx_chart = {}

        for i, surf in enumerate(objData.surfaces):
            if mat_list[surf.off_material].name not in mesh.data.materials:
                mesh.data.materials.append(mat_list[surf.off_material])
                mat_idx_chart[str(surf.off_material)] = len(mesh.data.materials) - 1

        mesh.data["MatIdxs"] = mat_idx_chart
