import bpy
from .export_object import exportObjects
from .export_object import exportTextures
from .export_object import exportMaterials


def float_to_short(f):
    return None


def short_to_float(s):
    return None


def float_vector_to_short_vector(f_vector):
    return tuple((float_to_short(f_vector.x), float_to_short(f_vector.y), float_to_short(f_vector.z)))


def short_vector_to_float_vector(s_vector):
    return tuple((short_to_float(s_vector.x), short_to_float(s_vector.y), short_to_float(s_vector.z)))


class ProcessBObject(Operator):
    def get_objects(self, context):
        if self.selected_only:
            pass
        else:
            pass

    def get_meshes(self, context):
        b_objs = []

        if self.selected_only:
            b_objs = context.selected_objects
        else:
            b_objs = context.scene.objects

        for obj in b_objs:
            exportObjects[obj.name] = {}
            if type(obj.data) is bpy.types.Mesh:
                exportObjects[obj.name]["mesh"] = obj.data
                # TODO: Triangulate all the mesh faces

                verts = []
                for vertex in obj.data.vertices:
                    for axis in vertex.co:
                        verts.append(axis)

                exportObjects[obj.name]["v_buffer"] = verts

                tri_idxs = []
                for tri in obj.data.loop_triangles:
                    for vertex in tri.vertices:
                        # TODO: append array to named collection
                        tri_idxs.append(vertex.index)

                # TODO: add indices to exportObjects collection


class ProcessBTex(Operator):
    pass


class ProcessBMat(Operator):
    pass
