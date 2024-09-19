import bpy
import bmesh
from collections import namedtuple
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import math

class GM2MeshCreator(Operator, AddObjectHelper):
    """Create mesh data from a GMF2 file"""
    bl_idname = "gm2_importer.mesh_creation"
    bl_label = "Create GMF2 mesh"

    SurfData = namedtuple("SurfData", "v i uvs")

    def create_object(self, context, obj_data, parent, fixCoord):
        obj_mesh = bpy.data.meshes.new(obj_data.name)
        from bpy_extras import object_utils
        new_obj = object_utils.object_data_add(context, obj_mesh, operator=None)

        context.view_layer.objects.active = new_obj

        if parent != None:
            new_obj.parent = parent

        pos = tuple((obj_data.origin.x * 0.1, obj_data.origin.y * 0.1, obj_data.origin.z * 0.1))
        new_obj.location = pos

        if parent == None and fixCoord:
            rot = tuple((math.radians(90), obj_data.rot_y, 0))
        else:
            rot = tuple((0, obj_data.rot_y, 0))
        new_obj.rotation_euler = rot

        context.view_layer.objects.active = None

        return new_obj

    def create_mesh_surface(self, context, obj, sdata: SurfData):
        mesh = obj.data

        bm = bmesh.new()
        bm.from_mesh(mesh)

        for vert in sdata.v:
            vert_pos = [vert[0], vert[1], vert[2]]
            #print(vert_pos)
            bm.verts.new(vert_pos)

        bm.verts.ensure_lookup_table()

        for idx_group in sdata.i:
            if idx_group.count(idx_group[0]) == 1 and idx_group.count(idx_group[1]) == 1 and idx_group.count(
                    idx_group[2]) == 1:
                if not bm.faces.get([bm.verts[j - 1] for j in idx_group]):
                    bm.faces.new([bm.verts[j - 1] for j in idx_group])

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

        return {'FINISHED'}

    def execute(self, context):
        return {'FINISHED'}
