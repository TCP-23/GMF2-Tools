import struct

import bpy
from bpy.types import Operator

from .export_object import *


class GM2ModelExporter(Operator):

    PLACEHOLDER_NUM = 51
    PLACEHOLDER_FLOAT = 0.5
    PLACEHOLDER_4STRING = "MRTD"
    PLACEHOLDER_8STRING = "MOREHERO"
    PLACEHOLDER_COUNT = 3

    def write_gmf2(self, context, filepath):
        file = open(filepath, 'wb')

        # Create the headers last, then append them to the top of the file
        GM2ModelExporter.create_main_header(self, context, file)
        GM2ModelExporter.create_tex_headers(self, file)
        GM2ModelExporter.create_mat_headers(self, file)
        GM2ModelExporter.create_wobject_headers(self, context, file)

        GM2ModelExporter.create_embedded_texture_data(self, file)
        GM2ModelExporter.create_material_data(self, file)
        GM2ModelExporter.create_mesh_data(self, context, file)

        file.close()

    def create_main_header(self, context, file):
        file.write(struct.pack('@4s', "GMF2".encode('shift_jis')))  # magic
        file.write(struct.pack('<I', 2))  # version

        file.write(struct.pack('16x'))

        if (self.selected_only):
            num_objects = len(context.selected_objects)
            num_textures = 0
            num_materials = 0
        else:
            num_objects = len(context.scene.objects)
            num_textures = len(bpy.data.textures)
            num_materials = len(bpy.data.materials)

        file.write(struct.pack('<H', num_objects))  # number of objects
        file.write(struct.pack('<H', num_textures))  # number of textures
        file.write(struct.pack('2x'))
        file.write(struct.pack('<H', num_materials))  # number of materials

        tex_offset = 112
        mat_offset = tex_offset + num_textures * 32
        obj_offset = mat_offset + num_materials * 32

        file.write(struct.pack('<I', obj_offset))  # starting offset of object data
        file.write(struct.pack('<I', tex_offset))  # starting offset of texture data (always 112 in NMH1 models)
        file.write(struct.pack('4x'))
        file.write(struct.pack('<I', mat_offset))  # starting offset of material data

        file.write(struct.pack('<I', 28))  # unknown data
        file.write(struct.pack('<I', 6))  # unknown data

        file.write(struct.pack('56x'))

    def create_tex_headers(self, file):
        for i, btex in enumerate(bpy.data.textures):
            file.write(struct.pack('@8s', btex.image.name.encode('shift_jis')))  # texture name

            prev_tex_offset = 32 * (i - 1) + 112
            if (prev_tex_offset < 112):
                prev_tex_offset = 0
            next_tex_offset = 32 * (i + 1) + 112
            if (i + 1) >= len(bpy.data.textures):
                next_tex_offset = 0

            file.write(struct.pack('<I', prev_tex_offset))  # offset of previous texture
            file.write(struct.pack('<I', next_tex_offset))  # offset of next texture

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the texture's data
            file.write(struct.pack('<I', i))  # unknown data (probably texture index)
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # length of the texture's data

            file.write(struct.pack('@4s', GM2ModelExporter.PLACEHOLDER_4STRING.encode('shift_jis')))  # unknown data

    def create_mat_headers(self, file):
        base_mat_offset = 112 + len(bpy.data.textures) * 32

        for i, bmat in enumerate(bpy.data.materials):
            file.write(struct.pack('@8s', bmat.name.encode('shift_jis')))  # material name

            prev_mat_offset = 32 * (i - 1) + base_mat_offset
            if (prev_mat_offset < base_mat_offset):
                prev_mat_offset = 0
            next_mat_offset = 32 * (i + 1) + base_mat_offset
            if (i + 1) >= len(bpy.data.materials):
                next_mat_offset = 0
            
            file.write(struct.pack('<I', prev_mat_offset))  # offset of previous material
            file.write(struct.pack('<I', next_mat_offset))  # offset of next material

            file.write(struct.pack('<I', 1))  # unknown data

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the material's data

            file.write(struct.pack('8x'))

    def create_wobject_headers(self, context, file):
        base_obj_offset = 112 + (len(bpy.data.textures) * 32) + (len(bpy.data.materials) * 32)

        for i, bobj in enumerate(context.scene.objects):
            file.write(struct.pack('@8s', bobj.name.encode('shift_jis')))  # object name

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the vbuffer

            prev_obj_offset = 128 * (i - 1) + base_obj_offset
            if (prev_obj_offset < base_obj_offset):
                prev_obj_offset = 0
            next_obj_offset = 128 * (i + 1) + base_obj_offset
            if (i + 1) >= len(context.scene.objects):
                next_obj_offset = 0

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of parent wobject
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of first child wobject
            file.write(struct.pack('<I', prev_obj_offset))  # offset of previous wobject
            file.write(struct.pack('<I', next_obj_offset))  # offset of next wobject

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the wobject's surface data
            file.write(struct.pack('<I', 0))  # unknown data (probably unused offset)
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the first bone linked to the object

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # v divisor (sometimes?)

            pos_x = bobj.location.x * self.exp_scale
            pos_y = bobj.location.y * self.exp_scale
            pos_z = bobj.location.z * self.exp_scale

            file.write(struct.pack('<f', pos_x))  # position x
            file.write(struct.pack('<f', pos_y))  # position y
            file.write(struct.pack('<f', pos_z))  # position z
            file.write(struct.pack('<f', 1))  # unused 4th component of position? always 1

            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # rotation x
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # rotation y
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # rotation z
            file.write(struct.pack('<f', 1))  # unused 4th component of rotation? always 1

            file.write(struct.pack('<f', 1))  # scale x
            file.write(struct.pack('<f', 1))  # scale y
            file.write(struct.pack('<f', 1))  # scale z

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # used as offset for v format, not sure what it actually is

            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # cullbox position x
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # cullbox position y
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # cullbox position z
            file.write(struct.pack('<f', 1))  # unused 4th component of cullbox position? always 1

            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # cullbox size x
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # cullbox size y
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # cullbox size z
            file.write(struct.pack('<f', 1))  # unused 4th component of cullbox size? always 1
    
    def create_embedded_texture_data(self, file):
        for i, btex in enumerate(bpy.data.textures):
            file.write(struct.pack('@4s', "GCT0".encode('shift_jis')))  # magic

            file.write(struct.pack('2x'))

            file.write(struct.pack('>H', GM2ModelExporter.PLACEHOLDER_NUM))  # encoding format

            file.write(struct.pack('>H', GM2ModelExporter.PLACEHOLDER_NUM))  # texture width
            file.write(struct.pack('>H', GM2ModelExporter.PLACEHOLDER_NUM))  # texture height

            file.write(struct.pack('B', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data
            file.write(struct.pack('3x'))

            file.write(struct.pack('>I', 64))  # data offset (always 64?)

            file.write(struct.pack('8x'))

            file.write(struct.pack('>H', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data
            file.write(struct.pack('2x'))

            file.write(struct.pack('>I', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data

            file.write(struct.pack('28x'))

            file.write(struct.pack('112x'))  # actual encoded texture data

            file.write(struct.pack('16x'))  # 16 empty bytes after texture data
    
    def create_material_data(self, file):
        for i, bmat in enumerate(bpy.data.materials):
            file.write(struct.pack('4x'))
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset to ramp data
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset to main texture header
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data

            # shader parameter vector?
            file.write(struct.pack('<f', 0))  # x
            file.write(struct.pack('<f', 0))  # y
            file.write(struct.pack('<f', 0))  # z
            file.write(struct.pack('<f', 1))  # w?

            # tint parameter vector?
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # x
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # y
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # z
            file.write(struct.pack('<f', 1))  # w?

        #     file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset to main data
        #     file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data
        #     file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset to ramp texture header
        #     file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data

        #     # shader parameter vector?
        #     file.write(struct.pack('<f', 0))  # x
        #     file.write(struct.pack('<f', 0))  # y
        #     file.write(struct.pack('<f', 0))  # z
        #     file.write(struct.pack('<f', 1))  # w?

        #     # tint parameter vector?
        #     file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # x
        #     file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # y
        #     file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # z
        #     file.write(struct.pack('<f', 1))  # w?

    def create_mesh_data(self, context, file):
        for i, bobj in enumerate(context.scene.objects):
            pass
