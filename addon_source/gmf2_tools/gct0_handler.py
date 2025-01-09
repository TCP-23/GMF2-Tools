import bpy
import struct
from bpy.types import Operator
from .gct0 import Gct0

CMPR_BLOCK_SIZE = 8
CMPR_SUBBLOCK_SIZE = 4


def rgb565_to_RGB(colorData):
    r = (colorData >> 11) & 31
    g = (colorData >> 5) & 63
    b = colorData & 31

    rgb_data = tuple((int(r * 255 / 31), int(g * 255 / 63), int(b * 255 / 31), 255))

    return rgb_data


def rgba32_to_RGB(colorData):
    return None


def decompress_rgb5a3_texture(gct0_data):
    pass


"""def decompress_rgba32_texture(gct0_data):
    BLOCK_W = 4
    BLOCK_H = 4

    tex_width, tex_height = gct0_data.width, gct0_data.height
    decompressed_texture = [0] * tex_width * tex_height * 4

    head = 0

    for y in range(0, tex_height, BLOCK_H):
        for x in range(0, tex_width, BLOCK_W):
            for y2 in range(BLOCK_H):
                for x2 in range(BLOCK_W):
                    idx = (((y + y2) * tex_width) + (x + x2)) * 4
                    decompressed_texture[idx+0] = gct0_data.texture_data[head+33]
                    decompressed_texture[idx+1] = gct0_data.texture_data[head+32]
                    decompressed_texture[idx+2] = gct0_data.texture_data[head+1]
                    decompressed_texture[idx+3] = gct0_data.texture_data[head]
                    head += 2
            head += 32

    for y in range(tex_height // 2):
        for x in range(tex_width):
            index_top = (y * tex_width + x) * 4
            index_bottom = ((tex_height - y - 1) * tex_width + x) * 4

            # swap the pixels
            decompressed_texture[index_top:index_top+4], decompressed_texture[index_bottom:index_bottom+4] = \
                decompressed_texture[index_bottom:index_bottom+4], decompressed_texture[index_top:index_top+4]

    return decompressed_texture"""


