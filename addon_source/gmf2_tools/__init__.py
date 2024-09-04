#   GMF2 Tools, Blender addon that allows Blender to import GMF2 models

import bpy

from .gmf2_importer import GM2ModelImporter
from .mesh_creator import GM2MeshCreator


def menu_func_import(self, context):
    self.layout.operator(GM2ModelImporter.bl_idname, text="No More Heroes Model (.gm2)")


def register():
    bpy.utils.register_class(GM2ModelImporter)
    bpy.utils.register_class(GM2MeshCreator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(GM2ModelImporter)
    bpy.utils.unregister_class(GM2MeshCreator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
