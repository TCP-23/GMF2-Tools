# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Gmf2(KaitaiStruct):
    """Grasshopper Manufacture
    No More Heroes world chunk
    GMF - Grasshopper Model File?
    Japanese text encoding.
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x47\x4D\x46\x32":
            raise kaitaistruct.ValidationNotEqualError(b"\x47\x4D\x46\x32", self.magic, self._io, u"/seq/0")
        self.version = self._io.read_u4le()
        if not self.version == 2:
            raise kaitaistruct.ValidationNotEqualError(2, self.version, self._io, u"/seq/1")
        self._unnamed2 = self._io.read_bytes(16)
        if not self._unnamed2 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed2, self._io, u"/seq/2")
        self.num_objects = self._io.read_u2le()
        self.num_textures = self._io.read_u2le()
        self._unnamed5 = self._io.read_bytes(2)
        if not self._unnamed5 == b"\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00", self._unnamed5, self._io, u"/seq/5")
        self.num_materials = self._io.read_u2le()
        self.off_objects = self._io.read_u4le()
        self.off_textures = self._io.read_u4le()
        self._unnamed9 = self._io.read_bytes(4)
        if not self._unnamed9 == b"\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed9, self._io, u"/seq/9")
        self.off_materials = self._io.read_u4le()
        self.unk_8 = self._io.read_u4le()
        self.unk_9 = self._io.read_u4le()
        self._unnamed13 = self._io.read_bytes(16)
        if not self._unnamed13 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed13, self._io, u"/seq/13")
        self._unnamed14 = self._io.read_bytes(16)
        if not self._unnamed14 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed14, self._io, u"/seq/14")
        self._unnamed15 = self._io.read_bytes(16)
        if not self._unnamed15 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed15, self._io, u"/seq/15")
        self._unnamed16 = self._io.read_bytes(8)
        if not self._unnamed16 == b"\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed16, self._io, u"/seq/16")
        if self.nmh2_identifier == 4294967295:
            self._unnamed17 = self._io.read_bytes(16)

        self.textures = []
        for i in range(self.num_textures):
            self.textures.append(Gmf2.Texture(self._io, self, self._root))

        self.materials = []
        for i in range(self.num_materials):
            self.materials.append(Gmf2.Material(self._io, self, self._root))

        self.world_objects = []
        for i in range(self.num_objects):
            self.world_objects.append(Gmf2.WorldObject(self._io.pos(), self._io, self, self._root))


    class WorldObject(KaitaiStruct):
        def __init__(self, off, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.off = off
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self.unk_0 = self._io.read_u4le()
            self.off_v_buf = self._io.read_u4le()
            self.off_parent = self._io.read_u4le()
            self.off_firstchild = self._io.read_u4le()
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.off_surf_list = self._io.read_u4le()
            self._unnamed8 = self._io.read_bytes(4)
            self.off_unk = self._io.read_u4le()
            self.v_divisor = self._io.read_s4le()
            self.origin = Gmf2.FlVector(self._io, self, self._root)
            self.unkf_a = self._io.read_f4le()
            self.unk_b = self._io.read_u4le()
            self.rot_y = self._io.read_f4le()
            self.rot_z = self._io.read_f4le()
            self.unkf_11 = self._io.read_f4le()
            self.scale = Gmf2.FlVector(self._io, self, self._root)
            self.off_data_c = self._io.read_u4le()
            self.cullbox_origin = Gmf2.FlVector(self._io, self, self._root)
            self.unkf_16 = self._io.read_f4le()
            self.cullbox_size = Gmf2.FlVector(self._io, self, self._root)
            self.unkf_1a = self._io.read_f4le()
            if self._root.nmh2_identifier == 4294967295:
                self.nmh2_unk_2 = self._io.read_bytes(64)


        class Surface(KaitaiStruct):
            """Headers are in a linked list.
            """
            def __init__(self, off_v_buf, v_divisor, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.off_v_buf = off_v_buf
                self.v_divisor = v_divisor
                self._read()

            def _read(self):
                self.off_prev = self._io.read_u4le()
                self.off_next = self._io.read_u4le()
                self.off_data = self._io.read_u4le()
                self.off_material = self._io.read_u4le()
                self.unk_4 = self._io.read_u2le()
                self.num_v = self._io.read_u2le()
                self.unk_5 = self._io.read_u4le()
                self.unk_6 = self._io.read_u2le()
                self.unk_7 = self._io.read_u2le()
                self.unk_8 = self._io.read_u2le()
                self.unk_9 = self._io.read_u2le()

            class Surfdata(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.data_size = self._io.read_u4be()
                    self.num_v_smthn_total = self._io.read_u2be()
                    self.unk_2 = self._io.read_u2be()
                    self._unnamed3 = self._io.read_bytes(8)
                    if not self._unnamed3 == b"\x00\x00\x00\x00\x00\x00\x00\x00":
                        raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed3, self._io, u"/types/world_object/types/surface/types/surfdata/seq/3")
                    self._unnamed4 = self._io.read_bytes(16)
                    if not self._unnamed4 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
                        raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed4, self._io, u"/types/world_object/types/surface/types/surfdata/seq/4")
                    self.data = self._io.read_bytes(self.data_size)


            class Tristrip(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.unk_0 = self._io.read_u2be()
                    if self.unk_0 == 153:
                        self.num_smthn = self._io.read_u2be()

                    if self.unk_0 == 153:
                        self.unk_1 = []
                        for i in range(self.num_smthn):
                            self.unk_1.append(Gmf2.WorldObject.Surface.Tristrip.I(self._io, self, self._root))



                class I(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.idx = self._io.read_u2be()
                        self.unk = self._io.read_bytes(9)



            @property
            def data(self):
                if hasattr(self, '_m_data'):
                    return self._m_data

                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_data)
                self._m_data = Gmf2.WorldObject.Surface.Surfdata(io, self, self._root)
                io.seek(_pos)
                return getattr(self, '_m_data', None)

            @property
            def v_buf(self):
                if hasattr(self, '_m_v_buf'):
                    return self._m_v_buf

                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_v_buf)
                self._m_v_buf = []
                for i in range(self.num_v):
                    _on = self.v_divisor
                    if _on == -1:
                        self._m_v_buf.append(Gmf2.FlVectorBe(io, self, self._root))
                    else:
                        self._m_v_buf.append(Gmf2.ShortVector(io, self, self._root))

                io.seek(_pos)
                return getattr(self, '_m_v_buf', None)


        @property
        def data_c(self):
            if hasattr(self, '_m_data_c'):
                return self._m_data_c

            if  ((self.off_data_c != 1065353216) and (self.off_data_c != 0)) :
                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_data_c)
                self._m_data_c = io.read_bytes(6)
                io.seek(_pos)

            return getattr(self, '_m_data_c', None)

        @property
        def surfaces(self):
            if hasattr(self, '_m_surfaces'):
                return self._m_surfaces

            if self.off_surf_list != 0:
                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_surf_list)
                self._m_surfaces = []
                i = 0
                while True:
                    _ = Gmf2.WorldObject.Surface(self.off_v_buf, self.v_divisor, io, self, self._root)
                    self._m_surfaces.append(_)
                    if _.off_next == 0:
                        break
                    i += 1
                io.seek(_pos)

            return getattr(self, '_m_surfaces', None)


    class Align(KaitaiStruct):
        """Byte alignment
        """
        def __init__(self, size, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.size = size
            self._read()

        def _read(self):
            self._unnamed0 = self._io.read_bytes(((self.size - self._io.pos()) % self.size))


    class FlVectorBe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4be()
            self.y = self._io.read_f4be()
            self.z = self._io.read_f4be()


    class ShortVector(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_s2be()
            self.y = self._io.read_s2be()
            self.z = self._io.read_s2be()


    class Material(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.unk_3 = self._io.read_u4le()
            self.off_data = self._io.read_u4le()
            self._unnamed5 = self._io.read_bytes(4)
            if not self._unnamed5 == b"\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed5, self._io, u"/types/material/seq/5")
            self._unnamed6 = self._io.read_bytes(4)
            if not self._unnamed6 == b"\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed6, self._io, u"/types/material/seq/6")

        class MaterialData(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self._unnamed0 = self._io.read_bytes(4)
                if not self._unnamed0 == b"\x00\x00\x00\x00":
                    raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed0, self._io, u"/types/material/types/material_data/seq/0")
                self.unk_0x04 = self._io.read_u4le()
                self.off_texture = self._io.read_u4le()
                self.unk_3 = self._io.read_u4le()
                self.shaderparams_a = Gmf2.FlVector4(self._io, self, self._root)
                self.shaderparams_b = Gmf2.FlVector4(self._io, self, self._root)


        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data

            io = self._root._io
            _pos = io.pos()
            io.seek(self.off_data)
            self._m_data = Gmf2.Material.MaterialData(io, self, self._root)
            io.seek(_pos)
            return getattr(self, '_m_data', None)


    class FlVector(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()


    class FlVector4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()
            self.w = self._io.read_f4le()


    class Texture(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.off_data = self._io.read_u4le()
            self.unk_0x14 = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.unk_str = (KaitaiStream.bytes_terminate(self._io.read_bytes(4), 0, False)).decode(u"SHIFT-JIS")

        @property
        def data(self):
            """GHM in-house texture format."""
            if hasattr(self, '_m_data'):
                return self._m_data

            io = self._root._io
            _pos = io.pos()
            io.seek(self.off_data)
            self._m_data = io.read_bytes(self.size)
            io.seek(_pos)
            return getattr(self, '_m_data', None)


    @property
    def nmh2_identifier(self):
        if hasattr(self, '_m_nmh2_identifier'):
            return self._m_nmh2_identifier

        _pos = self._io.pos()
        self._io.seek(112)
        self._m_nmh2_identifier = self._io.read_u4be()
        self._io.seek(_pos)
        return getattr(self, '_m_nmh2_identifier', None)


