import math

import bpy

from bpy.types import Operator


def check_transform_type(chan_index, data_form_flag):
    transform_type = 'NONE'

    if chan_index <= 2:
        #if data_form_flag == 4:
            #transform_type = 'ROT'
        #else:
            #transform_type = 'POS'
        transform_type = 'POS'
    elif chan_index <= 5:
        #if data_form_flag == 4:
            #transform_type = 'POS'
        #else:
            #transform_type = 'ROT'
        transform_type = 'ROT'

    if data_form_flag != 5:
        transform_type = 'INVALID'

    return transform_type


def gan2_rot_to_rad(gan2_rot):
    scale_factor = 32767 / math.pi
    rad_rot = ((gan2_rot / math.pi) / scale_factor) * math.pi

    return rad_rot


def rad_to_gan2_rot(rad_rot):
    scale_factor = 32767
    gan2_rot = rad_rot * scale_factor

    return gan2_rot


def gan2_rot_to_deg(gan2_rot):
    rad_rot = gan2_rot_to_rad(gan2_rot)

    return rad_rot * (180 / math.pi)


def deg_to_gan2_rot(deg_rot):
    rad_rot = deg_rot * (math.pi / 180)

    return rad_to_gan2_rot(rad_rot)


class GA2ActionCreator(Operator):
    bl_idname = "gm2_importer.action_creator"
    bl_label = "Create GAN2 Action"

    # Creates a Blender action from provided GA2 anim data
    def create_action(self, context, end_frame, anim_name, anim_obj_datas):
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

        converted_chan_idx = GA2ActionCreator.convert_channel_index(self, context, channel_index, self.up_axis, is_child_obj)
        transform_type = check_transform_type(channel_index, blockData.v_divisor)

        if transform_type == 'INVALID':
            return

        if anim_curve is None:
            if transform_type == 'POS':  # Position
                bone.location = (0.0, 0.0, 0.0)
                bone.keyframe_insert(data_path="location", frame=1, index=converted_chan_idx)

                for curve in anim_action.fcurves:
                    if curve.data_path == f'pose.bones["{bone.name}"].location':
                        if curve.array_index == converted_chan_idx:
                            anim_curve = curve

            elif transform_type == 'ROT':  # Rotation
                bone.rotation_euler = (0.0, 0.0, 0.0)
                bone.keyframe_insert(data_path="rotation_euler", frame=1, index=converted_chan_idx)

                for curve in anim_action.fcurves:
                    if curve.data_path == f'pose.bones["{bone.name}"].rotation_euler':
                        if curve.array_index == converted_chan_idx:
                            anim_curve = curve

        #GA2ActionCreator.insert_empty_keyframes(self, context, bone, anim_channel_frames, channel_index, is_child_obj)
        GA2ActionCreator.insert_empty_keyframes(self, context, bone, anim_channel_frames, converted_chan_idx, transform_type)

        # We have to manually increment the index because the length of the data_pairs array is 1 less than the
        # amount of keyframes in our curve.
        kf_index = 0
        for kf in anim_curve.keyframe_points:
            context.scene.frame_current = int(kf.co[0])
            GA2ActionCreator.insert_keyframe(self, context, bone, blockData.v_divisor, blockData.data_pairs[kf_index],
                                             converted_chan_idx, transform_type)

            kf_index += 1

    def insert_empty_keyframes(self, context, bone, kf_count, converted_chan_index, transform_type):
        frame_counter = 1
        context.scene.frame_current = 1

        if transform_type == 'POS':
            #bone.location = (1.5, 1.5, 1.5)

            for i in range(0, kf_count):
                bone.keyframe_insert(data_path="location", frame=frame_counter, index=converted_chan_index)
                frame_counter += 1
        elif transform_type == 'ROT':
            #bone.rotation_euler = (math.radians(20.0), math.radians(20.0), math.radians(20.0))

            for i in range(0, kf_count):
                bone.keyframe_insert(data_path="rotation_euler", frame=frame_counter, index=converted_chan_index)
                frame_counter += 1

    def insert_keyframe(self, context, bone, v_div, vecData, converted_chan_index, transform_type):
        if transform_type == 'POS':
            # Might not actually be v_divisor, the location may be derived from a matrix space, similar to rotation
            # bone.location[converted_chan_index] = (vecData / pow(2, v_div)) * self.position_scale
            bone.location[converted_chan_index] = (vecData / pow(2, v_div)) * self.position_scale

            bone.keyframe_insert(data_path="location", frame=context.scene.frame_current, index=converted_chan_index)
        elif transform_type == 'ROT':
            bone.rotation_euler[converted_chan_index] = gan2_rot_to_rad(vecData)
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
