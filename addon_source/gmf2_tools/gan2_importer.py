import bpy
import struct
from bpy.types import Operator

from .target_game import GameTarget_Enum
from .target_game import TargetGame

class GA2AnimImporter(Operator):
    bl_idname = "ga2_importer.anim_data"
    bl_label = "Import GAN2 animation"

    def load_file_data(self, context, filepath):
        pass