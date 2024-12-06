import bpy
import struct
from bpy.types import Operator
from .gct0 import Gct0


def rgb565_to_RGB(colorData):
    r = (colorData >> 11) & 31  # Extract 5 bits for red
    g = (colorData >> 5) & 63  # Extract 6 bits for green
    b = colorData & 31  # Extract 5 bits for blue

    # Convert to 8-bit RGB (scale 5 bits to 8 bits)
    rgb_data = tuple((int(r * 255 / 31), int(g * 255 / 63), int(b * 255 / 31), 255))

    return rgb_data


def decompress_dxt1_block(compressed_block):
    # 1 block = 8 bytes, 64 bits, 16 pixels

    # unpack the two color values
    color0_565, color1_565 = struct.unpack("<HH", compressed_block[:4])

    # extract RBG from the colors
    color0_rgb = rgb565_to_RGB(color0_565)
    color1_rgb = rgb565_to_RGB(color1_565)

    # compute the interpolated colors
    # color 2: 50% mix of color0 and color1
    # color 3: 25% mix of color0 and 75% mix of color1
    color2_rgb = tuple((color0_rgb[i] + color1_rgb[i]) // 2 for i in range(3))
    color3_rgb = tuple((color0_rgb[i] * 3 + color1_rgb[i]) // 4 for i in range(3))

    # extract the color indices (2 bits per pixel)
    indices = []
    for i in range(4):
        idx_byte = compressed_block[4 + i]
        for j in range(4):
            # Use bit masking to extract the 2-bit index for each pixel
            indices.append((idx_byte >> (6 - 2 * j)) & 3)

    # map each index to the corresponding color
    color_map = [color0_rgb, color1_rgb, color2_rgb, color3_rgb]

    # decompress the 16 pixels in the block using the 2-bit indices
    pixels = [color_map[idx] for idx in indices]

    return pixels


def decompress_dxt1_texture(tex_data):
    decompressed_data = []
    for i in range(0, (tex_data.len_data - tex_data.gct0_texture.data_offset), 8):
        decompressed_block = decompress_dxt1_block(tex_data.gct0_texture.texture_data[i:i+8])
        decompressed_data.append(decompressed_block)

    pixel_list = []
    for i, block in enumerate(decompressed_data):
        for j, pix in enumerate(block):
            pixel_list.append(pix[0] / 255)
            pixel_list.append(pix[1] / 255)
            pixel_list.append(pix[2] / 255)
            pixel_list.append(1.0)

    return pixel_list


def decompress_cmpr_block(compressed_block):
    pass


def decompress_cmpr_subblock(compressed_subblock):
    pass


def get_cmpr_color_map():
    pass


def decompress_cmpr_texture(tex_data):
    # constants for block dimensions (8x8 blocks, each containing 4x4 sub-blocks)
    BLOCK_W = 8
    BLOCK_H = 8
    SUBBLOCK_W = 4
    SUBBLOCK_H = 4

    # get texture width and texture height
    tex_width, tex_height = tex_data.gct0_texture.width, tex_data.gct0_texture.height

    decompressed_data = [0] * tex_width * tex_height * 4

    # pointer to the current position in the texture data
    head = 0

    # iterate over the texture in 8x8 blocks
    for y in range(0, tex_height, BLOCK_H):
        for x in range(0, tex_width, BLOCK_W):

            # iterate over the 4x4 sub-blocks within each 8x8 block
            for sub_y in range(0, BLOCK_H, SUBBLOCK_H):
                for sub_x in range(0, BLOCK_W, SUBBLOCK_W):

                    # read the two color values (565 format) from the texture data
                    color0_565, color1_565 = struct.unpack('>HH', tex_data.gct0_texture.texture_data[head:head+4])
                    head += 4

                    # convert the 565 color values to RGB format
                    color0_rgb = rgb565_to_RGB(color0_565)
                    color1_rgb = rgb565_to_RGB(color1_565)

                    # initialize default values for the other two colors
                    color2_rgb = [0, 0, 0, 0]
                    color3_rgb = [0, 0, 0, 0]

                    # determine the third and fourth colors based on the first two colors
                    if color0_565 > color1_565:
                        for i in range(4):
                            color2_rgb[i] = int((2 * color0_rgb[i] + color1_rgb[i]) / 3)
                            color3_rgb[i] = int((2 * color1_rgb[i] + color0_rgb[i]) / 3)
                    else:
                        for i in range(4):
                            color2_rgb[i] = int((color0_rgb[i] + color1_rgb[i]) / 2)
                        color3_rgb = [0, 0, 0, 0]

                    # create a color map for the four possible colors
                    color_map = [color0_rgb, color1_rgb, color2_rgb, color3_rgb]

                    # process each 4x4 sub-block (each block contains 4x4 pixels)
                    for sub_y_offset in range(SUBBLOCK_H):
                        # read the 1-byte pattern that defines pixel colors
                        color_pattern = tex_data.gct0_texture.texture_data[head]
                        head += 1

                        # iterate over the 4x4 pixel positions in the sub-block
                        for sub_x_offset in range(SUBBLOCK_W):
                            # calculate the pixel position in the decompressed data
                            pixel_y = y + sub_y + sub_y_offset
                            pixel_x = x + sub_x + sub_x_offset

                            # only write to decompressed data if the pixel is within bounds
                            if pixel_y < tex_height and pixel_x < tex_width:
                                # find the index in the decompressed data array
                                index = (pixel_y * tex_width + pixel_x) * 4

                                # use the color map based on the 2-bit index from the pattern
                                decompressed_data[index:index+4] = color_map[(color_pattern >> (6 - (sub_x_offset * 2))) & 3]

    # flip the texture vertically
    # iterate over the rows and reverse their pixel data
    for y in range(tex_height // 2):
        for x in range(tex_width):
            # calculate the index for the current pixel and its vertically flipped counterpart
            index_top = (y * tex_width + x) * 4
            index_bottom = ((tex_height - y - 1) * tex_width + x) * 4

            # swap the pixels
            decompressed_data[index_top:index_top+4], decompressed_data[index_bottom:index_bottom+4] = \
                decompressed_data[index_bottom:index_bottom+4], decompressed_data[index_top:index_top+4]

    return decompressed_data


def load_cmpr_texture(tex_data):
    pixel_list = []

    texture_data = decompress_cmpr_texture(tex_data)
    for pix in texture_data:
        pixel_list.append(pix / 255)

    return pixel_list


class GCTTextureHandler(Operator):
    #EMPTY_TEXTURE = r"b'\x90\xc4\x88\xe1\xaf\xaf\xff\xff[9] : --- No File ---\x00\x00\x00'"

    tex_list = {}
    mat_list = {}

    def import_textures(self, context, textures):
        for i, tex in enumerate(textures):
            if "No File" not in str(tex.gct0_texture.texture_data) and tex.gct0_texture.encoding == Gct0.TextureEncoding.cmpr:
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
            pixels.append([0, 0, 0, 1])

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
        pixels = []

        match tex_data.gct0_texture.encoding:
            case Gct0.TextureEncoding.rgb5a3:
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.rgba32:
                pixels = [[0, 0, 0, 0]] * img_size[0] * img_size[1]
                pass
            case Gct0.TextureEncoding.cmpr:
                pixels = load_cmpr_texture(tex_data)
            case _:
                print("Texture format not supported (yet)")
                pass

        bimg.pixels = pixels

        btex = bpy.data.textures.new(tex_data.name, type='IMAGE')
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
