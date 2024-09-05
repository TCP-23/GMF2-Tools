import bpy
import bmesh
from collections import namedtuple
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import mathutils


class GM2MeshCreator(Operator, AddObjectHelper):
    """Create mesh data from a GMF2 file"""
    bl_idname = "gm2_importer.mesh_creation"
    bl_label = "Create GMF2 mesh"

    SurfData = namedtuple("SurfData", "v i uvs")

    def create_mesh(self, context, id, origin=None):
        mesh = bpy.data.meshes.new(id)

        from bpy_extras import object_utils
        obj = object_utils.object_data_add(context, mesh, operator=None)

        if origin != None:
            context.scene.cursor.location = (0, 0, 0)
            context.view_layer.objects.active = obj
            context.scene.cursor.location = origin
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            context.scene.cursor.location = (0, 0, 0)
            context.view_layer.objects.active = None

        return {'FINISHED'}

    def set_mesh_parent(self, context, childId, parentId):
        if parentId != None and childId != None:
            bpy.data.objects[childId].parent = bpy.data.objects[parentId]

    def create_mesh_surface(self, context, id, sdata: SurfData):
        mesh = bpy.data.objects[id].data

        bm = bmesh.new()
        bm.from_mesh(mesh)

        for vert in sdata.v:
            vert_pos = [vert[0][0], vert[1][0], vert[2][0]]
            bm.verts.new(vert_pos)

        bm.verts.ensure_lookup_table()

        for idx_group in sdata.i:
            if idx_group.count(idx_group[0]) == 1 and idx_group.count(idx_group[1]) == 1 and idx_group.count(idx_group[2]) == 1:
                if not bm.faces.get([bm.verts[j - 1] for j in idx_group]):
                    bm.faces.new([bm.verts[j - 1] for j in idx_group])

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

        return {'FINISHED'}

    def execute(self, context):
        #create_mesh(self, context, None)

        return {'FINISHED'}
