import bpy
import bmesh
from collections import namedtuple
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import math

from .target_game import GameTarget_Enum
from .target_game import TargetGame


class GM2ObjectCreator(Operator, AddObjectHelper):
    """Creates object data from a GMF2 file"""
    bl_idname = "gm2_importer.object_creation"
    bl_label = "Create GMF2 Object"

    SurfData = namedtuple("SurfData", "verts idxs uvs norms")

    normals = {}

    def create_object(self, context, objData, upAxis):
        #new_obj = bpy.ops.object.empty_add()
        #new_obj.name = objData.obj.name

        obj_mesh = bpy.data.meshes.new(objData.obj.name)
        new_obj = object_utils.object_data_add(context, obj_mesh, operator=None)

        # set position
        # set rotation

        #if TargetGame.gameId == GameTarget_Enum.NMH2:
            #position = tuple((objData.obj.origin.x * 0.1, objData.obj.origin.z * 0.1, -(objData.obj.origin.y * 0.1)))
        #else:
        position = tuple((objData.obj.position.x * 0.1, objData.obj.position.y * 0.1, objData.obj.position.z * 0.1))
        new_obj.location = position

        if (objData.parent_obj is None) and (self.up_axis != 'OPT_C'):
            if self.up_axis == 'OPT_A':
                rotation = tuple((0, objData.obj.rotation.y + math.radians(90), objData.obj.rotation.z))
            else:
                rotation = tuple((math.radians(90), objData.obj.rotation.y, objData.obj.rotation.z))
        else:
            rotation = tuple((0, objData.obj.rotation.y, objData.obj.rotation.z))
        new_obj.rotation_euler = rotation

        return new_obj

    def create_mesh(self, meshData):
        pass

    def create_bone(self, boneData):
        pass

    def create_mesh_vertices(self):
        pass

    def create_mesh_surface(self, mesh, sdata: SurfData):
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
            if idx_group.count(idx_group[0]) == 1 and idx_group.count(idx_group[1]) == 1 and idx_group.count(idx_group[2]) == 1:
                if not bm.faces.get([bm.verts[j-1] for j in idx_group]):
                    face = bm.faces.new([bm.verts[j-1] for j in idx_group])
                    for loop in face.loops:
                        vert = loop.vert
                        if GM2ObjectCreator.normals.get(vert.index) is None and vert.index >= 0:
                            GM2ObjectCreator.normals[vert.index] = sdata.norms[iteration]

                        loop_uv = loop[uv_layer]
                        loop_uv.uv = sdata.uvs[iteration]
                        iteration += 1

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
