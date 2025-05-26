import bpy
import struct
from bpy.types import Operator

from .target_game import GameTarget_Enum
from .target_game import TargetGame

from .gan2 import Gan2

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

class GA2AnimImporter(Operator):
    bl_idname = "ga2_importer.anim_data"
    bl_label = "Import GAN2 animation"

    # animation rotation conversion formula
    # print((-32625 / pow(2, 5)) * 0.1)
    # print((-90 * pow(2, 5)) * 10)

    def load_file_data(self, context, filepath):
        ga2: Gan2 = Gan2.from_file(filepath)
