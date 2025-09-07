import math

import bpy
import struct
from bpy.types import Operator

from .target_game import GameTarget_Enum
from .target_game import TargetGame

from .gan2 import Gan2
from .action_creator import GA2ActionCreator


# Returns the name of an animation based on its filepath
def get_anim_name(anim_path):
    # TODO: Check operating system
    # The following code only works for Windows systems
    anim_name = str(anim_path).split('\\')[len(str(anim_path).split('\\'))-1].split('.')[0]
    return anim_name


def sort_objects(objs):
    sorted_objs = []

    # Loop through every object inside the provided list
    for i, anim_object in objs.items():
        parent, first_child, prev_obj, next_obj = None, None, None, None

        # Get references to linked objects
        if anim_object.off_parent in objs:
            parent = objs[anim_object.off_parent]
        if anim_object.off_first_child in objs:
            first_child = objs[anim_object.off_first_child]
        if anim_object.off_prev in objs:
            prev_obj = objs[anim_object.off_prev]
        if anim_object.off_next in objs:
            next_obj = objs[anim_object.off_next]

        # Create a ProcessedObject
        processed_obj = ProcessedAnimObject(anim_object, parent, first_child, prev_obj, next_obj)
        sorted_objs.append(processed_obj)

    return sorted_objs


def calculate_block_data_type(anim_data_block):
    data_type = 'NONE'

    match anim_data_block.block_id:
        case 0:
            data_type = 'POS_X'
        case 1:
            data_type = 'POS_Y'
        case 2:
            data_type = 'POS_Z'
        case 3:
            data_type = 'ROT_X'
        case 4:
            data_type = 'ROT_Y'
        case 5:
            data_type = 'ROT_Z'

    return data_type


class ProcessedAnimObject:
    obj = None
    parent_obj = None
    first_child_obj = None
    prev_obj = None
    next_obj = None

    is_first_child = False

    def __init__(self, _obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj):
        self.obj = _obj
        self.parent_obj = _parent_obj
        self.first_child_obj = _first_child_obj
        self.prev_obj = _prev_obj
        self.next_obj = _next_obj

        if self.parent_obj is not None and self.parent_obj.off_parent == 0:
            self.is_first_child = True


class AnimObjInfo:
    anim_obj = None
    obj_name = "NONE"
    has_anim_data = False
    has_pos = False
    has_rot = False
    is_child_obj = False

    pos_x_block = None
    pos_y_block = None
    pos_z_block = None
    rot_x_block = None
    rot_y_block = None
    rot_z_block = None

    def __init__(self, anim_obj, is_first_child):
        self.anim_obj = anim_obj
        self.obj_name = self.anim_obj.name

        if self.anim_obj.obj_anim_data is not None:
            self.has_anim_data = True

            if self.anim_obj.off_parent != 0 and not is_first_child:
                self.is_child_obj = True

            # We don't need to check if the first 3 blocks are null, because every object with valid obj_anim_data will
            # always have at least 3 blocks.

            b1_data_type = calculate_block_data_type(self.anim_obj.obj_anim_data.pos_x_block)
            b2_data_type = calculate_block_data_type(self.anim_obj.obj_anim_data.pos_y_block)
            b3_data_type = calculate_block_data_type(self.anim_obj.obj_anim_data.pos_z_block)
            b4_data_type = 'NONE'
            b5_data_type = 'NONE'
            b6_data_type = 'NONE'

            if self.anim_obj.obj_anim_data.block_count == 6:
                b4_data_type = calculate_block_data_type(self.anim_obj.obj_anim_data.rot_x_block)
                b5_data_type = calculate_block_data_type(self.anim_obj.obj_anim_data.rot_y_block)
                b6_data_type = calculate_block_data_type(self.anim_obj.obj_anim_data.rot_z_block)

            if b1_data_type == 'POS_X':
                self.pos_x_block = self.anim_obj.obj_anim_data.pos_x_block
            else:
                self.rot_x_block = self.anim_obj.obj_anim_data.pos_x_block
            if b2_data_type == 'POS_Y':
                self.pos_y_block = self.anim_obj.obj_anim_data.pos_y_block
            else:
                self.rot_y_block = self.anim_obj.obj_anim_data.pos_y_block
            if b3_data_type == 'POS_Z':
                self.pos_z_block = self.anim_obj.obj_anim_data.pos_z_block
            else:
                self.rot_z_block = self.anim_obj.obj_anim_data.pos_z_block

            # If an object has both position and rotation data, the position data will always come first.
            # Therefore, there is no need to perform an else check here.

            if b4_data_type == 'ROT_X':
                self.rot_x_block = self.anim_obj.obj_anim_data.rot_x_block
            if b5_data_type == 'ROT_Y':
                self.rot_y_block = self.anim_obj.obj_anim_data.rot_y_block
            if b6_data_type == 'ROT_Z':
                self.rot_z_block = self.anim_obj.obj_anim_data.rot_z_block

            # An object can't have only one or two channels in a set.
            # Because of this, we only need to check for one block in a set.

            if self.pos_x_block is not None:
                self.has_pos = True
            if self.rot_x_block is not None:
                self.has_rot = True


class GA2AnimImporter(Operator):
    bl_idname = "ga2_importer.anim_data"
    bl_label = "Import GAN2 animation"

    # animation rotation conversion formula
    # print((-32625 / pow(2, 5)) * 0.1)
    # print((-90 * pow(2, 5)) * 10)

    def load_file_data(self, context, filepath):
        # Read the data from the GA2 file, and create a variable to hold it
        ga2: Gan2 = Gan2.from_file(filepath)

        unsorted_objects = {}
        for i, anim_object in enumerate(ga2.anim_objects):
            unsorted_objects[anim_object.offset] = anim_object

        objects = sort_objects(unsorted_objects)
        obj_armature = None

        # Get the animation name from the filepath
        anim_name = get_anim_name(filepath)

        # Scale the animation end frame based on the framerate of the Blender scene
        # Remember to unscale the framerate before exporting
        end_frame = int(ga2.anim_time / 1000 * bpy.context.scene.render.fps)
        bpy.data.scenes["Scene"].frame_end = end_frame

        anim_obj_datas = []
        for anim_obj in objects:
            if anim_obj.parent_obj is None:
                print(f"Obj Name: {anim_obj.obj.name}. No parent!")
            else:
                print(f"Obj Name: {anim_obj.obj.name}. Parent is {anim_obj.parent_obj.name}.")
                if anim_obj.parent_obj.off_parent == 0:
                    print(f"Obj {anim_obj.obj.name} is the first child of {anim_obj.parent_obj.name}!")

            anim_obj_datas.append(AnimObjInfo(anim_obj.obj, anim_obj.is_first_child))

        # Create a Blender action using the anim data
        GA2ActionCreator.create_action(self, context, end_frame, anim_name, anim_obj_datas)
        
        GA2AnimImporter.cleanup_imported(self, context)

    def cleanup_imported(self, context):
        pass
