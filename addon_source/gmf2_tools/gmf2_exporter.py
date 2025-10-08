import struct

import bpy
from bpy.types import Operator


class GM2ModelExporter(Operator):

    PLACEHOLDER_NUM = 51
    PLACEHOLDER_FLOAT = 0
    PLACEHOLDER_4STRING = "MRTD"
    PLACEHOLDER_8STRING = "MOREHERO"
    PLACEHOLDER_COUNT = 3

    def write_gmf2(self, context, filepath):
        file = open(filepath, 'wb')

        # Create the headers last, then append them to the top of the file
        GM2ModelExporter.create_main_header(self, context, file)
        GM2ModelExporter.create_tex_headers(self, file)
        GM2ModelExporter.create_mat_headers(self, file)
        GM2ModelExporter.create_wobject_headers(self, file)

        file.close()

    def create_texture_data(self, file):
        pass

    def create_material_data(self, file):
        pass

    def create_wobject_data(self, file):
        pass

    def create_mesh_data(self, file):
        pass

    def create_main_header(self, context, file):
        file.write(struct.pack('@4s', "GMF2".encode('shift_jis')))  # magic
        file.write(struct.pack('<I', 2))  # version

        file.write(struct.pack('16x'))

        file.write(struct.pack('<H', len(bpy.data.objects)))  # number of objects
        file.write(struct.pack('<H', len(bpy.data.textures)))  # number of textures
        file.write(struct.pack('2x'))
        file.write(struct.pack('<H', len(bpy.data.materials)))  # number of materials

        file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # starting offset of object data
        file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # starting offset of texture data
        file.write(struct.pack('4x'))
        file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # starting offset of material data

        file.write(struct.pack('<I', 28))  # unknown data
        file.write(struct.pack('<I', 6))  # unknown data

        file.write(struct.pack('56x'))

    def create_tex_headers(self, file):
        for tex_idx in range(0, GM2ModelExporter.PLACEHOLDER_COUNT):
            # Create the header for the texture
            file.write(struct.pack('@8s', GM2ModelExporter.PLACEHOLDER_8STRING.encode('shift_jis')))  # texture name

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of previous texture
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of next texture

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the texture's data
            file.write(struct.pack('<I', tex_idx))  # unknown data (probably texture index)
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # length of the texture's data

            file.write(struct.pack('@4s', GM2ModelExporter.PLACEHOLDER_4STRING.encode('shift_jis')))  # unknown data

    def create_mat_headers(self, file):
        for mat_idx in range(0, GM2ModelExporter.PLACEHOLDER_COUNT):
            # Create the header for the material
            file.write(struct.pack('@8s', GM2ModelExporter.PLACEHOLDER_8STRING.encode('shift_jis')))  # material name

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of previous material
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of next material

            file.write(struct.pack('<I', 1))  # unknown data

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the material's data

            file.write(struct.pack('8x'))

    def create_wobject_headers(self, file):
        for wobj_index in range(0, GM2ModelExporter.PLACEHOLDER_COUNT):
            # Create the header for the world object
            file.write(struct.pack('@8s', GM2ModelExporter.PLACEHOLDER_8STRING.encode('shift_jis')))  # wobject name

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # unknown data

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the vbuffer

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of parent wobject
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of first child wobject
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of previous wobject
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of next wobject

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the wobject's surface data
            file.write(struct.pack('<I', 0))  # unknown data (probably unused offset)
            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # offset of the first bone linked to the object

            file.write(struct.pack('<I', GM2ModelExporter.PLACEHOLDER_NUM))  # v divisor (sometimes?)

            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # position x
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # position y
            file.write(struct.pack('<f', GM2ModelExporter.PLACEHOLDER_FLOAT))  # position z
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
