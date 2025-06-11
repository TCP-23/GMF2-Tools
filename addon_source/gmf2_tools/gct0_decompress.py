# THIS SCRIPT IS FOR TESTING

import math
import struct

from .gct0 import Gct0

RGB5A3_BLOCK_SIZE = 4
RGBA32_BLOCK_SIZE = 4
CMPR_BLOCK_SIZE = 8
CMPR_SUBBLOCK_SIZE = 4


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
    total_block_count = (gct0_data.width / RGBA32_BLOCK_SIZE) * (gct0_data.height / RGBA32_BLOCK_SIZE)
    decompressed_blocks = []

    for block_id in range(math.ceil(total_block_count)):
        compressed_block = gct0_data.texture_data[(0+(64*block_id)):(64+(64*block_id))]
        decompressed_blocks.append(decompress_rgba32_block(compressed_block))

    decompressed_texture = map_pixels_to_grid(gct0_data.width, gct0_data.height, RGBA32_BLOCK_SIZE, decompressed_blocks)

    return decompressed_texture


def decompress_rgba32_block(compressed_block):
    decompressed_block = []

    for pixel_id in range(RGBA32_BLOCK_SIZE):
        compressed_pixel = struct.unpack('>Q', compressed_block[(0+(16*pixel_id)):(16+(16*pixel_id))])[0]
        decompressed_pixel = rgba32_to_RGB(compressed_pixel)
        decompressed_block.append(decompressed_pixel)

    return decompressed_block


def decompress_rgb5a3_texture(gct0_data):
    total_block_count = (gct0_data.width / RGB5A3_BLOCK_SIZE) * (gct0_data.height / RGB5A3_BLOCK_SIZE)
    decompressed_blocks = []

    print(f"Read data length: {len(gct0_data.texture_data)}")
    print(f"Total data length: {32*total_block_count}")

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
    total_block_count = (gct0_data.width / CMPR_BLOCK_SIZE) * (gct0_data.height / CMPR_BLOCK_SIZE)
    decompressed_blocks = []
    decompressed_texture = []

    print(f"Image dimensions: {gct0_data.width}x{gct0_data.height}")
    print(f"Read data length: {len(gct0_data.texture_data)}")
    print(f"Total data length: {32*total_block_count}")

    for block_id in range(math.ceil(total_block_count)):
        compressed_block = gct0_data.texture_data[(0+(32*block_id)):(32+(32*block_id))]
        decompressed_blocks.append(decompress_cmpr_block(compressed_block))

    pixel_grid = map_pixels_to_grid(gct0_data.width, gct0_data.height, CMPR_BLOCK_SIZE, decompressed_blocks)

    for y_pos in range(gct0_data.height):
        for x_pos in range(gct0_data.width):
            try:
                decompressed_texture.append(pixel_grid[x_pos][y_pos])
            except IndexError:
                decompressed_texture.append([255, 255, 255, 255])

    return decompressed_texture


def decompress_cmpr_block(compressed_block):
    decompressed_block = []
    subblock_container = []

    for subblock_id in range(CMPR_SUBBLOCK_SIZE):
        compressed_subblock = compressed_block[(0+(8*subblock_id)):(8+(8*subblock_id))]
        subblock_container.append(decompress_cmpr_subblock(compressed_subblock))

    # crush the list before we return it
    decompressed_block.append(subblock_container[0][0])
    decompressed_block.append(subblock_container[0][1])
    decompressed_block.append(subblock_container[1][0])
    decompressed_block.append(subblock_container[1][1])

    decompressed_block.append(subblock_container[0][2])
    decompressed_block.append(subblock_container[0][3])
    decompressed_block.append(subblock_container[1][2])
    decompressed_block.append(subblock_container[1][3])

    decompressed_block.append(subblock_container[2][0])
    decompressed_block.append(subblock_container[2][1])
    decompressed_block.append(subblock_container[3][0])
    decompressed_block.append(subblock_container[3][1])

    decompressed_block.append(subblock_container[2][2])
    decompressed_block.append(subblock_container[2][3])
    decompressed_block.append(subblock_container[3][2])
    decompressed_block.append(subblock_container[3][3])  # not crushing subblocks correctly

    return decompressed_block


def decompress_cmpr_subblock(compressed_subblock):
    decompressed_subblock = []

    color0_565, color1_565 = struct.unpack('>HH', compressed_subblock[0:4])

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

    for pixel_id in range(CMPR_SUBBLOCK_SIZE):
        color_pattern = compressed_subblock[pixel_id+4]
        decompressed_subblock.append(color_map[(color_pattern >> (6 - (pixel_id * 2))) & 3])

    return decompressed_subblock


def map_pixels_to_grid(tex_x, tex_y, block_size, decompressed_blocks):
    pixel_grid = [[0, 0, 0, 0] * tex_x] * tex_y
    blocks_per_row = (len(decompressed_blocks) / (tex_y / (block_size / 2)))
    print(f"Blocks per row: {blocks_per_row}")

    block_count = 0
    y_ceiling = 0
    x_count = 0
    y_count = 0

    for block in decompressed_blocks:
        for pixel in block:
            pixel_grid[x_count][y_count] = pixel

            x_count += 1
            if x_count >= math.ceil(block_size / 2):
                y_count += 1
                x_count = 0

        x_count = 0
        y_count = y_ceiling
        block_count += 1
        if block_count >= blocks_per_row:
            y_ceiling += math.ceil(block_size / 2)
            block_count = 0

    print(f"First pixel in the grid: {pixel_grid[0][0]}")
    return pixel_grid
