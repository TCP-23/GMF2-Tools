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

    def create_mesh(self, context, id):
        mesh = bpy.data.meshes.new(id)

        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=None)

        return {'FINISHED'}

    def create_mesh_surface(self, context, id, sdata: SurfData):
        mesh = bpy.data.objects[id].data

        bm = bmesh.new()
        bm.from_mesh(mesh)

        for vert in sdata.v:
            vert_pos = [vert[0][0], vert[1][0], vert[2][0]]
            bm.verts.new(vert_pos)

        bm.verts.ensure_lookup_table()

        print(sdata.i)

        for idx_group in sdata.i:
            if idx_group.count(idx_group[0]) == 1 and idx_group.count(idx_group[1]) == 1 and idx_group.count(idx_group[2]) == 1:
                if not bm.faces.get([bm.verts[j - 1] for j in idx_group]):
                    bm.faces.new([bm.verts[j - 1] for j in idx_group])

        #for idx_group in obj.i:
            #if idx_group[0] <= len(obj.v) and idx_group[1] <= len(obj.v) and idx_group[2] <= len(obj.v):
                #if (idx_group[0] != idx_group[1]) and (idx_group[0] != idx_group[2]) and (idx_group[1] != idx_group[2]):
                    #if not bm.faces.get([bm.verts[j - 1] for j in idx_group]):
                        #bm.faces.new([bm.verts[j - 1] for j in idx_group])

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

        return {'FINISHED'}

    def trim_indices(self, un_idxs) -> list:
        trimmed_idxs = []
        for ind in un_idxs:
            ind_perms = []
            ind_perms.append(tuple((ind[0], ind[1], ind[2])))

        return trimmed_idxs

    def execute(self, context):
        #create_mesh(self, context, None)

        return {'FINISHED'}
