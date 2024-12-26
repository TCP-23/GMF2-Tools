#   GMF2 Tools, Blender addon that allows Blender to import GMF2 models

import bpy

from .tools_setup import ToolsSetup
from .tools_setup import AddonWikiPanel
from .texture_toolbar import ExternalTextureToolbar
from .texture_toolbar import TextureReplacementOperator
from .texture_toolbar import TextureCleanupOperator


def menu_func_import(self, context):
    self.layout.operator(ToolsSetup.bl_idname, text="Grasshopper Manufacture Model (.gm2)")


def register():
    bpy.utils.register_class(ToolsSetup)
    bpy.utils.register_class(AddonWikiPanel)
    bpy.utils.register_class(ExternalTextureToolbar)
    bpy.utils.register_class(TextureReplacementOperator)
    bpy.utils.register_class(TextureCleanupOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ToolsSetup)
    bpy.utils.unregister_class(AddonWikiPanel)
    bpy.utils.unregister_class(ExternalTextureToolbar)
    bpy.utils.unregister_class(TextureReplacementOperator)
    bpy.utils.unregister_class(TextureCleanupOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
