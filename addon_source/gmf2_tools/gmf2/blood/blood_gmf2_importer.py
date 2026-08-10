import bpy
import bmesh
import struct
import mathutils
import math
import os
from bpy.types import Operator


class BinaryReader:
    def __init__(self, data):
        self.data = data
        self.offset = 0
        self.size = len(data)
    
    def seek(self, off, whence=0):
        if whence == 0: self.offset = off
        elif whence == 1: self.offset += off
        elif whence == 2: self.offset = self.size + off

    def read(self, fmt):
        res = struct.unpack_from(fmt, self.data, self.offset)
        self.offset += struct.calcsize(fmt)
        return res
    
    def read_string(self, length):
        raw = struct.unpack_from(f'<{length}s', self.data, self.offset)[0]
        self.offset += length
        return raw.split(b'\x00')[0].decode('ascii', errors='ignore')
    

def get_parent_index(parent_name, bones):
    for i, bone in enumerate(bones):
        if bone['name'] == parent_name:
            return i
    return -1


def find_tme_blocks(data):
    magics = [b'\x4C\x10\x00\x20', b'\x4C\x04\x00\x20', b'\x4C\x38\x00\x20', b'\x10\x20\x00\x20']
    offsets = []
    for magic in magics:
        start = 0
        while True:
            idx = data.find(magic, start)
            if idx == -1: break
            offsets.append(idx)
            start = idx + 4
    return sorted(offsets)


