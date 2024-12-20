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

    """armature_mode: EnumProperty(
        name="Armature Import Mode",
        description="",
        items=(
            ('OPT_A', "Import mesh & armature", ""),
            ('OPT_B', "Import mesh only", "Won't import models parented to the armature (e.g. most faces)"),
            ('OPT_C', "Import armature only", "Will import models parented to the armature (e.g. most faces)"),
        ),
        default='OPT_A'
    )"""

    up_axis: EnumProperty(
        name="Up Axis",
        description="The up axis of the model you are trying to import. \nMess with this if your model imports in the wrong orientation.\n",
        items=(
            ('OPT_A', "X", ""),
            ('OPT_B', "Y", ""),
            ('OPT_C', "Z", ""),
        ),
        default='OPT_B'
    )

    smooth_shading: BoolProperty(
        name="Use Smooth Shading",
        description="Defaults the model to use 'smooth' shading instead of 'flat' shading. \nLeave this on in most cases",
        default=True
    )

    import_models: BoolProperty(
        name="Import Models & Armatures",
        description="",
        default=True
    )

    import_mats: BoolProperty(
        name="Import Materials & Textures",
        description="",
        default=True
    )

    def start_plugin(self, context, filepath):
        GM2ModelImporter.load_file_data(self, context, filepath)

    def execute(self, context):
        self.start_plugin(context, self.filepath)

        return {'FINISHED'}
