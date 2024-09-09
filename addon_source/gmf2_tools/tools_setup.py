import bpy

from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from bpy.props import BoolProperty

from .gmf2_importer import GM2ModelImporter


class ToolsSetup(Operator, ImportHelper):
    bl_idname = "gm2_importer.setup"
    bl_label = "Setup GMF2 Tools"

    fix_coord_space: BoolProperty(
        name="Fix Coordinate Space",
        description="Forces the object to obey Blender's default coordinate space",
        default=False,
    )

    def start_plugin(self, context, filepath):
        GM2ModelImporter.import_models(self, context, filepath, self.fix_coord_space)

    def execute(self, context):
        self.start_plugin(context, self.filepath)

        return {'FINISHED'}
