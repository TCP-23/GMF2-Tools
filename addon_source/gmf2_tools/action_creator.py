import bpy

from bpy.types import Operator

class GA2ActionCreator(Operator):
    bl_idname = "gm2_importer.action_creator"
    bl_label = "Create GAN2 Action"

    def create_action(self, context, end_frame, anim_name):
        new_action = bpy.data.actions.new(anim_name)

        context.active_object.animation_data_create()
        context.active_object.animation_data.action = new_action