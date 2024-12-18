#   GMF2 Tools, Blender addon that allows Blender to import GMF2 models

import bpy

from .tools_setup import ToolsSetup
from .gct0_handler import ExternalSuccessPopup
from .gct0_handler import ExternalTexturePopup


def menu_func_import(self, context):
    self.layout.operator(ToolsSetup.bl_idname, text="Grasshopper Manufacture Model (.gm2)")


def register():
    bpy.utils.register_class(ToolsSetup)
    bpy.utils.register_class(ExternalSuccessPopup)
    bpy.utils.register_class(ExternalTexturePopup)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ToolsSetup)
    bpy.utils.unregister_class(ExternalSuccessPopup)
    bpy.utils.unregister_class(ExternalTexturePopup)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
