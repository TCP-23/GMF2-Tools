# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO

from .tme import Tme


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Gmf2b(KaitaiStruct):
    """Planned to be merged into the main gmf2.ksy file soon.
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Gmf2b, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.magic = (self._io.read_bytes(4)).decode(u"Shift_JIS")
        if not  ((self.magic == u"GMF2") or (self.magic == u"GM2F") or (self.magic == u"GMDF")) :
            raise kaitaistruct.ValidationNotAnyOfError(self.magic, self._io, u"/seq/0")
        self.version = self._io.read_u4le()
        if not self.version == 2:
            raise kaitaistruct.ValidationNotEqualError(2, self.version, self._io, u"/seq/1")
        self._unnamed2 = self._io.read_bytes(16)
        self.num_objects = self._io.read_u2le()
        self.num_textures = self._io.read_u2le()
        self.unused_0x1c = self._io.read_u2le()
        if not self.unused_0x1c == 0:
            raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x1c, self._io, u"/seq/5")
        self.num_materials = self._io.read_u2le()
        self.off_objects = self._io.read_u4le()
        self.off_textures = self._io.read_u4le()
        if not self.off_textures == 112:
            raise kaitaistruct.ValidationNotEqualError(112, self.off_textures, self._io, u"/seq/8")
        self.unused_0x28 = self._io.read_u4le()
        if not self.unused_0x28 == 0:
            raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x28, self._io, u"/seq/9")
        self.off_materials = self._io.read_u4le()
        self.unk_0x30 = self._io.read_u4le()
        self.unk_0x34 = self._io.read_u4le()
        self._unnamed13 = self._io.read_bytes(56)
        self.textures = []
        for i in range(self.num_textures):
            self.textures.append(Gmf2b.Texture(self._io.pos(), self._io, self, self._root))

        self.materials = []
        for i in range(self.num_materials):
            self.materials.append(Gmf2b.Material(self._io.pos(), self._io, self, self._root))

        self.world_objects = []
        for i in range(self.num_objects):
            self.world_objects.append(Gmf2b.WorldObject(self._io.pos(), i, self._io, self, self._root))



    def _fetch_instances(self):
        pass
        for i in range(len(self.textures)):
            pass
            self.textures[i]._fetch_instances()

        for i in range(len(self.materials)):
            pass
            self.materials[i]._fetch_instances()

        for i in range(len(self.world_objects)):
            pass
            self.world_objects[i]._fetch_instances()


    class FlVector4Le(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Gmf2b.FlVector4Le, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()
            self.w = self._io.read_f4le()


        def _fetch_instances(self):
            pass


    class FlVectorBe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Gmf2b.FlVectorBe, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.x = self._io.read_f4be()
            self.y = self._io.read_f4be()
            self.z = self._io.read_f4be()


        def _fetch_instances(self):
            pass


    class FlVectorLe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Gmf2b.FlVectorLe, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()


        def _fetch_instances(self):
            pass


    class Material(KaitaiStruct):
        """A LOT of this material information is inaccurate,
        particularly involving the shadow ramps.
        Update this soon.
        """
        def __init__(self, offset, _io, _parent=None, _root=None):
            super(Gmf2b.Material, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"Shift_JIS")
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.unk_3 = self._io.read_u4le()
            self.off_data = self._io.read_u4le()
            self._unnamed5 = self._io.read_bytes(8)


        def _fetch_instances(self):
            pass
            _ = self.data
            if hasattr(self, '_m_data'):
                pass
                self._m_data._fetch_instances()


        class MaterialData(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                super(Gmf2b.Material.MaterialData, self).__init__(_io)
                self._parent = _parent
                self._root = _root
                self._read()

            def _read(self):
                self.unused_0x00 = self._io.read_u4le()
                if not self.unused_0x00 == 0:
                    raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x00, self._io, u"/types/material/types/material_data/seq/0")
                self.off_ramp_data = self._io.read_u4le()
                self.off_main_tex = self._io.read_u4le()
                self.unk_0xc = self._io.read_u4le()
                self.shaderparams_main_a = Gmf2b.FlVector4Le(self._io, self, self._root)
                self.shaderparams_main_tint = Gmf2b.FlVector4Le(self._io, self, self._root)
                self.off_main_data = self._io.read_u4le()
                self.unk_0x34 = self._io.read_u4le()
                self.off_ramp_tex = self._io.read_u4le()
                self.unk_0x3c = self._io.read_u4le()
                self.shaderparams_ramp_a = Gmf2b.FlVector4Le(self._io, self, self._root)
                self.shaderparams_ramp_tint = Gmf2b.FlVector4Le(self._io, self, self._root)


            def _fetch_instances(self):
                pass
                self.shaderparams_main_a._fetch_instances()
                self.shaderparams_main_tint._fetch_instances()
                self.shaderparams_ramp_a._fetch_instances()
                self.shaderparams_ramp_tint._fetch_instances()


        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data

            io = self._root._io
            _pos = io.pos()
            io.seek(self.off_data)
            self._m_data = Gmf2b.Material.MaterialData(io, self, self._root)
            io.seek(_pos)
            return getattr(self, '_m_data', None)


    class ShortVector(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Gmf2b.ShortVector, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.x = self._io.read_s2be()
            self.y = self._io.read_s2be()
            self.z = self._io.read_s2be()


        def _fetch_instances(self):
            pass


    class Texture(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            super(Gmf2b.Texture, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"Shift_JIS")
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.off_data = self._io.read_u4le()
            self.unk_0x14 = self._io.read_u4le()
            self.unused_0x18 = self._io.read_u4le()
            if not self.unused_0x18 == 0:
                raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x18, self._io, u"/types/texture/seq/5")
            self.unk_string = (KaitaiStream.bytes_terminate(self._io.read_bytes(4), 0, False)).decode(u"Shift_JIS")


        def _fetch_instances(self):
            pass
            _ = self.texture_data
            if hasattr(self, '_m_texture_data'):
                pass
                self._m_texture_data._fetch_instances()


        @property
        def texture_data(self) -> Tme:
            if hasattr(self, '_m_texture_data'):
                return self._m_texture_data

            io = self._root._io
            _pos = io.pos()
            io.seek(self.off_data)
            self._m_texture_data = Tme(io)
            io.seek(_pos)
            return getattr(self, '_m_texture_data', None)


    class U1Vector(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Gmf2b.U1Vector, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.x = self._io.read_u1()
            self.y = self._io.read_u1()
            self.z = self._io.read_u1()


        def _fetch_instances(self):
            pass


    class WorldObject(KaitaiStruct):
        """Please remember to figure out how to actually grab the proper strips.
        Please.
        
        Most of the bone/skin weighting data is incorrect.
        Update soon.
        """
        def __init__(self, offset, obj_idx, _io, _parent=None, _root=None):
            super(Gmf2b.WorldObject, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.offset = offset
            self.obj_idx = obj_idx
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"Shift_JIS")
            self.flags = self._io.read_u4le()
            self.unused_0x0c = self._io.read_u4le()
            if not self.unused_0x0c == 0:
                raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x0c, self._io, u"/types/world_object/seq/2")
            self.off_parent = self._io.read_u4le()
            self.off_first_child = self._io.read_u4le()
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.off_surfaces = self._io.read_u4le()
            self.unk_0x24 = self._io.read_f4le()
            self.off_first_bone = self._io.read_u4le()
            self.unused_0x2c = self._io.read_u4le()
            if not self.unused_0x2c == 0:
                raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x2c, self._io, u"/types/world_object/seq/10")
            self.position = Gmf2b.FlVector4Le(self._io, self, self._root)
            self.rotation = Gmf2b.FlVector4Le(self._io, self, self._root)
            self.scale = Gmf2b.FlVector4Le(self._io, self, self._root)
            self.cullbox_position = Gmf2b.FlVector4Le(self._io, self, self._root)
            self.cullbox_size = Gmf2b.FlVector4Le(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.position._fetch_instances()
            self.rotation._fetch_instances()
            self.scale._fetch_instances()
            self.cullbox_position._fetch_instances()
            self.cullbox_size._fetch_instances()
            _ = self.surfaces
            if hasattr(self, '_m_surfaces'):
                pass
                for i in range(len(self._m_surfaces)):
                    pass
                    self._m_surfaces[i]._fetch_instances()



        class Surface(KaitaiStruct):
            def __init__(self, offset, surf_idx, _io, _parent=None, _root=None):
                super(Gmf2b.WorldObject.Surface, self).__init__(_io)
                self._parent = _parent
                self._root = _root
                self.offset = offset
                self.surf_idx = surf_idx
                self._read()

            def _read(self):
                self.off_prev = self._io.read_u4le()
                self.off_next = self._io.read_u4le()
                self.off_data = self._io.read_u4le()
                self.off_material = self._io.read_u4le()
                self.unk_0x10 = self._io.read_u4le()
                self.off_skin_data = self._io.read_u4le()
                self.unused_0x1c = self._io.read_bytes(8)


            def _fetch_instances(self):
                pass
                _ = self.data_strips
                if hasattr(self, '_m_data_strips'):
                    pass
                    for i in range(len(self._m_data_strips)):
                        pass
                        self._m_data_strips[i]._fetch_instances()


                _ = self.skin_data
                if hasattr(self, '_m_skin_data'):
                    pass
                    self._m_skin_data._fetch_instances()


            class SkinningData(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    super(Gmf2b.WorldObject.Surface.SkinningData, self).__init__(_io)
                    self._parent = _parent
                    self._root = _root
                    self._read()

                def _read(self):
                    self.off_prev = self._io.read_u4le()
                    self.off_next = self._io.read_u4le()
                    self.off_data = self._io.read_u4le()
                    self.unused_0x0c = self._io.read_u4be()
                    if not self.unused_0x0c == 0:
                        raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x0c, self._io, u"/types/world_object/types/surface/types/skinning_data/seq/3")


                def _fetch_instances(self):
                    pass
                    _ = self.ub
                    if hasattr(self, '_m_ub'):
                        pass
                        for i in range(len(self._m_ub)):
                            pass
                            self._m_ub[i]._fetch_instances()



                class UnkBinding02(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        super(Gmf2b.WorldObject.Surface.SkinningData.UnkBinding02, self).__init__(_io)
                        self._parent = _parent
                        self._root = _root
                        self._read()

                    def _read(self):
                        self.off_prev = self._io.read_u4le()
                        self.off_next = self._io.read_u4le()
                        self.off_data = self._io.read_u4le()
                        self.unused_0x0c = self._io.read_u4be()
                        if not self.unused_0x0c == 0:
                            raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x0c, self._io, u"/types/world_object/types/surface/types/skinning_data/types/unk_binding_02/seq/3")


                    def _fetch_instances(self):
                        pass
                        _ = self.weight_binds
                        if hasattr(self, '_m_weight_binds'):
                            pass
                            for i in range(len(self._m_weight_binds)):
                                pass
                                self._m_weight_binds[i]._fetch_instances()



                    class BoneWeightBinding(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            super(Gmf2b.WorldObject.Surface.SkinningData.UnkBinding02.BoneWeightBinding, self).__init__(_io)
                            self._parent = _parent
                            self._root = _root
                            self._read()

                        def _read(self):
                            self.off_prev = self._io.read_u4le()
                            self.off_next = self._io.read_u4le()
                            self.off_bone = self._io.read_u4le()
                            self.weight_strength = self._io.read_f4le()


                        def _fetch_instances(self):
                            pass


                    @property
                    def weight_binds(self):
                        if hasattr(self, '_m_weight_binds'):
                            return self._m_weight_binds

                        io = self._root._io
                        _pos = io.pos()
                        io.seek(self.off_data)
                        self._m_weight_binds = []
                        i = 0
                        while True:
                            _ = Gmf2b.WorldObject.Surface.SkinningData.UnkBinding02.BoneWeightBinding(io, self, self._root)
                            self._m_weight_binds.append(_)
                            if _.off_next == 0:
                                break
                            i += 1
                        io.seek(_pos)
                        return getattr(self, '_m_weight_binds', None)


                @property
                def ub(self):
                    if hasattr(self, '_m_ub'):
                        return self._m_ub

                    io = self._root._io
                    _pos = io.pos()
                    io.seek(self.off_data)
                    self._m_ub = []
                    i = 0
                    while True:
                        _ = Gmf2b.WorldObject.Surface.SkinningData.UnkBinding02(io, self, self._root)
                        self._m_ub.append(_)
                        if _.off_next == 0:
                            break
                        i += 1
                    io.seek(_pos)
                    return getattr(self, '_m_ub', None)


            class SurfaceData(KaitaiStruct):
                def __init__(self, offset, _io, _parent=None, _root=None):
                    super(Gmf2b.WorldObject.Surface.SurfaceData, self).__init__(_io)
                    self._parent = _parent
                    self._root = _root
                    self.offset = offset
                    self._read()

                def _read(self):
                    self._unnamed0 = self._io.read_bytes(8)
                    self.off_prevstrip = self._io.read_u4le()
                    self.unk_0x0c = self._io.read_u2le()
                    if not self.unk_0x0c == 32768:
                        raise kaitaistruct.ValidationNotEqualError(32768, self.unk_0x0c, self._io, u"/types/world_object/types/surface/types/surface_data/seq/2")
                    self.unk_0x0e = self._io.read_u2le()
                    self.count = self._io.read_u4le()
                    self.dir_val = self._io.read_u4le()
                    self.unused_0x18 = self._io.read_u8be()
                    if not self.unused_0x18 == 0:
                        raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x18, self._io, u"/types/world_object/types/surface/types/surface_data/seq/6")
                    self.vertices: list[Gmf2b.WorldObject.Surface.SurfaceData.Vertex] = []
                    for i in range(self.count):
                        self.vertices.append(Gmf2b.WorldObject.Surface.SurfaceData.Vertex(self._io, self, self._root))

                    self.unk_1 = self._io.read_u4be()
                    if not self.unk_1 == 17:
                        raise kaitaistruct.ValidationNotEqualError(17, self.unk_1, self._io, u"/types/world_object/types/surface/types/surface_data/seq/8")
                    self.unk_2 = self._io.read_u4be()
                    if not self.unk_2 == 23:
                        raise kaitaistruct.ValidationNotEqualError(23, self.unk_2, self._io, u"/types/world_object/types/surface/types/surface_data/seq/9")
                    self._unnamed10 = self._io.read_bytes(8)


                def _fetch_instances(self):
                    pass
                    for i in range(len(self.vertices)):
                        pass
                        self.vertices[i]._fetch_instances()

                    _ = self.is_final_strip
                    if hasattr(self, '_m_is_final_strip'):
                        pass
                        self._m_is_final_strip._fetch_instances()


                class DataEndCalc(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        super(Gmf2b.WorldObject.Surface.SurfaceData.DataEndCalc, self).__init__(_io)
                        self._parent = _parent
                        self._root = _root
                        self._read()

                    def _read(self):
                        pass


                    def _fetch_instances(self):
                        pass
                        _ = self.sentinel_check
                        if hasattr(self, '_m_sentinel_check'):
                            pass


                    @property
                    def ending_pos(self):
                        if hasattr(self, '_m_ending_pos'):
                            return self._m_ending_pos

                        self._m_ending_pos = (self._parent.offset + 48) + 64 * self._parent.count
                        return getattr(self, '_m_ending_pos', None)

                    @property
                    def is_final(self):
                        if hasattr(self, '_m_is_final'):
                            return self._m_is_final

                        self._m_is_final = (self._parent._parent._parent.surfaces[self._parent._parent.surf_idx + 1].off_data == self.ending_pos if self.is_final_surf_of_obj == False else (True if self.ending_pos == self._io.size() else self.sentinel_check != 0))
                        return getattr(self, '_m_is_final', None)

                    @property
                    def is_final_surf_of_obj(self):
                        if hasattr(self, '_m_is_final_surf_of_obj'):
                            return self._m_is_final_surf_of_obj

                        self._m_is_final_surf_of_obj = len(self._parent._parent._parent.surfaces) == self._parent._parent.surf_idx + 1
                        return getattr(self, '_m_is_final_surf_of_obj', None)

                    @property
                    def sentinel_check(self):
                        if hasattr(self, '_m_sentinel_check'):
                            return self._m_sentinel_check

                        if self.ending_pos != self._io.size():
                            pass
                            io = self._root._io
                            _pos = io.pos()
                            io.seek(self.ending_pos + 8)
                            self._m_sentinel_check = io.read_u4le()
                            io.seek(_pos)

                        return getattr(self, '_m_sentinel_check', None)


                class Vertex(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        super(Gmf2b.WorldObject.Surface.SurfaceData.Vertex, self).__init__(_io)
                        self._parent = _parent
                        self._root = _root
                        self._read()

                    def _read(self):
                        self.position = Gmf2b.FlVectorLe(self._io, self, self._root)
                        self.unk_0x0c = self._io.read_f4le()
                        self.unk_0x10 = Gmf2b.FlVectorLe(self._io, self, self._root)
                        self.unused_0x1c = self._io.read_u4be()
                        if not self.unused_0x1c == 0:
                            raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x1c, self._io, u"/types/world_object/types/surface/types/surface_data/types/vertex/seq/3")
                        self.unk_0x20 = self._io.read_f4le()
                        self.unk_0x24 = self._io.read_f4le()
                        self.unk_0x28 = self._io.read_f4le()
                        self.unk_0x2c = self._io.read_f4le()
                        self.u = self._io.read_f4le()
                        self.v_tex = self._io.read_f4le()
                        self.unk_0x38 = self._io.read_f4le()
                        if not self.unk_0x38 == 1:
                            raise kaitaistruct.ValidationNotEqualError(1, self.unk_0x38, self._io, u"/types/world_object/types/surface/types/surface_data/types/vertex/seq/10")
                        self.unused_0x3c = self._io.read_u4be()
                        if not self.unused_0x3c == 0:
                            raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x3c, self._io, u"/types/world_object/types/surface/types/surface_data/types/vertex/seq/11")


                    def _fetch_instances(self):
                        pass
                        self.position._fetch_instances()
                        self.unk_0x10._fetch_instances()

                    @property
                    def v(self):
                        if hasattr(self, '_m_v'):
                            return self._m_v

                        self._m_v = 1 - self.v_tex
                        return getattr(self, '_m_v', None)


                @property
                def is_final_strip(self):
                    if hasattr(self, '_m_is_final_strip'):
                        return self._m_is_final_strip

                    self._m_is_final_strip = Gmf2b.WorldObject.Surface.SurfaceData.DataEndCalc(self._io, self, self._root)
                    return getattr(self, '_m_is_final_strip', None)


            @property
            def data_strips(self) -> list[SurfaceData | None]:
                if hasattr(self, '_m_data_strips'):
                    return self._m_data_strips

                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_data)
                self._m_data_strips = []
                i = 0
                while True:
                    _ = Gmf2b.WorldObject.Surface.SurfaceData(self._io.pos(), io, self, self._root)
                    self._m_data_strips.append(_)
                    if _.is_final_strip.is_final == True:
                        break
                    i += 1
                io.seek(_pos)
                return getattr(self, '_m_data_strips', None)

            @property
            def skin_data(self) -> SkinningData | None:
                if hasattr(self, '_m_skin_data'):
                    return self._m_skin_data

                if self.off_skin_data != 0:
                    pass
                    io = self._root._io
                    _pos = io.pos()
                    io.seek(self.off_skin_data)
                    self._m_skin_data = Gmf2b.WorldObject.Surface.SkinningData(io, self, self._root)
                    io.seek(_pos)

                return getattr(self, '_m_skin_data', None)


        @property
        def surfaces(self) -> list[Surface | None]:
            if hasattr(self, '_m_surfaces'):
                return self._m_surfaces

            if self.off_surfaces != 0:
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_surfaces)
                self._m_surfaces = []
                i = 0
                while True:
                    _ = Gmf2b.WorldObject.Surface(self._io.pos(), i, io, self, self._root)
                    self._m_surfaces.append(_)
                    if _.off_next == 0:
                        break
                    i += 1
                io.seek(_pos)

            return getattr(self, '_m_surfaces', None)



