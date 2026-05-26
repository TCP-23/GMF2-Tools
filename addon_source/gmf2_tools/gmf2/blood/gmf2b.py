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
            self.world_objects.append(Gmf2b.WorldObject(self._io.pos(), self._io, self, self._root))



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
        """Most of the bone/skin weighting data is incorrect.
        Update soon.
        """
        def __init__(self, offset, _io, _parent=None, _root=None):
            super(Gmf2b.WorldObject, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"Shift_JIS")
            self.flags = self._io.read_u4le()
            self.off_v_buf = self._io.read_u4le()
            self.off_parent = self._io.read_u4le()
            self.off_first_child = self._io.read_u4le()
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.off_surfaces = self._io.read_u4le()
            self.unk_0x24 = self._io.read_f4le()
            self.off_first_bone = self._io.read_u4le()
            self.v_divisor = self._io.read_u4le()
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



