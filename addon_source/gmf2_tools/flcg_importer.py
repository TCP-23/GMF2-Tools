import bpy
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from .flcg import Flcg

class GCLModelImporter(Operator, AddObjectHelper):
    """Import mesh data from a FLCG file"""
    bl_idname = "gcl_importer.model_data"
    bl_label = "Import FLCG Model"

    bmat_list = {}

    def load_file_data(self, context, filepath):
        GCLModelImporter.bmat_list.clear()

        gcl: Flcg = Flcg.from_file(filepath)

        if self.import_mats:
            GCLModelImporter.import_dummy_materials(self, gcl.materials)

        GCLModelImporter.import_objects(self, context, gcl.objects)

    def import_dummy_materials(self, materials):
        for mat in materials:
            new_bmat = GCLModelImporter.create_dummy_material(self, mat)

        GCLModelImporter.bmat_list[mat.offset] = new_bmat

    def create_dummy_material(self, mat_info):
        bmat = bpy.data.materials.new(mat_info.name)
        bmat.use_nodes = True
        bmat.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1

        return bmat
    
    def import_objects(self, context, objects):
        for o_info in objects:
            obj_mesh = bpy.data.meshes.new(o_info.name)
            new_obj = object_utils.object_data_add(context, obj_mesh, operator=None)

            position = tuple((o_info.origin.x * self.imp_scale, o_info.origin.y * self.imp_scale, o_info.origin.z * self.imp_scale))
            new_obj.location = position
        
