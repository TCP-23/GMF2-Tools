import bpy
import random
from bpy.types import Operator


class GCTTextureHandler(Operator):

    #EMPTY_TEXTURE = r"b'\x90\xc4\x88\xe1\xaf\xaf\xff\xff[9] : --- No File ---\x00\x00\x00'"

    tex_list = {}
    mat_list = {}

    def import_textures(self, context, textures):
        for i, tex in enumerate(textures):
            if "No File" not in str(tex.gct0_texture.texture_data):
                new_btex = GCTTextureHandler.create_texture(self, tex)
            else:
                new_btex = GCTTextureHandler.get_fallback_texture(self)
            GCTTextureHandler.tex_list[tex.offset] = new_btex

    def import_materials(self, context, materials):
        for i, mat in enumerate(materials):
            new_mat = GCTTextureHandler.create_material(self, mat, GCTTextureHandler.tex_list[mat.data.off_texture])
            GCTTextureHandler.mat_list[mat.offset] = new_mat

    def export_textures(self, context):
        pass

    def get_fallback_texture(self):
        if not bpy.data.textures.get("FALLBACK_TEX"):
            bimg = bpy.data.images.new("FALLBACK_TEX", 1, 1)
            pixels = []
            pixels.append([1, 1, 1, 1])

            pixels = [channel for pix in pixels for channel in pix]
            bimg.pixels = pixels

            btex = bpy.data.textures.new("FALLBACK_TEX", type='IMAGE')
            btex.image = bimg
        else:
            btex = bpy.data.textures.get("FALLBACK_TEX")

        return btex

    def create_texture(self, tex_data):
        img_size = tex_data.gct0_texture.width, tex_data.gct0_texture.height
        bimg = bpy.data.images.new(tex_data.name, width=img_size[0], height=img_size[1])
        pixels = [None] * img_size[0] * img_size[1]
        for x in range(img_size[0]):
            for y in range(img_size[1]):
                r = 0.8
                g = y / img_size[1]
                b = 0.6
                a = 1.0

                pixels[(y * img_size[0]) + x] = [r, g, b, a]

        pixels = [channel for pix in pixels for channel in pix]

        bimg.pixels = pixels

        btex = bpy.data.textures.new(tex_data.name, type='IMAGE')
        btex.image = bimg

        return btex

    def create_material(self, matData, texture):
        mat = bpy.data.materials.new(matData.name)
        #mat.diffuse_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)
        mat.use_nodes = True
        if texture is not None:
            node_tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
            node_tex.image = texture.image

            mat.node_tree.links.new(node_tex.outputs[0], mat.node_tree.nodes[0].inputs["Base Color"])

        return mat
