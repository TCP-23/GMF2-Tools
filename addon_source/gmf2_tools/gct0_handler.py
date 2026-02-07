import bpy
import struct
import math
from bpy.types import Operator
from .gct0 import Gct0

CMPR_BLOCK_SIZE = 8
CMPR_SUBBLOCK_SIZE = 4


# Convert a RGB565 color
def rgb565_to_RGB(colorData):
    r = (colorData >> 11) & 31
    g = (colorData >> 5) & 63
    b = colorData & 31

    rgb_data = tuple((int(r * 255 / 31), int(g * 255 / 63), int(b * 255 / 31), 255))

    return rgb_data


def rgb5a3_to_RGBA(colorData):
    hasAlpha = False if (colorData >> 15) == 1 else True
    if hasAlpha:
        a = (colorData >> 12) & 7
        r = (colorData >> 8) & 15
        g = (colorData >> 4) & 15
        b = colorData & 15

        rgba_data = tuple((int(r * 255 / 15), int(g * 255 / 15), int(b * 255 / 15), int(a * 255 / 7)))
    else:
        a = 255
        r = (colorData >> 10) & 31
        g = (colorData >> 5) & 31
        b = colorData & 31

        rgba_data = tuple((int(r * 255 / 31), int(g * 255 / 31), int(b * 255 / 31), a))
    
    return rgba_data


def pixel_block_mapper(unmapped_data, img_width, img_height, block_width, block_height):
    mapped_data = []

    width_in_blocks = int(math.ceil(img_width / block_width))
    width_remainder = img_width % block_width

    height_in_blocks = int(math.ceil(img_height / block_height))
    height_remainder = img_height % block_height

    w_block_iterator = 1
    h_block_iterator = 1
    block_row_iterator = 1

    # NONFUNCTIONAL FOR NOW
    if width_in_blocks > 1:
        block_loop_w = block_width
    else:
        block_loop_w = width_remainder
    if height_in_blocks > 1:
        block_loop_h = block_height
    else:
        block_loop_h = height_remainder

    pixel = 1
    for i in range(1, int((len(unmapped_data) / 4) + 1)):
        index = (pixel - 1) + ((w_block_iterator - 1) * (block_width * block_height)) + ((block_width * block_height) * ((h_block_iterator - 1) * width_in_blocks))
        mapped_data.extend([
            unmapped_data[(index * 4)],  # red
            unmapped_data[(index * 4) + 1],  # green
            unmapped_data[(index * 4) + 2],  # blue
            unmapped_data[(index * 4) + 3]  # alpha
        ])

        if pixel % block_width == 0:
            if w_block_iterator % width_in_blocks == 0:
                if block_row_iterator == block_height:
                    h_block_iterator += 1
                    block_row_iterator = 1
                else:
                    block_row_iterator += 1
                w_block_iterator = 1
            else:
                w_block_iterator += 1
            pixel = 1 + ((block_row_iterator - 1) * (block_width))
        else:
            pixel += 1
        
    #return mapped_data
    return mirror_texture_y(mapped_data, img_width, img_height)


