import bpy
from bpy.types import Operator
from .gct0 import Gct0
from .gct0_handler import GCTTextureHandler


class ExternalTextureToolbar(bpy.types.Panel):
    """toolbar for external textures"""
    bl_idname = "tex_toolbar.tex_panel"

    bl_category = "GMF2 Tools"
    bl_label = "External Texture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        """define the panel's layout"""
        layout = self.layout

        layout.operator("tex_toolbar.replace_texture")
        layout.operator("tex_toolbar.tex_cleanup")


class TextureReplacementOperator(Operator):
    bl_idname = "tex_toolbar.replace_texture"
    bl_label = "Replace Texture"

    replace_tex: bpy.props.StringProperty(
        name="Texture to replace",
        description=""
    )

    tex_path: bpy.props.StringProperty(
        name="Path to replacement",
        description="",
        subtype='FILE_PATH'
    )

    def draw(self, context):
        layout = self.layout
        layout.ui_units_x = 25

        layout.prop(self, "replace_tex")
        layout.prop(self, "tex_path")

        row = layout.row()
        row.label(text="Supported formats are: .BIN (GCT0), .GCT (GCT0), .bin (DXT1 DDS), .dds (DXT1 DDS)")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        gct0: Gct0 = Gct0.from_file(self.tex_path)
        GCTTextureHandler.create_texture_from_external(self, self.replace_tex, gct0)

        return {'FINISHED'}


class TextureCleanupOperator(Operator):
    bl_idname = "tex_toolbar.tex_cleanup"
    bl_label = "Cleanup Unused Textures"

    def draw(self, context):
        layout = self.layout

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):

        return {'FINISHED'}
