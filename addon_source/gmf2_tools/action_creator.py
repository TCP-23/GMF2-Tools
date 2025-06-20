import bpy

from bpy.types import Operator

class GA2ActionCreator(Operator):
    bl_idname = "gm2_importer.action_creator"
    bl_label = "Create GAN2 Action"

    # Creates a Blender action from provided GA2 anim data
    def create_action(self, context, end_frame, anim_name, anim_objects):
        if context.active_object.mode != "POSE":
            bpy.ops.object.mode_set(mode="POSE")

        new_action = bpy.data.actions.new(anim_name)

        active_arm = context.active_object

        active_arm.animation_data_create()
        active_arm.animation_data.action = new_action

        new_action.frame_end = end_frame

        for bone in active_arm.pose.bones:
            a_obj = None

            for anim_obj in anim_objects:
                if anim_obj.obj.name == bone.name:
                    a_obj = anim_obj
                    break

            if a_obj is not None:
                if a_obj.obj.obj_anim_data is not None:
                    if (a_obj.obj.obj_anim_data.pos_x_off != 0 or a_obj.obj.obj_anim_data.pos_y_off != 0
                            or a_obj.obj.obj_anim_data.pos_z_off != 0):
                        GA2ActionCreator.insert_channel(self, context, a_obj.obj.obj_anim_data.pos_x_block, "POS_X", bone)
                        GA2ActionCreator.insert_channel(self, context, a_obj.obj.obj_anim_data.pos_y_block, "POS_Y", bone)
                        GA2ActionCreator.insert_channel(self, context, a_obj.obj.obj_anim_data.pos_z_block, "POS_Z", bone)

    def insert_channel(self, context, blockData, channelName, bone):
        channel_index = 0
        anim_channel_frames = blockData.data_pair_count
        anim_action = context.active_object.animation_data.action
        anim_curve = None

        match channelName:
            case "POS_X":
                channel_index = 0
            case "POS_Y":
                channel_index = 1
            case "POS_Z":
                channel_index = 2

        if channel_index <= 3:
            if anim_curve is None:
                bone.location = (0.0, 0.0, 0.0)
                bone.keyframe_insert(data_path="location", frame=1, index=channel_index)

                for curve in anim_action.fcurves:
                    if curve.data_path == f'pose.bones["{bone.name}"].location':
                        if curve.array_index == channel_index:
                            anim_curve = curve

            GA2ActionCreator.insert_empty_keyframes(self, context, bone, anim_channel_frames, channel_index)

            for i, kf in enumerate(anim_curve.keyframe_points):
                context.scene.frame_current = int(kf.co[0])
                if blockData.unk_3 == 5:
                    GA2ActionCreator.insert_keyframe(self, context, bone, blockData.unk_3, blockData.data_pairs[i], channel_index)

    def insert_empty_keyframes(self, context, bone, kf_count, channel_index):
        frame_counter = 1

        context.scene.frame_current = 1

        if channel_index <= 3:
            bone.location = (0.0, 0.0, 0.0)

            for i in range(0, kf_count):
                bone.keyframe_insert(data_path="location", frame=frame_counter, index=channel_index)
                frame_counter += 1

    def insert_keyframe(self, context, bone, v_div, posData, channel_index):
        if channel_index <= 3:
            # (position_data / pow(2, unk_3)) * scale_factor
            # (position_data / pow(2, v_divisor)) * scale_factor
            # (-32625 / pow(2, 5)) * 0.1

            if v_div == 5:
                bone.location[channel_index] = (posData / pow(2, v_div)) * 0.1
            else:
                # Change this to our decoded position
                bone.location[channel_index] = 0.0

            bone.keyframe_insert(data_path="location", frame=context.scene.frame_current, index=channel_index)

    def set_interpolation(self, context):
        pass