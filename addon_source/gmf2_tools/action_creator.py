import math

import bpy

from bpy.types import Operator

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
            else:
                self.is_child_obj = False

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

            if self.pos_x_block is not None or self.pos_y_block is not None or self.pos_z_block is not None:
                self.has_pos = True
            else:
                self.has_pos = False

            if self.rot_x_block is not None or self.rot_y_block is not None or self.rot_z_block is not None:
                self.has_rot = True
            else:
                self.has_rot = False
        else:
            self.has_anim_data = False
            self.is_child_obj = False
            self.has_pos = False
            self.has_rot = False


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


class GA2ActionCreator(Operator):
    bl_idname = "gm2_importer.action_creator"
    bl_label = "Create GAN2 Action"

    # Creates a Blender action from provided GA2 anim data
    def create_action(self, context, end_frame, anim_name, anim_objects):

        anim_obj_datas = []
        for anim_obj in anim_objects:
            is_first_child = False
            if anim_obj.parent_obj is not None:
                if anim_obj.parent_obj.off_parent == 0:
                    is_first_child = True

            anim_obj_datas.append(AnimObjInfo(anim_obj.obj, is_first_child))

        if context.active_object.mode != "POSE":
            bpy.ops.object.mode_set(mode="POSE")

        new_action = bpy.data.actions.new(anim_name)

        active_arm = context.active_object

        active_arm.animation_data_create()
        active_arm.animation_data.action = new_action

        new_action.frame_end = end_frame

        for bone in active_arm.pose.bones:
            a_obj_data = None

            for anim_obj_data in anim_obj_datas:
                if anim_obj_data.obj_name == bone.name:
                    a_obj_data = anim_obj_data

            if a_obj_data is not None:
                if a_obj_data.has_anim_data:
                    if a_obj_data.has_pos:
                        GA2ActionCreator.insert_channel(self, context, a_obj_data.pos_x_block, 'POS_X', bone, a_obj_data.is_child_obj)
                        GA2ActionCreator.insert_channel(self, context, a_obj_data.pos_y_block, 'POS_Y', bone, a_obj_data.is_child_obj)
                        GA2ActionCreator.insert_channel(self, context, a_obj_data.pos_z_block, 'POS_Z', bone, a_obj_data.is_child_obj)

                    if a_obj_data.has_rot:
                        GA2ActionCreator.insert_channel(self, context, a_obj_data.rot_x_block, 'ROT_X', bone, a_obj_data.is_child_obj)
                        GA2ActionCreator.insert_channel(self, context, a_obj_data.rot_y_block, 'ROT_Y', bone, a_obj_data.is_child_obj)
                        GA2ActionCreator.insert_channel(self, context, a_obj_data.rot_z_block, 'ROT_Z', bone, a_obj_data.is_child_obj)

    def insert_channel(self, context, blockData, channelName, bone, is_child_obj):
        channel_index = -1
        anim_channel_frames = blockData.data_pair_count
        anim_action = context.active_object.animation_data.action
        anim_curve = None

        match channelName:
            case 'POS_X':
                channel_index = 0
            case 'POS_Y':
                channel_index = 1
            case 'POS_Z':
                channel_index = 2
            case 'ROT_X':
                channel_index = 3
            case 'ROT_Y':
                channel_index = 4
            case 'ROT_Z':
                channel_index = 5

        if anim_curve is None:
            converted_chan_idx = GA2ActionCreator.convert_channel_index(self, context, channel_index, self.up_axis, is_child_obj)

            if channel_index <= 2:  # Position
                bone.location = (0.0, 0.0, 0.0)
                bone.keyframe_insert(data_path="location", frame=1, index=converted_chan_idx)

                for curve in anim_action.fcurves:
                    if curve.data_path == f'pose.bones["{bone.name}"].location':
                        if curve.array_index == converted_chan_idx:
                            anim_curve = curve

            elif channel_index <= 5:  # Rotation
                bone.rotation_euler = (0.0, 0.0, 0.0)
                bone.keyframe_insert(data_path="rotation_euler", frame=1, index=converted_chan_idx)

                for curve in anim_action.fcurves:
                    if curve.data_path == f'pose.bones["{bone.name}"].rotation_euler':
                        if curve.array_index == converted_chan_idx:
                            anim_curve = curve

        GA2ActionCreator.insert_empty_keyframes(self, context, bone, anim_channel_frames, channel_index, is_child_obj)

        # We have to manually increment the index because the length of the data_pairs array is 1 less than the
        # amount of keyframes in our curve.
        kf_index = 0
        for kf in anim_curve.keyframe_points:
            context.scene.frame_current = int(kf.co[0])
            GA2ActionCreator.insert_keyframe(self, context, bone, blockData.v_divisor, blockData.data_pairs[kf_index], channel_index, is_child_obj)

            kf_index += 1

    def insert_empty_keyframes(self, context, bone, kf_count, channel_index, is_child_obj):
        frame_counter = 1
        context.scene.frame_current = 1

        converted_chan_index = GA2ActionCreator.convert_channel_index(self, context, channel_index, self.up_axis, is_child_obj)

        if channel_index <= 2:
            bone.location = (1.5, 1.5, 1.5)

            for i in range(0, kf_count):
                bone.keyframe_insert(data_path="location", frame=frame_counter, index=converted_chan_index)
                frame_counter += 1
        elif channel_index <= 5:
            bone.rotation_euler = (math.radians(20.0), math.radians(20.0), math.radians(20.0))

            for i in range(0, kf_count):
                bone.keyframe_insert(data_path="rotation_euler", frame=frame_counter, index=converted_chan_index)
                frame_counter += 1

    def insert_keyframe(self, context, bone, v_div, vecData, channel_index, is_child_obj):
        converted_chan_index = GA2ActionCreator.convert_channel_index(self, context, channel_index, self.up_axis, is_child_obj)

        if channel_index <= 2:
            # (position_data / pow(2, unk_3)) * scale_factor
            # (position_data / pow(2, v_divisor)) * scale_factor
            # (-32625 / pow(2, 5)) * 0.1

            if v_div == 5:
                bone.location[converted_chan_index] = (vecData / pow(2, v_div)) * self.position_scale
            else:
                bone.location[converted_chan_index] = 0.0

            #bone.location[converted_chan_index] = (vecData / pow(2, v_div)) * 0.01

            bone.keyframe_insert(data_path="location", frame=context.scene.frame_current, index=converted_chan_index)
        elif channel_index <= 5:
            if v_div == 5:
                bone.rotation_euler[converted_chan_index] = math.radians((vecData / pow(2, v_div)) * self.rotation_scale)
            else:
                bone.rotation_euler[converted_chan_index] = 0.0
            bone.keyframe_insert(data_path="rotation_euler", frame=context.scene.frame_current, index=converted_chan_index)

    def set_interpolation(self, context):
        pass

    # Change this later
    def convert_channel_index(self, context, chan_index, up_axis, is_child_obj):
        converted_chan_idx = chan_index

        if up_axis == 'OPT_A':
            up_axis = 'UP_X'
        elif up_axis == 'OPT_B':
            up_axis = 'UP_Y'
        elif up_axis == 'OPT_C':
            up_axis = 'UP_Z'

        if not is_child_obj or self.axis_swap_children:
            if up_axis == 'UP_X':
                if chan_index == 0 or chan_index == 3:
                    converted_chan_idx = 1
                elif chan_index == 1 or chan_index == 4:
                    converted_chan_idx = 0
                elif chan_index == 2 or chan_index == 5:
                    converted_chan_idx = 2
            elif up_axis == 'UP_Y':
                if chan_index == 1 or chan_index == 4:
                    converted_chan_idx = 2
                elif chan_index == 2 or chan_index == 5:
                    converted_chan_idx = 1
                elif chan_index == 0 or chan_index == 3:
                    converted_chan_idx = 0
            elif up_axis == 'UP_Z':
                if chan_index == 0 or chan_index == 3:
                    converted_chan_idx = 0
                elif chan_index == 1 or chan_index == 4:
                    converted_chan_idx = 1
                elif chan_index == 2 or chan_index == 5:
                    converted_chan_idx = 2
        else:
            if chan_index == 0 or chan_index == 3:
                converted_chan_idx = 0
            elif chan_index == 1 or chan_index == 4:
                converted_chan_idx = 1
            elif chan_index == 2 or chan_index == 5:
                converted_chan_idx = 2

        return converted_chan_idx
