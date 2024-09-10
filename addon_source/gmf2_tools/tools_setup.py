import bpy

from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from bpy.props import BoolProperty, EnumProperty

from .gmf2_importer import GM2ModelImporter


class ToolsSetup(Operator, ImportHelper):
    bl_idname = "gm2_importer.setup"
    bl_label = "Import GMF2 model"

    index_override: EnumProperty(
        name="Face Index Override Mode",
        description="Forces the addon to load the model using a specific index format.\nMess with this if an object won't load using default settings.\n",
        items=(
            ('OPT_A', "No override", "Allows the addon to decide what format each model should use."),
            ('OPT_B', "9 byte format", ""),
            ('OPT_C', "9 byte format (extra data)", ""),
            ('OPT_D', "11 byte format", ""),
        ),
        default='OPT_A',
    )

    fix_coord_space: BoolProperty(
        name="Fix Coordinate Space",
        description="Forces the object to obey Blender's default coordinate space",
        default=False,
    )

    def start_plugin(self, context, filepath, idxMode):
        GM2ModelImporter.import_models(self, context, filepath, idxMode, self.fix_coord_space)

    def execute(self, context):
        self.start_plugin(context, self.filepath, self.index_override)

        return {'FINISHED'}
