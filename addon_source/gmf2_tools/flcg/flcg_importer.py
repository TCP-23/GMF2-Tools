import bpy
import bmesh
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add

import math

from typing import NamedTuple

from .flcg import Flcg
from .collision_object_info import *

SCALE_MULTIPLIER = 0.1


class BlenderColor(NamedTuple):
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
MATERIAL_COLORS = [BlenderColor(0.6118, 0.6706, 0.5176),
                   BlenderColor(0.9137, 0.498, 0.2902),
                   BlenderColor(0.3765, 0.4824, 0.5608),
                   BlenderColor(0.9686, 0.8902, 0.5882),
                   BlenderColor(0.9882, 0.9804, 0.9333),
                   BlenderColor(0.8667, 0.6824, 0.8275),
                   BlenderColor(0.8549, 0.4235, 0.4235),
                   BlenderColor(0.4118, 0.4353, 0.7804),
                   BlenderColor(0.541, 0.3333, 0.3412),
                   BlenderColor(1.0, 0.5647, 0.7373)]


class GCLModelImporter(Operator, AddObjectHelper):
    """Import mesh data from a FLCG file"""
    bl_idname = "gcl_importer.model_data"
    bl_label = "Import FLCG Model"

    bmat_list = {}
    bobj_list = {}

    def load_file_data(self, context, filepath):
        GCLModelImporter.bmat_list.clear()
        GCLModelImporter.bobj_list.clear()

        gcl = Flcg.from_file(filepath)

        minfo_list = create_minfo_from_wobjects(gcl.objects)

        if self.import_mats:
            GCLModelImporter.import_dummy_materials(self, gcl.materials)

        GCLModelImporter.import_objects(self, context, minfo_list)

        GCLModelImporter.cleanup(self, context)

    def import_dummy_materials(self, materials: list[Flcg.Material]):
        for i, mat in enumerate(materials):
            new_bmat = GCLModelImporter.create_dummy_material(self, mat, i)
            GCLModelImporter.bmat_list[mat.offset] = new_bmat

    def create_dummy_material(self, mat_info: Flcg.Material, mat_index: int):
        bmat = bpy.data.materials.new(mat_info.name)
        bmat.use_nodes = True
        bmat.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1
        if (self.generate_mat_colors):
            mat_index_truncated = mat_index
            while mat_index_truncated >= len(MATERIAL_COLORS):
                mat_index_truncated -= len(MATERIAL_COLORS)

            bmat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = MATERIAL_COLORS[mat_index_truncated]
            bmat.diffuse_color = MATERIAL_COLORS[mat_index_truncated]

        return bmat
    
    def import_objects(self, context, objects: list[CollisionModelObjectInfo]):
        for minfo in objects:
            obj_mesh = bpy.data.meshes.new(minfo.name)
            new_obj = object_utils.object_data_add(context, obj_mesh, operator=None)

            position = tuple((minfo.data_object.origin.x * SCALE_MULTIPLIER * self.imp_scale, minfo.data_object.origin.y * SCALE_MULTIPLIER * self.imp_scale,
                              minfo.data_object.origin.z * SCALE_MULTIPLIER * self.imp_scale))
            new_obj.location = position

            # still need to rewrite this...
            half_pi = math.pi / 2
            if not minfo.is_child and self.up_axis is not 'OPT_C':
                if self.up_axis is 'OPT_A':
                    rotation = tuple((0, half_pi, 0))
                else:
                    rotation = tuple((half_pi, 0, 0))
            else:
                rotation = tuple((0, 0, 0))
            new_obj.rotation_euler = rotation

            if minfo.has_model_data:
                bm = bmesh.new()

                # we still need to unpack the area data here, but for now we can just get the triangles
                for tri in minfo.data_object.model_data.col_tris:
                    bvert1 = bm.verts.new([tri.vertex1.x * SCALE_MULTIPLIER * self.imp_scale, tri.vertex1.y * SCALE_MULTIPLIER * self.imp_scale,
                                           tri.vertex1.z  * SCALE_MULTIPLIER * self.imp_scale])
                    bvert2 = bm.verts.new([tri.vertex2.x * SCALE_MULTIPLIER * self.imp_scale, tri.vertex2.y * SCALE_MULTIPLIER * self.imp_scale,
                                           tri.vertex2.z  * SCALE_MULTIPLIER * self.imp_scale])
                    bvert3 = bm.verts.new([tri.vertex3.x * SCALE_MULTIPLIER * self.imp_scale, tri.vertex3.y * SCALE_MULTIPLIER * self.imp_scale,
                                           tri.vertex3.z  * SCALE_MULTIPLIER * self.imp_scale])
                    
                    new_face = bm.faces.new([bvert1, bvert2, bvert3])
                    if self.import_mats:
                        if GCLModelImporter.bmat_list[tri.off_material] not in new_obj.data.materials.values():
                            new_obj.data.materials.append(GCLModelImporter.bmat_list[tri.off_material])
                        
                        mat_dict = {slot.material.name: i for i, slot in enumerate(new_obj.material_slots) if slot.material}
                        new_face.material_index = mat_dict.get(GCLModelImporter.bmat_list[tri.off_material].name)

                bm.verts.ensure_lookup_table()
                
                bm.to_mesh(obj_mesh)
                obj_mesh.update()
                bm.free()

            GCLModelImporter.bobj_list[minfo.data_object.offset] = new_obj
            if minfo.is_child:
                new_obj.parent = GCLModelImporter.bobj_list[minfo.parent.data_object.offset]
    
    def cleanup(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')
