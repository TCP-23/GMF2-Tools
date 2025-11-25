import bpy
import struct
from bpy.types import Operator
from .gct0 import Gct0
from .gct0_decompress import *

CMPR_BLOCK_SIZE = 8
CMPR_SUBBLOCK_SIZE = 4


# Convert a RGB565 color
def rgb565_to_RGB(colorData):
    r = (colorData >> 11) & 31
    g = (colorData >> 5) & 63
    b = colorData & 31

    rgb_data = tuple((int(r * 255 / 31), int(g * 255 / 63), int(b * 255 / 31), 255))

    return rgb_data


def cmpr_texture_testing(gct0_data):
    BLOCK_W = 8
    BLOCK_H = 8
    SUBBLOCK_W = 4
    SUBBLOCK_H = 4

    tex_width, tex_height = gct0_data.width, gct0_data.height

    decompressed_data = [0] * tex_width * tex_height * 4

    head = 0

    for y in range(0, tex_height, BLOCK_H):
        for x in range(0, tex_width, BLOCK_W):
            for sub_y in range(0, BLOCK_H, SUBBLOCK_H):
                for sub_x in range(0, BLOCK_W, SUBBLOCK_W):
                    color0_565, color1_565 = struct.unpack('>HH', gct0_data.texture_data[head:head + 4])
                    head += 4

                    color0_rgb = rgb565_to_RGB(color0_565)
                    color1_rgb = rgb565_to_RGB(color1_565)

                    color2_rgb = [0, 0, 0, 0]
                    color3_rgb = [0, 0, 0, 0]

                    if color0_565 > color1_565:
                        for i in range(4):
                            color2_rgb[i] = int((2 * color0_rgb[i] + color1_rgb[i]) / 3)
                            color3_rgb[i] = int((2 * color1_rgb[i] + color0_rgb[i]) / 3)
                    else:
                        for i in range(4):
                            color2_rgb[i] = int((color0_rgb[i] + color1_rgb[i]) / 2)
                        color3_rgb = [0, 0, 0, 0]

                    color_map = [color0_rgb, color1_rgb, color2_rgb, color3_rgb]

                    for sub_y_offset in range(SUBBLOCK_H):
                        color_pattern = gct0_data.texture_data[head]
                        head += 1

                        for sub_x_offset in range(SUBBLOCK_W):
                            pixel_y = y + sub_y + sub_y_offset
                            pixel_x = x + sub_x + sub_x_offset

                            if pixel_y < tex_height and pixel_x < tex_width:
                                index = (pixel_y * tex_width + pixel_x) * 4

                                decompressed_data[index:index + 4] = color_map[
                                    (color_pattern >> (6 - (sub_x_offset * 2))) & 3]

    for y in range(tex_height // 2):
        for x in range(tex_width):
            index_top = (y * tex_width + x) * 4
            index_bottom = ((tex_height - y - 1) * tex_width + x) * 4

            decompressed_data[index_top:index_top + 4], decompressed_data[index_bottom:index_bottom + 4] = \
                decompressed_data[index_bottom:index_bottom + 4], decompressed_data[index_top:index_top + 4]

    return decompressed_data


# Returns a list of pixels using provided RGB5A3 texture data
def load_rgb5a3_texture(gct0_data):
    pixel_list = []

    texture_data = decompress_rgb5a3_texture(gct0_data)
    for pix in texture_data:
        try:
            pixel_list.append(pix[0][0] / 255)
            pixel_list.append(pix[0][1] / 255)
            pixel_list.append(pix[0][2] / 255)
            pixel_list.append(pix[0][3] / 255)

            pixel_list.append(pix[0][0] / 255)
            pixel_list.append(pix[0][1] / 255)
            pixel_list.append(pix[0][2] / 255)
            pixel_list.append(pix[0][3] / 255)

            pixel_list.append(pix[0][0] / 255)
            pixel_list.append(pix[0][1] / 255)
            pixel_list.append(pix[0][2] / 255)
            pixel_list.append(pix[0][3] / 255)

            pixel_list.append(pix[0][0] / 255)
            pixel_list.append(pix[0][1] / 255)
            pixel_list.append(pix[0][2] / 255)
            pixel_list.append(pix[0][3] / 255)
        except TypeError:
            print(pix[0])
            print(pix[1])
            print(pix[2])
            print(pix[3])
            return None

    return pixel_list


# Returns a list of pixels using provided CMPR texture data
def load_cmpr_texture(gct0_data):
    pixel_list = []

    texture_data = cmpr_texture_testing(gct0_data)
    for pix in texture_data:
        pixel_list.append(pix / 255)

    return pixel_list


class GCTTextureHandler(Operator):
    #EMPTY_TEXTURE = r"b'\x90\xc4\x88\xe1\xaf\xaf\xff\xff[9] : --- No File ---\x00\x00\x00'"

    tex_list = {}
    mat_list = {}

    def import_textures(self, context, textures):
        for i, tex in enumerate(textures):
            new_btex = None
            if tex.gct0_texture.encoding != Gct0.TextureEncoding.rgba32:
                # Check if the texture data is embedded in the model file
                if "No File" not in str(tex.gct0_texture.texture_data):
                    # If it is embedded, create a new Blender texture using the data
                    new_btex = GCTTextureHandler.create_internal_texture(self, tex)
                else:
                    # If it is not embedded, create a placeholder texture in its place
                    new_btex = GCTTextureHandler.create_empty_texture(self, tex.name)

            # If the texture doesn't exist, replace it with the fallback texture
            if new_btex is None:
                new_btex = GCTTextureHandler.get_fallback_texture(self)

            # Add the texture to the texture list
            GCTTextureHandler.tex_list[tex.offset] = new_btex

    def import_materials(self, context, materials):
        for i, mat in enumerate(materials):
            # Check if the material data has a valid texture
            if mat.data.off_main_tex != 0:
                new_mat = GCTTextureHandler.create_material(self, mat, GCTTextureHandler.tex_list[mat.data.off_main_tex])
            else:
                # Create a material using a fallback texture
                new_mat = GCTTextureHandler.create_material(self, mat, GCTTextureHandler.get_fallback_texture(self))

            # Add the new material to the material list
            GCTTextureHandler.mat_list[mat.offset] = new_mat

    # Unused
    def export_textures(self, context):
        pass

    # Creates a default texture
    def create_empty_texture(self, tex_name):
        default_color_1 = [0.945, 0.851, 0.753, 1]
        default_color_2 = [0.356, 0.159, 0.102, 1]
        color_picker = False

        # Create a new image and set its width and height
        bimg = bpy.data.images.new(tex_name, 32, 32)
        pixels = []
        for i in range(0, 32):
            if color_picker is False:
                for j in range(0, 16):
                    pixels.append(default_color_1)
                    pixels.append(default_color_2)
            else:
                for j in range(0, 16):
                    pixels.append(default_color_2)
                    pixels.append(default_color_1)
            color_picker = not color_picker

        # Crush the list of pixels so we can use it to make a Blender texture
        pixels = [channel for pix in pixels for channel in pix]
        bimg.pixels = pixels

        # Create a Blender texture and apply the image
        btex = bpy.data.textures.new(tex_name, type='IMAGE')
        btex.image = bimg

        return btex

    # Returns the default fallback texture
    def get_fallback_texture(self):
        # Check if the fallback texture has already been created
        if not bpy.data.textures.get("FALLBACK_TEX"): # If it doesn't exist, create it
            btex = GCTTextureHandler.create_empty_texture(self, "FALLBACK_TEX")
        else: # If it has been created, just get it
            btex = bpy.data.textures.get("FALLBACK_TEX")

        return btex

    def create_internal_texture(self, tex_data):
        img_size = tex_data.gct0_texture.width, tex_data.gct0_texture.height

        # Create a Blender image and set its width and height
        bimg = bpy.data.images.new(tex_data.name, width=img_size[0], height=img_size[1])

        pixels = []

        match tex_data.gct0_texture.encoding:
            case Gct0.TextureEncoding.rgb5a3:
                pixels = load_rgb5a3_texture(tex_data.gct0_texture)
            case Gct0.TextureEncoding.rgba32:
                # This encoding is currently not supported, so set all the pixels to pure black
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.cmpr:
                pixels = load_cmpr_texture(tex_data.gct0_texture)
            case _:
                print("Texture format not supported (yet)")
                pass

        try:
            bimg.pixels = pixels
        except:
            print(tex_data.name)
            print(len(bimg.pixels))
            print(len(pixels))

        # Create a Blender texture and apply the image
        btex = bpy.data.textures.new(tex_data.name, type='IMAGE')
        btex.image = bimg
        btex.id_data["GCT0 Encode"] = str(tex_data.gct0_texture.encoding).replace("TextureEncoding.", "")
        btex.use_fake_user = True

        return btex

    def create_texture_from_external(self,  tex_name, gct0_data):
        img_size = gct0_data.width, gct0_data.height

        # Get the placeholder image we created earlier and set its width and height
        bimg = bpy.data.images.get(tex_name)
        bimg.scale(img_size[0], img_size[1])

        pixels = []

        match gct0_data.encoding:
            case Gct0.TextureEncoding.rgb5a3:
                pixels = load_rgb5a3_texture(gct0_data)
            case Gct0.TextureEncoding.rgb5a3:
                # This encoding is currently not supported, so set all the pixels to pure black
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.cmpr:
                pixels = load_cmpr_texture(gct0_data)
            case _:
                print("Texture format not supported (yet)")
                pass

        bimg.pixels = pixels

        # Create a Blender texture and apply the image
        btex = bpy.data.textures.get(tex_name)
        btex.image = bimg

        return btex

    def create_material(self, matData, texture):
        # Create a new material, and set its roughness to 1
        mat = bpy.data.materials.new(matData.name)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1

        # Check if we have supplied a texture
        if texture is not None:
            # Add a new texture node to the material
            node_tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
            node_tex.image = texture.image

            # Link the color and alpha of the texture to the material
            mat.node_tree.links.new(node_tex.outputs[0], mat.node_tree.nodes[0].inputs["Base Color"])
            mat.node_tree.links.new(node_tex.outputs["Alpha"], mat.node_tree.nodes[0].inputs["Alpha"])

        return mat
