import bpy

from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from bpy.props import BoolProperty, StringProperty, EnumProperty

from .gmf2_importer import GM2ModelImporter
from .gan2_importer import GA2AnimImporter


class GMF2_Setup(Operator, ImportHelper):
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

    import_models: BoolProperty(
        name="Import Models & Armatures",
        description="Turn this off if you just want to load the textures into Blender",
        default=True
    )

    import_mats: BoolProperty(
        name="Import Materials & Textures",
        description="Turn this off if you don't care about textures, or want the models to load faster",
        default=True
    )

    import_normals: BoolProperty(
        name="Use Imported Normals",
        description="Use the normals that are packed into the model file",
        default=True
    )

    display_tails: BoolProperty(
        name="Display Bone Tails",
        description="Generate and display bone tails based on children",
        default=False
    )

    def start_plugin(self, context, filepath):
        GM2ModelImporter.load_file_data(self, context, filepath)

    def execute(self, context):
        self.start_plugin(context, self.filepath)

        return {'FINISHED'}


class FLCG_Setup(Operator, ImportHelper):
    bl_idname = "ghman_tools.gcl_setup"
    bl_label = "Import FLCG Model"

    filter_glob: StringProperty(default="*.gcl", options={'HIDDEN'})


class GAN2_Setup(Operator, ImportHelper):
    bl_idname = "ghman_tools.ga2_setup"
    bl_label = "Import GAN2 Anim"

    filter_glob: StringProperty(default="*.ga2", options={'HIDDEN'})

    def start_plugin(self, context, filepath):
        GA2AnimImporter.load_file_data(self, context, filepath)

    def execute(self, context):
        self.start_plugin(context, self.filepath)

        return {'FINISHED'}


class RMHG_Setup(Operator, ImportHelper):
    bl_idname = "ghman_tools.rsl_setup"
    bl_label = "Import RMHG Archive"

    filter_glob: StringProperty(default="*.rsl", options={'HIDDEN'})


class AddonWikiPanel(bpy.types.Panel):
    bl_idname = "addon_wiki.wiki"

    bl_category = "GMF2 Tools"
    bl_label = "Addon Instructions"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.url_open", text="Open Addon Instructions", icon='URL').url = "https://github.com/TCP-23/GMF2-Tools/wiki"