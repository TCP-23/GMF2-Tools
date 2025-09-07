#   GMF2 Tools, Blender addon that allows Blender to import GMF2 models

import bpy

from .tools_setup import GMF2_Setup
from .tools_setup import FLCG_Setup
from .tools_setup import GAN2_Setup
from .tools_setup import RMHG_Setup
from .tools_setup import AddonWikiPanel
from .texture_toolbar import ExternalTextureToolbar
from .texture_toolbar import TextureReplacementOperator
from .texture_toolbar import TextureCleanupOperator


def menu_func_import(self, context):
    self.layout.operator(GMF2_Setup.bl_idname, text="Grasshopper Manufacture Model (.gm2)")
    #self.layout.operator(FLCG_Setup.bl_idname, text="Grasshopper Manufacture Collision Model (.gcl)")
    self.layout.operator(GAN2_Setup.bl_idname, text="Grasshopper Manufacture Animation (.ga2)")
    #self.layout.operator(RMHG_Setup.bl_idname, text="Grasshopper Manufacture Archive (.rsl)")


# Registers all operators to Blender
def register():
    bpy.utils.register_class(GMF2_Setup)
    bpy.utils.register_class(FLCG_Setup)
    bpy.utils.register_class(GAN2_Setup)
    bpy.utils.register_class(RMHG_Setup)
    bpy.utils.register_class(AddonWikiPanel)
    bpy.utils.register_class(ExternalTextureToolbar)
    bpy.utils.register_class(TextureReplacementOperator)
    bpy.utils.register_class(TextureCleanupOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


# Unregisters all operators from Blender
def unregister():
    bpy.utils.unregister_class(GMF2_Setup)
    bpy.utils.unregister_class(FLCG_Setup)
    bpy.utils.unregister_class(GAN2_Setup)
    bpy.utils.unregister_class(RMHG_Setup)
    bpy.utils.unregister_class(AddonWikiPanel)
    bpy.utils.unregister_class(ExternalTextureToolbar)
    bpy.utils.unregister_class(TextureReplacementOperator)
    bpy.utils.unregister_class(TextureCleanupOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