def decode_tme_to_material(data, offset, mat_idx):
    csm_flags = data[offset + 0x0A]
    print(csm_flags)
    img_width = struct.unpack_from('<I', data, offset + 0x40)[0]
    img_height = struct.unpack_from('<I', data, offset + 0x44)[0]

    pixel_size = img_width * img_height
    pixels_data = data[offset + 0x70 : offset + 0x70 + pixel_size]
    pal_off = offset + 0x70 + pixel_size + 0x60
    palette_data = bytearray(data[pal_off : pal_off + 0x400])

    if csm_flags == 0x08:
        new_pal = bytearray(0x400)
        for i in range(256):
            swapped_i = (i & ~0x18) | ((i & 0x08) << 1) | ((i & 0x10) >> 1)
            new_pal[i * 4 : i * 4 + 4] = palette_data[swapped_i * 4 : swapped_i * 4 + 4]
        palette_data = new_pal
    
    blender_pixels = [0.0] * (img_width * img_height * 4)
    for y in range(img_height):
        for x in range(img_width):
            px_idx = y * img_width + x
            pal_idx = pixels_data[px_idx]
            out_idx = ((img_height - 1 - y) * img_width + x) * 4
            blender_pixels[out_idx] = palette_data[pal_idx * 4] / 255.0
            blender_pixels[out_idx + 1] = palette_data[pal_idx * 4 + 1] / 255.0
            blender_pixels[out_idx + 2] = palette_data[pal_idx * 4 + 2] / 255.0
            blender_pixels[out_idx + 3] = 1.0
    
    img = bpy.data.images.new(f"TME_Tex_{mat_idx:02X}", img_width, img_height, alpha=True)
    img.pixels = blender_pixels

    mat = bpy.data.materials.new(name=f"TME_Mat_{mat_idx:02X}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])
    mat.blend_method = 'HASHED'
    return mat


class BloodGMF2ModelImporter(Operator):
    bl_idname = "gm2_importer.blood_data"
    bl_label = "Import Blood GMF2 model"

    def import_gm2(self, context, filepath):
        with open(filepath, 'rb') as f:
            data = f.read()
        
        bs = BinaryReader(data)
        if not data.startswith((b'GMDF', b'GM2F', b'GMF2')):
            return {'CANCELLED'}
        
        tme_offsets = find_tme_blocks(data)
        materials = [decode_tme_to_material(data, off, i) for i, off in enumerate(tme_offsets)]

        bs.seek(24)
        bone_num, mesh_num, unk, mat_num = bs.read('<4H')
        info = bs.read('<6I')

        bs.seek(info[0])
        bones, mesh_offsets, off_unk = [], [], []

        for x in range(bone_num):
            name = bs.read_string(8)
            node_type = bs.read('<q')[0]
            b_info = list(bs.read('<4I'))

            curPos = bs.offset
            for i, off in enumerate(b_info):
                if off != 0:
                    bs.seek(off)
                    b_info[i] = bs.read_string(8)
                    bs.seek(curPos)
                else:
                    b_info[i] = None
            
            mesh_off = bs.read('<I')[0]
            if mesh_off != 0:
                mesh_offsets.append(mesh_off)
                off_unk.append([bs.read('<I')[0], bs.read('<I')[0], name])
                bs.seek(4, 1)
            else:
                bs.seek(12, 1)
            
            px, py, pz = bs.read('<3f')
            bs.seek(68, 1)

            local_mat = mathutils.Matrix.Translation((px, py, pz))
            bones.append({
                'index': x, 'name': name, 'local_mat': local_mat,
                'global_mat': local_mat.copy(), 'parent_name': b_info[0]
            })
        
        for bone in bones:
            bone['parent_index'] = get_parent_index(bone['parent_name'], bones)
            if bone['parent_index'] != -1:
                parent_bone = bones[bone['parent_index']]
                bone['global_mat'] = parent_bone['global_mat'] @ bone['local_mat']
        
        arm_data = bpy.data.armatures.new("Armature")
        arm_obj = bpy.data.objects.new("Armature", arm_data)
        context.collection.objects.link(arm_obj)
        arm_obj.rotation_euler = (math.radians(90), 0, 0)
        context.view_layer.objects.active = arm_obj

        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = {}
        for b in bones:
            eb = arm_data.edit_bones.new(b['name'])
            pos = b['global_mat'].translation
            eb.head, eb.tail = pos, pos + mathutils.Vector((0, 0.1, 0))
            edit_bones[b['name']] = eb
        for b in bones:
            if b['parent_index'] != -1:
                parent_name = bones[b['parent_index']]['name']
                edit_bones[b['name']].parent = edit_bones[parent_name]
        bpy.ops.object.mode_set(mode='OBJECT')

        for i, x_off in enumerate(mesh_offsets):
            bs.seek(x_off)
            x_val = x_off
            while x_val != 0:
                bs.seek(4, 1)
                x_val, _ = bs.read('<2I')
                bs.seek(20, 1)
            
            end = bs.size if i + 1 >= len(mesh_offsets) else (off_unk[i + 1][1] if off_unk[i + 1][1] != 0 else mesh_offsets[i + 1])
            bone_name = off_unk[i][2]
            mesh_name = bone_name if bone_name else f"Mesh_{i}"

            parent_bone_mat = mathutils.Matrix.Identity(4)
            for b in bones:
                if b['name'] == bone_name:
                    parent_bone_mat = b['global_mat']
                    break
            
            vertices, uvs, faces, face_mats = [], [], [], []
            v_off, mat_counter = 0, 0

            while bs.offset < end:
                bs.seek(16, 1)
                count, dir_val, _ = bs.read('<IIQ')
                if count <= 0: break

                for _ in range(count):
                    v_start = bs.offset
                    px, py, pz = bs.read('<3f')
                    global_vec = parent_bone_mat @ mathutils.Vector((px, py, pz))
                    vertices.append((global_vec.x, global_vec.y, global_vec.z))

                    bs.seek(v_start + 48)
                    u, v_tex = bs.read('<2f')
                    uvs.append((u, 1.0 - v_tex))
                    bs.seek(v_start + 64)

                current_mat_idx = mat_counter % len(materials) if materials else 0

                for s in range(count - 2):
                    idx = [v_off + s, v_off + s + 1, v_off + s + 2]
                    if s % 2 == 1: idx[0], idx[1] = idx[1], idx[0]
                    if len(set(idx)) == 3:
                        faces.append(idx)
                        face_mats.append(current_mat_idx)

                v_off += count
                mat_counter += 1
                bs.seek(16, 1)
            
            if not vertices: continue

            mesh_data = bpy.data.meshes.new(mesh_name)
            mesh_data.from_pydata(vertices, [], faces)

            used_mats = sorted(list(set(face_mats)))
            mat_map = {old: new for new, old in enumerate(used_mats)}
            for old_idx in used_mats:
                if old_idx < len(materials): mesh_data.materials.append(materials[old_idx])
            for poly, m_idx in zip(mesh_data.polygons, face_mats):
                poly.material_index = mat_map.get(m_idx, 0)
                poly.use_smooth = True
            
            uv_layer = mesh_data.uv_layers.new(name="UVMap")
            for loop in mesh_data.loops:
                uv_layer.data[loop.index].uv = uvs[loop.vertex_index]
            
            obj = bpy.data.objects.new(mesh_name, mesh_data)
            context.collection.objects.link(obj)
            vg = obj.vertex_groups.new(name=bone_name)
            vg.add(list(range(len(vertices))), 1.0, 'REPLACE')
            obj.parent = arm_obj
            obj.modifiers.new(type='ARMATURE', name='Armature').object = arm_obj

            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.average_normals(average_type='FACE_AREA')
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select_set(False)
        
        context.view_layer.objects.active = arm_obj
        return {'FINISHED'}