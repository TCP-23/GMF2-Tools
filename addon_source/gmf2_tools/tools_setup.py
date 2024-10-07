import bpy

from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from bpy.props import BoolProperty, StringProperty, EnumProperty

from .gmf2_importer import GM2ModelImporter


class ToolsSetup(Operator, ImportHelper):
    bl_idname = "gm2_importer.setup"
    bl_label = "Import GMF2 model"

    filter_glob: StringProperty(default="*.gm2", options={'HIDDEN'})

    index_override: EnumProperty(
        name="Face Index Override Mode",
        description="Forces the addon to load the model using a specific index format.\nMess with this if an object won't load using default settings.\n",
        items=(
            ('OPT_A', "No override", "Allows the addon to decide what format each model should use"),
            ('OPT_B', "Index format A", ""),
            ('OPT_C', "Index format B", ""),
            ('OPT_D', "Index format C", ""),
        ),
        default='OPT_A',
    )

    import_armature: EnumProperty(
        name="Armature Import Mode",
        description="",
        items=(
            ('OPT_A', "Import mesh & armature", ""),
            ('OPT_B', "Import mesh only", "Won't import models parented to the armature (e.g. most faces)"),
            ('OPT_C', "Import armature only", "Will import models parented to the armature (e.g. most faces)"),
        ),
        default='OPT_A'
    )

    fix_coord_space: BoolProperty(
        name="Fix Coordinate Space",
        description="Forces the object to obey Blender's default coordinate space",
        default=True,
    )

    smooth_shading: BoolProperty(
        name="Use Smooth Shading",
        description="",
        default=True,
    )

    dev_testing: BoolProperty(
        name="Enable Testing Features",
        description="Enables experimental features that are still being tested.\nProbably don't turn this on",
        default=False,
    )

    def start_plugin(self, context, filepath):
        GM2ModelImporter.set_import_variables(self, self.index_override, self.import_armature, self.fix_coord_space,
                                              self.smooth_shading, self.dev_testing)
        GM2ModelImporter.load_model_data(self, context, filepath)

    def execute(self, context):
        self.start_plugin(context, self.filepath)

        return {'FINISHED'}
