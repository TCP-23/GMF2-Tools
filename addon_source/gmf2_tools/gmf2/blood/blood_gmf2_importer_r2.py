import bpy
import bmesh
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from .gmf2b import Gmf2b
from .blood_tex import BloodTex
from .blood_object_info import *
from ..gct0.gct0_handler import GCTTextureHandler

SCALE_MULTIPLIER = 0.1


class GMF2BModelImporter(Operator):
    bl_idname = "gm2_importer.b_data2"
    bl_label = "Import GMF2B Model"

    btex_list = {}
    bmat_list = {}
    bobj_list = {}

    def load_file_data(self, context, filepath):
        GMF2BModelImporter.btex_list.clear()
        GMF2BModelImporter.bmat_list.clear()
        GMF2BModelImporter.bobj_list.clear()

        gm2 = Gmf2b.from_file(filepath)

        minfo_list = create_minfo_from_wobjects(gm2.world_objects)

        if self.import_mats:
            GMF2BModelImporter.import_textures(self, gm2.textures)
            GMF2BModelImporter.import_materials(self, gm2.materials)

        GMF2BModelImporter.import_objects(self, context, minfo_list)

        GMF2BModelImporter.cleanup(self, context)

        return {'FINISHED'}
    
    def import_textures(self, textures: list[Gmf2b.Texture]):
        for tex in textures:
            new_btex = GMF2BModelImporter.create_texture(self, tex)
            GMF2BModelImporter.btex_list[tex.offset] = new_btex

    def create_texture(self, tex_info: Gmf2b.Texture):
        palette_data = bytearray(tex_info.texture_data.palette_data)
        if tex_info.texture_data.csm_flags == 0x08:
            new_pal = bytearray(0x400)
            for i in range(256):
                swapped_i = (i & ~0x18) | ((i & 0x08) << 1) | ((i & 0x10) >> 1)
                new_pal[i * 4 : i * 4 + 4] = palette_data[swapped_i * 4 : swapped_i * 4 + 4]
            palette_data = new_pal

        blender_pixels = [0.0] * (tex_info.texture_data.pixel_size * 4)
        for y in range(tex_info.texture_data.img_height):
            for x in range(tex_info.texture_data.img_width):
                px_idx = y * tex_info.texture_data.img_width + x
                pal_idx = tex_info.texture_data.pixels_data[px_idx]
                out_idx = ((tex_info.texture_data.img_height - 1 - y) * tex_info.texture_data.img_width + x) * 4
                blender_pixels[out_idx] = palette_data[pal_idx * 4] / 255.0
                blender_pixels[out_idx + 1] = palette_data[pal_idx * 4 + 1] / 255.0
                blender_pixels[out_idx + 2] = palette_data[pal_idx * 4 + 2] / 255.0
                blender_pixels[out_idx + 3] = 1.0

        tex_name = f"{tex_info.name}_{tex_info.offset}"
        bimg = bpy.data.images.new(tex_name, tex_info.texture_data.img_width, tex_info.texture_data.img_height, alpha=True)
        bimg.pixels = blender_pixels

        btex = bpy.data.textures.new(tex_name, type='IMAGE')
        btex.image = bimg
        btex.use_fake_user = True

        return btex
    
    def import_materials(self, materials: list[Gmf2b.Material]):
        for mat in materials:
            new_bmat = GMF2BModelImporter.create_material(self, mat)
            GMF2BModelImporter.bmat_list[mat.offset] = new_bmat
    
    def create_material(self, mat_info: Gmf2b.Material):
        bmat = bpy.data.materials.new(mat_info.name)
        bmat.use_nodes = True
        bmat.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1
        if mat_info.data.off_main_tex != 0:
            btex = GMF2BModelImporter.btex_list[mat_info.data.off_main_tex]
        else:
            btex = GCTTextureHandler.get_fallback_texture(self)
        node_tex = bmat.node_tree.nodes.new('ShaderNodeTexImage')
        node_tex.image = btex.image
        bmat.node_tree.links.new(node_tex.outputs[0], bmat.node_tree.nodes[0].inputs["Base Color"])
        bmat.node_tree.links.new(node_tex.outputs["Alpha"], bmat.node_tree.nodes[0].inputs["Alpha"])
        
        return bmat

    def import_objects(self, context, objects: list[BloodModelObjectInfo]):
        pass

    def cleanup(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
