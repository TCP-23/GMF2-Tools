import math
import struct

from .gct0 import Gct0

RGB5A3_BLOCK_SIZE = 4
RGBA32_BLOCK_SIZE = 4
CMPR_BLOCK_SIZE = 8


def rgb565_to_RGB(colorData):
    r = (colorData >> 11) & 31
    g = (colorData >> 5) & 31
    b = colorData & 31

    rgb_data = tuple((int(r * 255 / 31), int(g * 255 / 63), int(b * 255 / 31), 255))

    return rgb_data


def rgba32_to_RGB(colorData):
    return None


def rgb5a3_to_RGB(colorData):
    check_bit = (colorData >> 15) & 1
    if check_bit == 0:
        a = (colorData >> 12) & 7
        r = (colorData >> 8) & 15
        g = (colorData >> 4) & 15
        b = colorData & 15

        rgb_data = tuple((int(r * 255 / 15), int(g * 255 / 15), int(b * 255 / 15), int(a * 255 / 7)))
    else:
        r = (colorData >> 10) & 31
        g = (colorData >> 5) & 31
        b = colorData & 31

        rgb_data = tuple((int(r * 255 / 31), int(g * 255 / 31), int(b * 255 / 31), 255))

    return rgb_data


def decompress_rgba32_texture(gct0_data):
    pass


def decompress_rgba32_block(compressed_block):
    pass


def decompress_rgb5a3_texture(gct0_data):
    total_block_count = (gct0_data.width / RGB5A3_BLOCK_SIZE) * (gct0_data.width / RGB5A3_BLOCK_SIZE)

    decompressed_blocks = []

    for block_id in range(math.ceil(total_block_count)):
        compressed_block = gct0_data.texture_data[(0+(32*block_id)):(32+(32*block_id))]
        decompressed_blocks.append(decompress_rgb5a3_block(compressed_block))

    decompressed_texture = map_pixels_to_grid(gct0_data.width, gct0_data.height, RGB5A3_BLOCK_SIZE, decompressed_blocks)

    return decompressed_texture


def decompress_rgb5a3_block(compressed_block):
    decompressed_block = []

    for pixel_id in range(RGB5A3_BLOCK_SIZE):
        compressed_pixel = struct.unpack('>Q', compressed_block[(0+(8*pixel_id)):(8+(8*pixel_id))])[0]
        decompressed_pixel = rgb5a3_to_RGB(compressed_pixel)
        decompressed_block.append(decompressed_pixel)

    return decompressed_block


def decompress_cmpr_texture(gct0_data):
    pass


def decompress_cmpr_block(compressed_block):
    pass


def map_pixels_to_grid(tex_x, tex_y, block_size, decompressed_blocks):
    #pixel_grid = [tuple((0, 0, 0, 0)) * tex_x] * tex_y
    pixel_2D = []

    for block in decompressed_blocks:
        for pixel in block:
            pixel_2D.append(pixel)

    return pixel_2D
