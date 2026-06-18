import math

import bpy
import bmesh
from bpy.types import Operator
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from .gmf2b import Gmf2b
from .tme import Tme
from .blood_object_info import *
from ..gct0.gct0_handler import GCTTextureHandler

SCALE_MULTIPLIER = 0.1
PI_OVER_TWO = math.pi / 2


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
        empties: list[BloodModelObjectInfo] = []
        bones: list[BloodModelObjectInfo] = []
        meshes: list[BloodModelObjectInfo] = []

        non_bones: list[BloodModelObjectInfo] = []

        for obj in objects:
            is_empty = True

            if obj.has_model_data:
                is_empty = False
                meshes.append(obj)
                non_bones.append(obj)
            if obj.is_bone:
                is_empty = False
                bones.append(obj)
            
            if is_empty:
                empties.append(obj)
                non_bones.append(obj)
        
        arm_obj = None
        if len(bones) > 0:
            arm_obj = GMF2BModelImporter.create_armature(self, context, bones)

        for obj in non_bones:
            new_bobj = GMF2BModelImporter.create_object(self, context, obj)
            GMF2BModelImporter.bobj_list[obj.data_object.offset] = new_bobj

            if obj.is_child:
                if obj.parent.is_bone:
                    context.view_layer.objects.active = arm_obj
                    new_bobj.parent = arm_obj
                    new_bobj.parent_type = "BONE"
                    new_bobj.parent_bone = obj.parent.unique_name_string
                    new_bobj.matrix_parent_inverse = arm_obj.pose.bones[obj.parent.unique_name_string].matrix.inverted()
                    
                    if obj.has_model_data:
                        new_bobj.modifiers.new(type="ARMATURE", name="Armature").object = arm_obj

    def create_object(self, context, obj_info: BloodModelObjectInfo):
        if obj_info.has_model_data:
            new_bobj = GMF2BModelImporter.create_mesh(self, context, obj_info)
        else:
            new_bobj = bpy.data.objects.new(obj_info.unique_name_string, bpy.data.meshes.new(obj_info.unique_name_string))
            context.collection.objects.link(new_bobj)

            # Handle position later
        
        # Handle objects that are children of bones elsewhere
        if obj_info.is_child:
            if not obj_info.parent.is_bone:
                new_bobj.parent = GMF2BModelImporter.bobj_list[obj_info.parent.data_object.offset]
        else:
            new_bobj.rotation_euler = (PI_OVER_TWO, 0, 0)

        return new_bobj

    def create_armature(self, context, bones: list[BloodModelObjectInfo]):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1)
        bone_model = context.active_object

        arm_data = bpy.data.armatures.new("Armature")
        arm_obj = bpy.data.objects.new("Armature", arm_data)
        context.collection.objects.link(arm_obj)
        arm_obj.rotation_euler = (PI_OVER_TWO, 0, 0)
        context.view_layer.objects.active = arm_obj

        bpy.ops.object.mode_set(mode="EDIT")
        edit_bones = {}
        for b in bones:
            eb = arm_data.edit_bones.new(b.unique_name_string)
            pos = b.global_matrix.translation
            eb.head = pos
            eb.tail = pos
            edit_bones[b.data_object.offset] = eb
        for b in bones:
            if b.is_child:
                edit_bones[b.data_object.offset].parent = edit_bones[b.parent.data_object.offset]

        bpy.ops.object.mode_set(mode="OBJECT")

        pose_bones = context.object.pose.bones
        pose_bone_scale = (self.imp_scale * SCALE_MULTIPLIER) / 5
        for b in pose_bones:
            b.custom_shape = bone_model
            b.custom_shape_scale_xyz = tuple((pose_bone_scale, pose_bone_scale, pose_bone_scale))
            b.use_custom_shape_bone_size = False
        
        bpy.ops.object.select_all(action="DESELECT")
        bpy.data.objects[bone_model.name].select_set(True)
        bpy.ops.object.delete(use_global=False, confirm=False)

        context.view_layer.objects.active = arm_obj

        return arm_obj

    def create_mesh(self, context, mesh_info: BloodModelObjectInfo):
        vertices, uvs, faces, face_mats = [], [], [], []
        v_off = 0
        mat_counter = 0

        vertex_groups: dict[int, list[int]] = {}

        mat_offset_to_idx = {}

        for i, surf in enumerate(mesh_info.data_object.surfaces):
            vertex_groups[i] = []
            for strip_data in surf.data_strips:
                if self.import_mats:
                    if not mat_offset_to_idx.keys().__contains__(surf.off_material):
                        mat_offset_to_idx[surf.off_material] = mat_counter
                        mat_counter += 1
                
                for j, vdata in enumerate(strip_data.vertices):
                    global_vec = mesh_info.global_matrix @ mathutils.Vector((vdata.position.x, vdata.position.y, vdata.position.z))
                    vertices.append((global_vec.x, global_vec.y, global_vec.z))
                    vertex_groups[i].append(v_off + j)

                    uvs.append((vdata.u, vdata.v))

                for s in range(strip_data.count - 2):
                    idx = [v_off + s, v_off + s + 1, v_off + s + 2]
                    if s % 2 == 1: idx[0], idx[1] = idx[1], idx[0]
                    if len(set(idx)) == 3:
                        faces.append(idx)
                        face_mats.append(mat_offset_to_idx[surf.off_material])
                
                v_off += strip_data.count

                if not self.assume_surf_data:
                    break
    
        mesh_data = bpy.data.meshes.new(mesh_info.unique_name_string)
        mesh_data.from_pydata(vertices, [], faces)

        mat_idx_to_offset = {value: key for key, value in mat_offset_to_idx.items()}
        for mat_idx in range(0, mat_counter):
            mesh_data.materials.append(GMF2BModelImporter.bmat_list[mat_idx_to_offset[mat_idx]])
        
        for poly, m_idx in zip(mesh_data.polygons, face_mats):
            poly.material_index = m_idx
            poly.use_smooth = True
        
        uv_layer = mesh_data.uv_layers.new(name="UVMap")
        for loop in mesh_data.loops:
            uv_layer.data[loop.index].uv = uvs[loop.vertex_index]
        
        new_bobj = bpy.data.objects.new(mesh_info.unique_name_string, mesh_data)
        context.collection.objects.link(new_bobj)

        for i in range(len(mesh_info.data_object.surfaces)):
            vg = new_bobj.vertex_groups.new(name=f"surface_{i+1}")
            vg.add(vertex_groups[i], 1.0, "REPLACE")

        context.view_layer.objects.active = new_bobj
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.average_normals(average_type="FACE_AREA")
        bpy.ops.object.mode_set(mode="OBJECT")
        new_bobj.select_set(False)

        # if mesh_info.is_child:
        #     if mesh_info.root.is_bone:
        #         vg = new_bobj.vertex_groups.new(name=mesh_info.parent.unique_name_string)
        #         vg.add(list(range(len(vertices))), 1.0, "REPLACE")

        return new_bobj

    def cleanup(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
