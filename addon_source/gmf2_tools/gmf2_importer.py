import bpy
import struct
from collections import namedtuple
from bpy.types import Operator

from .target_game import GameTarget_Enum
from .target_game import TargetGame

from .gmf2 import Gmf2
from .object_creator import GM2ObjectCreator
from .gct0_handler import GCTTextureHandler
from .processed_object_data import ModelObjInfo

Vec3 = namedtuple("Vec3", "x y z")
Gm2Idx = namedtuple("Gm2Idx", "i u v n")


# Used to keep links from the GM2 file when imported into Blender
"""class ProcessedObject:
    obj = None
    parent_obj = None
    first_child_obj = None
    prev_obj = None
    next_obj = None

    def __init__(self, _obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj):
        self.obj = _obj
        self.parent_obj = _parent_obj
        self.first_child_obj = _first_child_obj
        self.prev_obj = _prev_obj
        self.next_obj = _next_obj"""


# Sorts objects based on their data types, and creates lists of the objects
def sort_objects(objs):
    sorted_objs = []
    sorted_bones = []

    bone_world_objects = []

    processed_object_data = ModelObjInfo.process_object_info(objs)
    for proc_data in processed_object_data:
        if proc_data.is_bone:
            sorted_bones.append(proc_data)
        #elif proc_data.has_model_data:
            #sorted_meshes.append(proc_data)
        else:
            sorted_objs.append(proc_data)

    """# Loop through every object inside the provided list
    for i, world_object in objs.items():
        parent, first_child, prev_obj, next_obj = None, None, None, None

        # Get references to linked objects
        if world_object.off_parent in objs:
            parent = objs[world_object.off_parent]
        if world_object.off_first_child in objs:
            first_child = objs[world_object.off_first_child]
        if world_object.off_prev in objs:
            prev_obj = objs[world_object.off_prev]
        if world_object.off_next in objs:
            next_obj = objs[world_object.off_next]

        # Create a ProcessedObject
        processed_obj = ProcessedObject(world_object, parent, first_child, prev_obj, next_obj)

        # Add the ProcessedObject to the appropriate list based on object type
        if processed_obj.obj.name == "ROOT" and processed_obj.obj.surfaces is None:
            processed_obj.obj.isBone = True
            sorted_bones.append(processed_obj)
            bone_world_objects.append(processed_obj.obj)
        elif processed_obj.parent_obj in bone_world_objects and processed_obj.obj.surfaces is None:
            processed_obj.obj.isBone = True
            sorted_bones.append(processed_obj)
            bone_world_objects.append(processed_obj.obj)
        else:
            processed_obj.obj.isBone = False
            sorted_objs.append(processed_obj)"""

    return sorted_objs, sorted_bones


def get_tristrip_format(surface, num_idx):
    surfbuf = surface.surface_data.strip_data

    try:
        if surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 153 \
                or (surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 5] == 0
                    # and surfbuf[struct.unpack('>H', surfbuf[2:4])[0] * 11 + 4] != 0
                    and num_idx == surface.surface_data.num_vertices):
            return 1
    except IndexError:
        pass
        #print("Error in detecting tristrip format!")
        #print(f"Surface buffer length: {len(surfbuf)}")

    return 0