def decompress_cmpr_texture(gct0_data):
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
                    color0_565, color1_565 = struct.unpack('>HH', gct0_data.texture_data[head:head+4])
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

                                decompressed_data[index:index+4] = color_map[(color_pattern >> (6 - (sub_x_offset * 2))) & 3]

    for y in range(tex_height // 2):
        for x in range(tex_width):
            index_top = (y * tex_width + x) * 4
            index_bottom = ((tex_height - y - 1) * tex_width + x) * 4

            decompressed_data[index_top:index_top+4], decompressed_data[index_bottom:index_bottom+4] = \
                decompressed_data[index_bottom:index_bottom+4], decompressed_data[index_top:index_top+4]

    return decompressed_data


"""def decompress_cmpr_block(compressed_block):
    decompressed_block = []

    head = 0
    for subblock in range(0, CMPR_BLOCK_SIZE * CMPR_BLOCK_SIZE, CMPR_SUBBLOCK_SIZE * CMPR_SUBBLOCK_SIZE):
        compressed_subblock = compressed_block[head:head+8]
        decompressed_subblock = decompress_cmpr_subblock(compressed_subblock)
        decompressed_block.append(decompressed_subblock)
        head += 8

    return decompressed_block


def decompress_cmpr_subblock(compressed_subblock):
    decompressed_subblock = []

    color0_565, color1_565 = struct.unpack('>HH', compressed_subblock[0:4])
    color_map = [rgb565_to_RGB(color0_565), rgb565_to_RGB(color1_565), [0, 0, 0, 0], [0, 0, 0, 0]]

    if color0_565 > color1_565:
        for i in range(4):
            color_map[2][i] = int((2 * color_map[0][i] + color_map[1][i]) / 3)
            color_map[3][i] = int((2 * color_map[1][i] + color_map[0][i]) / 3)
    else:
        for i in range(4):
            color_map[2][i] = int((color_map[0][i] + color_map[1][i]) / 2)

    head = 0
    for pixel_column in range(0, CMPR_SUBBLOCK_SIZE):
        color_pattern = compressed_subblock[pixel_column]

        for pixel_row in range(0, CMPR_SUBBLOCK_SIZE):
            decompressed_subblock[head:head+4] = color_map[(color_pattern >> (6 - (pixel_row * 2))) & 3]
            head += 4

    return decompressed_subblock"""


"""def decompress_cmpr_texture(tex_data):
    tex_width, tex_height = tex_data.gct0_texture.width, tex_data.gct0_texture.height
    decompressed_texture = [0] * tex_width * tex_height * 4
    decompressed_blocks = []

    head = 0
    for block in range(0, tex_height * tex_width, CMPR_BLOCK_SIZE * CMPR_BLOCK_SIZE):
        compressed_block = tex_data.gct0_texture.texture_data[head:head+32]
        decompressed_block = decompress_cmpr_block(compressed_block)
        decompressed_blocks.append(decompressed_block)
        head += 32

    for y in range(tex_height // 2):
        for x in range(tex_width):
            index_top = (y * tex_width + x) * 4
            index_bottom = ((tex_height - y - 1) * tex_width + x) * 4

            decompressed_texture[index_top:index_top+4], decompressed_texture[index_bottom:index_bottom+4] = \
                decompressed_texture[index_bottom:index_bottom+4], decompressed_texture[index_top:index_top+4]

    return decompressed_texture"""


def load_cmpr_texture(gct0_data):
    pixel_list = []

    texture_data = decompress_cmpr_texture(gct0_data)
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
            if tex.gct0_texture.encoding == Gct0.TextureEncoding.cmpr:
                if "No File" not in str(tex.gct0_texture.texture_data):
                    new_btex = GCTTextureHandler.create_internal_texture(self, tex)
                else:
                    new_btex = GCTTextureHandler.create_empty_texture(self, tex.name)

            if new_btex is None:
                new_btex = GCTTextureHandler.get_fallback_texture(self)

            GCTTextureHandler.tex_list[tex.offset] = new_btex

    def import_materials(self, context, materials):
        for i, mat in enumerate(materials):
            if mat.data.off_texture != 0:
                new_mat = GCTTextureHandler.create_material(self, mat, GCTTextureHandler.tex_list[mat.data.off_texture])
            else:
                new_mat = GCTTextureHandler.create_material(self, mat, GCTTextureHandler.get_fallback_texture(self))
            GCTTextureHandler.mat_list[mat.offset] = new_mat

    def export_textures(self, context):
        pass

    def create_empty_texture(self, tex_name):
        default_color_1 = [0.945, 0.851, 0.753, 1]
        default_color_2 = [0.356, 0.159, 0.102, 1]
        color_picker = False

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

        pixels = [channel for pix in pixels for channel in pix]
        bimg.pixels = pixels

        btex = bpy.data.textures.new(tex_name, type='IMAGE')
        btex.image = bimg

        return btex

    def get_fallback_texture(self):
        if not bpy.data.textures.get("FALLBACK_TEX"):
            btex = GCTTextureHandler.create_empty_texture(self, "FALLBACK_TEX")
        else:
            btex = bpy.data.textures.get("FALLBACK_TEX")

        return btex

    def create_internal_texture(self, tex_data):
        img_size = tex_data.gct0_texture.width, tex_data.gct0_texture.height
        bimg = bpy.data.images.new(tex_data.name, width=img_size[0], height=img_size[1])
        pixels = []

        match tex_data.gct0_texture.encoding:
            case Gct0.TextureEncoding.rgb5a3:
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.rgba32:
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.cmpr:
                pixels = load_cmpr_texture(tex_data.gct0_texture)
            case _:
                print("Texture format not supported (yet)")
                pass

        bimg.pixels = pixels

        btex = bpy.data.textures.new(tex_data.name, type='IMAGE')
        btex.image = bimg

        return btex

    def create_texture_from_external(self,  tex_name, gct0_data):
        img_size = gct0_data.width, gct0_data.height
        bimg = bpy.data.images.get(tex_name)
        bimg.scale(img_size[0], img_size[1])

        pixels = []

        match gct0_data.encoding:
            case Gct0.TextureEncoding.rgb5a3:
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.rgb5a3:
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.cmpr:
                pixels = load_cmpr_texture(gct0_data)
            case _:
                print("Texture format not supported (yet)")
                pass

        bimg.pixels = pixels
        btex = bpy.data.textures.get(tex_name)
        btex.image = bimg

        return btex

    def create_material(self, matData, texture):
        mat = bpy.data.materials.new(matData.name)
        #mat.diffuse_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1
        if texture is not None:
            node_tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
            node_tex.image = texture.image

            mat.node_tree.links.new(node_tex.outputs[0], mat.node_tree.nodes[0].inputs["Base Color"])

        return mat