# Mirrors the provided pixel data to match Blender's dimension grid
def mirror_texture_y(unmirrored_data, img_width, img_height):
    x_iter = 0
    y_iter = 0

    for pix_idx in range((img_width * img_height) // 2):
        index_top = (y_iter * img_width + x_iter) * 4
        index_bottom = ((img_height - y_iter - 1) * img_width + x_iter) * 4

        x_iter += 1
        if (x_iter % img_width == 0):
            y_iter += 1
            x_iter = 0

        unmirrored_data[index_top:index_top + 4], unmirrored_data[index_bottom:index_bottom + 4] = \
            unmirrored_data[index_bottom:index_bottom + 4], unmirrored_data[index_top:index_top + 4]
    
    return unmirrored_data


def rgb5a3_texture(gct0_data):
    color_data = []

    expected_data_len = gct0_data.width * gct0_data.height
    pixel_data_len = int(len(gct0_data.texture_data) / 2)
    if (pixel_data_len != expected_data_len):
        print(f"Texture data length mismatch! Expected length: {expected_data_len}. Actual length: {pixel_data_len}.")
        print(f"Skipping texture [TEX_NAME]")
        return "ERROR_FLAG"

    head = 0
    for i in range(0, pixel_data_len):
        pix_data_5a3 = struct.unpack('>H', gct0_data.texture_data[head:head+2])[0]
        head += 2

        pix_data_rgb = rgb5a3_to_RGBA(pix_data_5a3)

        color_data.extend([
            pix_data_rgb[0],
            pix_data_rgb[1],
            pix_data_rgb[2],
            pix_data_rgb[3]
        ])

    return pixel_block_mapper(color_data, gct0_data.width, gct0_data.height, 4, 4)


def rgba32_texture(gct0_data):
    decompressed_data = [0] * gct0_data.width * gct0_data.height * 4

    red = []
    green = []
    blue = []
    alpha = []

    expected_data_len = gct0_data.width * gct0_data.height
    pixel_data_len = int(len(gct0_data.texture_data))
    if (pixel_data_len != expected_data_len):
        print(f"Texture data length mismatch! Expected length: {expected_data_len}. Actual length: {pixel_data_len}.")
        print(f"Skipping texture [TEX_NAME]")
        return "ERROR_FLAG"

    row = 0
    for i in range(pixel_data_len):
        # Every 16 bytes in a block, update the row
        if i % 16 == 0:
            row += 1
        # If the row is 5, we have finished a block and need to start on the next block
        if row == 5:
            row = 1

        # Unpack the channel data into an integer
        col_chan = int(struct.unpack('>B', gct0_data.texture_data[i:i+1])[0])

        # Determine which color channel is currently stored in i
        if row == 1 or row == 2:
            if i % 2 == 0:  # alpha
                alpha.append(col_chan)
            else:  # red
                red.append(col_chan)
        else:
            if i % 2 == 0:  # green
                green.append(col_chan)
            else:  # blue
                blue.append(col_chan)
    
    head = 0
    for i in range(int(len(red))):  # all channels are the same length, so it doesn't matter which one is used here
        decompressed_data[head] = red[i]
        decompressed_data[head+1] = green[i]
        decompressed_data[head+2] = blue[i]
        decompressed_data[head+3] = alpha[i]

        head += 4

    return pixel_block_mapper(decompressed_data, gct0_data.width, gct0_data.height, 4, 4)


def cmpr_texture(gct0_data):
    decompressed_data = [0] * gct0_data.width * gct0_data.height * 4


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

    return mirror_texture_y(decompressed_data, tex_width, tex_height)


def load_rgb5a3_texture(gct0_data):
    pixel_list = []
    texture_data = rgb5a3_texture(gct0_data)
    if (texture_data == "ERROR_FLAG"):
        return "ERROR_FLAG"

    for pix in texture_data:
        pixel_list.append(pix / 255)

    return pixel_list


def load_rgba32_texture(gct0_data):
    pixel_list = []
    texture_data = rgba32_texture(gct0_data)
    if (texture_data == "ERROR_FLAG"):
        return "ERROR_FLAG"

    for pix in texture_data:
        pixel_list.append(pix / 255)

    return pixel_list


# Returns a list of pixels using provided CMPR texture data
def load_cmpr_texture(gct0_data):
    pixel_list = []
    texture_data = cmpr_texture_testing(gct0_data)
    if (texture_data == "ERROR_FLAG"):
        return "ERROR_FLAG"

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
                pixels = load_rgba32_texture(tex_data.gct0_texture)
            case Gct0.TextureEncoding.cmpr:
                pixels = load_cmpr_texture(tex_data.gct0_texture)
            case _:
                print("Texture format not supported (yet)")
                pass

        if pixels == "ERROR_FLAG":
            return None
        
        try:
            #bimg.pixels = pixels
            bimg.pixels.foreach_set(pixels)
            bimg.update()
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
            case Gct0.TextureEncoding.rgba32:
                pixels = load_rgba32_texture(gct0_data)
            case Gct0.TextureEncoding.cmpr:
                pixels = load_cmpr_texture(gct0_data)
            case _:
                print("Texture format not supported (yet)")
                pass

        bimg.pixels.foreach_set(pixels)
        bimg.update()

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
