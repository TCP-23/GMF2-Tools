import bpy
import random
from bpy.types import Operator


class GCTTextureHandler(Operator):

    tex_list = {}
    mat_list = {}

    def import_textures(self, context, textures):
        for i, tex in enumerate(textures):
            new_btex = GCTTextureHandler.create_texture(self, tex)

    def import_materials(self, context, materials):
        for i, mat in enumerate(materials):
            new_mat = GCTTextureHandler.create_material(self, mat)
            GCTTextureHandler.mat_list[mat.offset] = new_mat

    def export_textures(self, context):
        pass

    def create_texture(self, tex_data):
        return tex_data

    def create_material(self, matData):
        mat = bpy.data.materials.new(matData.name)
        mat.diffuse_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)

        return mat

    def load_texture_data(self):
        pass
