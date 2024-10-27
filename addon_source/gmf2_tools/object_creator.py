import bpy
import bmesh
from collections import namedtuple
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import math

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

        position = tuple((objData.obj.origin.x * 0.1, objData.obj.origin.y * 0.1, objData.obj.origin.z * 0.1))
        new_obj.location = position

        rotation = tuple((0, objData.obj.rot_y, objData.obj.rot_z))
        new_obj.rotation_euler = rotation

        return new_obj

    def create_mesh(self, meshData):
        pass

    def create_bone(self, boneData):
        pass

    def create_mesh_surface(self, mesh, sdata: SurfData):
        bm = bmesh.new()
        bm.from_mesh(mesh)

        for vert in sdata.verts:
            bm.verts.new([vert[0], vert[1], vert[2]])

        bm.verts.ensure_lookup_table()

        uv_layer = bm.loops.layers.uv.verify()

        iter = 0
        for idx_group in sdata.idxs:
            if idx_group.count(idx_group[0]) == 1 and idx_group.count(idx_group[1]) == 1 and idx_group.count(idx_group[2]) == 1:
                if not bm.faces.get([bm.verts[j-1] for j in idx_group]):
                    face = bm.faces.new([bm.verts[j-1] for j in idx_group])
                    for loop in face.loops:
                        vert = loop.vert
                        if GM2ObjectCreator.normals.get(vert.index) is None and vert.index >= 0:
                            GM2ObjectCreator.normals[vert.index] = sdata.norms[iter]

                        loop_uv = loop[uv_layer]
                        loop_uv.uv = sdata.uvs[iter]
                        iter += 1

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

    def apply_normals(self, mesh):
        normals = []
        #for i in range(len(mesh.vertices)):
            #pass

        while len(normals) < len(GM2ObjectCreator.normals):
            for k, v in GM2ObjectCreator.normals.items():
                if int(k) < 0 or int(k) > len(GM2ObjectCreator.normals):
                    break

                if len(normals) == int(k):
                    normals.append(v)

        mesh.normals_split_custom_set_from_vertices(normals)
        GM2ObjectCreator.normals = normals