class GM2ModelImporter(Operator):
    """Import mesh data from a GMF2 file"""
    bl_idname = "gm2_importer.model_data"
    bl_label = "Import GMF2 model"

    obj_list = {}
    offset_list = {}
    junk_objs = {}
    temp_arm_list = {}

    def load_file_data(self, context, filepath):
        # Manually clear the object and junk object lists
        # Have to do this because Blender doesn't automatically clear them, otherwise the addon would break if you tried
        # to import multiple objects
        GM2ModelImporter.obj_list.clear()
        GM2ModelImporter.offset_list.clear()
        GM2ModelImporter.junk_objs.clear()

        # Read the data from the GM2 file, and create a variable to hold it
        gm2: Gmf2 = Gmf2.from_file(filepath)

        # Detect the game the file is from
        if gm2.game_id == Gmf2.GameName.nmh2:
            TargetGame.gameId = GameTarget_Enum.NMH2
        else:
            TargetGame.gameId = GameTarget_Enum.NMH1

        # Get a list of all the objects in the file
        unsorted_objects = {}
        for i, world_object in enumerate(gm2.world_objects):
            unsorted_objects[world_object.offset] = world_object

        # Sort all the objects based on their type
        objects, bones = sort_objects(unsorted_objects)
        obj_armature = None

        if self.import_mats:
            if len(gm2.textures) > 0:
                GCTTextureHandler.import_textures(self, context, gm2.textures)
            if len(gm2.materials) > 0:
                GCTTextureHandler.import_materials(self, context, gm2.materials)

        if self.import_models:
            if len(bones) > 0:
                obj_armature = GM2ModelImporter.import_bones(self, context, bones)
            if len(objects) > 0:
                GM2ModelImporter.import_objects(self, context, objects, obj_armature)

        GM2ModelImporter.cleanup_imported(self, context, objects, obj_armature)

    def import_objects(self, context, objects, obj_arm):
        for m_info in objects:
            # Check if the object has model data
            if m_info.has_model_data:  # If so, get the mesh data from the surfaces
                obj_data = [[], [], [], [], [], [], []]  # vertices, indices, uvs, normals, unused (for now), material offset, skinning name

                obj_data[0] += GM2ModelImporter.GET_OBJECT_VERTS(self, m_info)
                for surf in m_info.data_obj.surfaces:
                    surf_idxs, surf_uvs, surf_norms = GM2ModelImporter.GET_SURFACE_DATA(self, m_info, surf)
                    skin_name = GM2ModelImporter.get_skin_data(self, surf)

                    obj_data[1].append(surf_idxs)
                    obj_data[2] += surf_uvs
                    obj_data[3] += surf_norms
                    obj_data[5].append(surf.off_material)
                    obj_data[6].append(skin_name)

                # Create a mesh using the mesh data
                new_mesh = GM2ObjectCreator.CREATE_MESH(self, context, m_info, obj_data, obj_arm)

                # Add the mesh to the object list
                GM2ModelImporter.obj_list[m_info.data_obj] = new_mesh

                # Set the object's parent
                if m_info.is_child_obj:
                    new_mesh.parent = GM2ModelImporter.obj_list[m_info.parent_obj]

                # If the object has normals, apply them
                if len(GM2ObjectCreator.normals) > 0:
                    GM2ObjectCreator.apply_normals(self, new_mesh.data)
            else:  # If the object has no surfaces, create an empty object
                new_obj = GM2ObjectCreator.CREATE_OBJECT(self, context, m_info)
                GM2ModelImporter.obj_list[m_info.data_obj] = new_obj

                # Set the object's parent
                if m_info.is_child_obj:
                    new_obj.parent = GM2ModelImporter.obj_list[m_info.parent_obj]

    def GET_OBJECT_VERTS(self, m_info):
        verts = []
        v_buf = m_info.data_obj.v_data.v_buffer

        for v in v_buf:
            # Check the game ID
            if TargetGame.gameId == GameTarget_Enum.NMH1:
                try:
                    vertPos = Vec3((v.x / pow(2, m_info.data_obj.v_divisor)) * self.imp_scale,
                                   (v.y / pow(2, m_info.data_obj.v_divisor)) * self.imp_scale,
                                   (v.z / pow(2, m_info.data_obj.v_divisor)) * self.imp_scale)
                except OverflowError:
                    vertPos = Vec3(0.1, 0.1, 0.1)
                    print(len(v_buf))
                    return []
            elif TargetGame.gameId == GameTarget_Enum.NMH2:
                vertPos = Vec3(v.x * self.imp_scale, v.y * self.imp_scale, v.z * self.imp_scale)
            else:  # If the game ID isn't recognized, return empty
                return []

            verts.append(vertPos)

        return verts

    def GET_SURFACE_DATA(self, m_info, surf):
        mesh_strips = GM2ModelImporter.GET_MESH_STRIPS(self, surf, m_info)

        # If the surface has no strips, return empty
        if not mesh_strips:
            return [], [], []

        indices = []
        uvs = []
        normals = []

        # Loop through every data bit in the strips
        for idx in mesh_strips:
            normals.append(tuple((idx.n[0] / pow(2, 10), idx.n[1] / pow(2, 10), idx.n[2] / pow(2, 10))))
            uvs.append(tuple((idx.u / pow(2, 10), -(idx.v / pow(2, 10)) + 1)))

        valid_idx_count = 0
        for iii in range(len(mesh_strips) - 2):
            valid_idx_count += 1
            if valid_idx_count >= 4:
                valid_idx_count = 1

            if valid_idx_count == 1:
                va = mesh_strips[iii].i + 1
                vb = mesh_strips[iii + 1].i + 1
                vc = mesh_strips[iii + 2].i + 1

                indices.append(tuple((va, vb, vc)))

        return indices, uvs, normals

    def GET_MESH_STRIPS(self, surf, m_info):
        surfbuf = surf.surface_data.strip_data
        mesh_strips = []

        head = 0
        i_remaining = surf.surface_data.num_vertices

        while i_remaining > 0:
            command = struct.unpack('>H', surfbuf[head:head+2])[0]
            num_idx = struct.unpack('>H', surfbuf[head+2:head+4])[0]
            head += 4

            idxs = []
            match command:
                case 0x96:
                    # unknown what this means, appears in some models
                    return []
                case 0x99:
                    for _ in range(num_idx):
                        if (self.index_override == "OPT_D" or
                                (self.index_override == "OPT_A" and m_info.data_obj.v_data.v_format is not None)):
                            ibuf = surfbuf[head:head+11]
                            head += 11

                            idx = struct.unpack('>H', ibuf[0:2])[0]
                            norm = tuple((ibuf[2], ibuf[3], ibuf[4]))
                            u = struct.unpack('>h', ibuf[7:9])[0]
                            v = struct.unpack('>h', ibuf[9:11])[0]
                        else:
                            if (self.index_override == "OPT_C" or
                                    (self.index_override == "OPT_A" and get_tristrip_format(surf, num_idx) == 1)):
                                ibuf = surfbuf[head+2:head+11]
                                head += 11
                            else:
                                ibuf = surfbuf[head:head+9]
                                head += 9

                            idx = struct.unpack('>H', ibuf[0:2])[0]
                            norm = tuple((ibuf[2], ibuf[3], ibuf[4]))
                            u = struct.unpack('>h', ibuf[5:7])[0]
                            v = struct.unpack('>h', ibuf[7:9])[0]

                        if len(m_info.data_obj.v_data.v_buffer) >= idx - 1:
                            idxs.append(Gm2Idx(idx, u, v, norm))
                        else:
                            return []
                case _:
                    print(f"ERR: unk_0 = {hex(command)}")
                    return []

            if len(idxs) <= 0:
                return []

            for i in range(num_idx-2):
                if idxs[i] != idxs[i+1] and idxs[i] != idxs[i+2] and idxs[i+1] != idxs[i+2]:
                    if i % 2 == 0:
                        mesh_strips.append(idxs[i])
                        mesh_strips.append(idxs[i+1])
                        mesh_strips.append(idxs[i+2])
                    else:
                        mesh_strips.append(idxs[i])
                        mesh_strips.append(idxs[i+2])
                        mesh_strips.append(idxs[i+1])

            i_remaining -= num_idx

        return mesh_strips

    def get_skin_data(self, surf):
        skin_name = ""

        return skin_name

    def import_bones(self, context, bones):
        root_key = ""
        bone_model = None

        combined_armature = None

        # Create a sphere, and grab its mesh. Later, we will use this model as the display model for the bones.
        if not self.display_tails:
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1)
            bone_model = bpy.context.active_object

        for i, bone in enumerate(bones):
            new_bone = GM2ObjectCreator.CREATE_OBJECT(self, context, bone)

            # Append the bone to the object and junk object lists
            GM2ModelImporter.junk_objs[bone.data_obj] = new_bone
            GM2ModelImporter.obj_list[bone.data_obj] = new_bone

            if bone.parent_obj is not None:
                new_bone.parent = GM2ModelImporter.obj_list[bone.parent_obj]
                new_bone.parent = GM2ModelImporter.junk_objs[bone.parent_obj]

            # Create a temporary armature for all the bones
            temp_arm = GM2ObjectCreator.CREATE_BONE(self, context, bone, new_bone)

            # Append the temporary armature to a list
            GM2ModelImporter.temp_arm_list[temp_arm.name] = temp_arm

        # Deselect all selected objects
        for obj in context.selected_objects:
            obj.select_set(False)

        # Select all of the temporary armatures
        for j, arm_obj in GM2ModelImporter.temp_arm_list.items():
            root_key = j
            arm_obj.select_set(True)

        # Combine all the armatures into one object
        context.view_layer.objects.active = GM2ModelImporter.temp_arm_list[root_key]
        bpy.ops.object.join()

        # Initialize the combined armature
        combined_armature = context.view_layer.objects.active
        combined_armature.name = "ROOT_armature"
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        # Switch to edit mode
        if context.active_object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        # Link all the bones to their parents
        all_bones = context.view_layer.objects.active.data.edit_bones
        for bone in bones:
            if bone.parent_obj is not None:
                all_bones[bone.data_obj.name].parent = all_bones[bone.parent_obj.name]

        # Switch to pose mode
        bpy.ops.object.mode_set(mode="POSE")

        # Set all pose bones on the armature to use Euler XYZ rotation
        p_bones = context.view_layer.objects.active.pose.bones
        for p_bone in p_bones:
            p_bone.rotation_mode = 'XYZ'

        # Switch to object mode
        bpy.ops.object.mode_set(mode="OBJECT")

        # Manually clear the temporary armature list
        GM2ModelImporter.temp_arm_list = {}

        if not self.display_tails:
            pose_bones = bpy.context.object.pose.bones

            # Apply the display model to the bones
            for bone in pose_bones:
                bone.custom_shape = bone_model
                bone.custom_shape_scale_xyz = tuple((self.imp_scale / 20, self.imp_scale / 20, self.imp_scale / 20))
                bone.use_custom_shape_bone_size = False

            # Switch to object mode
            bpy.ops.object.mode_set(mode="OBJECT")

            # Delete the sphere bone model
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[bone_model.name].select_set(True)
            bpy.ops.object.delete(use_global=False, confirm=False)

        return combined_armature

    # Cleans up Blender by deleting unneeded assets
    def cleanup_imported(self, context, m_info_list, root_armature):
        if self.import_models:
            # Deselect everything
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action='DESELECT')

            for m_info in m_info_list:
                if m_info.parent_obj is not None and m_info.parent_obj in GM2ModelImporter.junk_objs:
                    bpy.data.objects[GM2ModelImporter.obj_list[m_info.data_obj].name].select_set(True)

                    parent_name = GM2ModelImporter.obj_list[m_info.parent_obj].name
                    context.view_layer.objects.active = root_armature
                    root_armature.data.bones.active = root_armature.data.bones[parent_name]

                    bpy.ops.object.parent_set(type='BONE', keep_transform=True)

                    bpy.data.objects[GM2ModelImporter.obj_list[m_info.data_obj].name].select_set(False)

            # Clear the junk object list
            for junk_obj in GM2ModelImporter.junk_objs:
                GM2ModelImporter.junk_objs[junk_obj].data.user_clear()
                bpy.data.objects[GM2ModelImporter.junk_objs[junk_obj].name].select_set(True)

            GM2ModelImporter.junk_objs.clear()

            bpy.ops.object.delete(use_global=False, confirm=False)
