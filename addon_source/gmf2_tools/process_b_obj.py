import bpy


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
        b_meshes = []

        v_buffers = {}

        if self.selected_only:
            b_objs = context.selected_objects
        else:
            b_objs = context.scene.objects

        for obj in b_objs:
            if type(obj.data) is bpy.types.Mesh:
                b_meshes.append(obj.data)

        # TODO: Triangulate all the mesh faces

        for mesh in b_meshes:
            verts = []

            for vertex in mesh.vertices:
                for axis in vertex.co:
                    verts.append(axis)

            v_buffers[mesh.name] = verts

            for tri in mesh.loop_triangles:
                for vertex in tri.vertices:
                    for axis in vertex.co:
                        # TODO: append all to a large array of ints
                        # TODO: append array to named collection
                        pass
