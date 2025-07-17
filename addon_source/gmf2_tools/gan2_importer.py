import math

import bpy
import struct
from bpy.types import Operator

from .target_game import GameTarget_Enum
from .target_game import TargetGame

from .gan2 import Gan2
from .action_creator import GA2ActionCreator


class ProcessedAnimObject:
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
        self.next_obj = _next_obj


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

        # Create a Blender action using the anim data
        GA2ActionCreator.create_action(self, context, end_frame, anim_name, objects)
