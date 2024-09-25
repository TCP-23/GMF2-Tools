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
            rot = tuple((math.radians(90), obj_data.rot_y, obj_data.rot_z))
        else:
            rot = tuple((0, obj_data.rot_y, obj_data.rot_z))
        new_obj.rotation_euler = rot

        print(f"\n//////////////////////////////////////////////////\nnew object: {new_obj.name}\n//////////////////////////////////////////////////")

        context.view_layer.objects.active = None

        return new_obj

    def create_mesh_surface(self, context, obj, sdata: SurfData):
        print(f"--- new mesh surface for {obj.name} ---")
        print(f"total indices: {len(sdata.i)}")
        print(f"total uvs: {len(sdata.uvs)}")
        mesh = obj.data

        bm = bmesh.new()
        bm.from_mesh(mesh)

        for vert in sdata.v:
            vert_pos = [vert[0], vert[1], vert[2]]
            bm.verts.new(vert_pos)

        bm.verts.ensure_lookup_table()

        uv_layer = bm.loops.layers.uv.verify()

        #loops = []
        #iter = len(sdata.uvs) - 1
        iter = 0
        faces = 0
        for idx_group in sdata.i:
            if idx_group.count(idx_group[0]) == 1 and idx_group.count(idx_group[1]) == 1 and idx_group.count(
                    idx_group[2]) == 1:
                if not bm.faces.get([bm.verts[j - 1] for j in idx_group]):
                    face = bm.faces.new([bm.verts[j - 1] for j in idx_group])
                    for loop in face.loops:
                        # loops.append(loop)
                        loop_uv = loop[uv_layer]
                        loop_uv.uv = sdata.uvs[iter]
                        iter += 1
                    faces += 1

        """for loop in loops:
            loop_uv = loop[uv_layer]
            loop_uv.uv = sdata.uvs[iter]
            iter += 1"""

        """for face in bm.faces:
            for loop in face.loops:
                loop_uv = loop[uv_layer]
                if len(sdata.uvs) > iter:
                    loop_uv.uv = sdata.uvs[iter]
                    iter += 1"""

        print(f"uvs: {iter}\nfaces: {faces}\nloops: {iter}")
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

        """bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(mesh)

        uv_layer = bm.loops.layers.uv.verify()

        iter = 0
        faces = 0
        loops = 0
        for face in bm.faces:
            for loop in face.loops:
                loop_uv = loop[uv_layer]
                if len(sdata.uvs) > iter:
                    loop_uv.uv = sdata.uvs[iter]
                    iter += 1
                loops += 1
            faces += 1
        
        print(f"uvs: {iter}\nfaces: {faces}\nloops: {loops}")
        
        bmesh.update_edit_mesh(mesh)
        bpy.ops.object.mode_set(mode="OBJECT")"""

        return {'FINISHED'}

    def execute(self, context):
        return {'FINISHED'}
