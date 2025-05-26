# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Gan2(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x47\x41\x4E\x32":
            raise kaitaistruct.ValidationNotEqualError(b"\x47\x41\x4E\x32", self.magic, self._io, u"/seq/0")
        self.version = self._io.read_u4be()
        self._unnamed2 = self._io.read_bytes(4)
        if not self._unnamed2 == b"\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed2, self._io, u"/seq/2")
        self.anim_time = self._io.read_u4le()
        self._unnamed4 = self._io.read_bytes(4)
        if not self._unnamed4 == b"\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed4, self._io, u"/seq/4")
        self.num_obj = self._io.read_u4le()
        self._unnamed6 = self._io.read_bytes(8)
        if not self._unnamed6 == b"\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed6, self._io, u"/seq/6")
        self.off_obj = self._io.read_u4le()
        self._unnamed8 = self._io.read_bytes(12)
        if not self._unnamed8 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed8, self._io, u"/seq/8")
        self.anim_objects = []
        for i in range(self.num_obj):
            self.anim_objects.append(Gan2.AnimObject(self._io, self, self._root))


    class U1Vector(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_u1()
            self.y = self._io.read_u1()
            self.z = self._io.read_u1()


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


    class FlVector4Le(KaitaiStruct):
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


    class FlVectorLe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()


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


    class AnimData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk_1 = self._io.read_u4be()
            self._unnamed1 = self._io.read_bytes(4)
            if not self._unnamed1 == b"\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed1, self._io, u"/types/anim_data/seq/1")
            self.unk_3 = self._io.read_u4le()
            self.block_count = self._io.read_u4le()
            self._unnamed4 = self._io.read_bytes(12)
            if not self._unnamed4 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed4, self._io, u"/types/anim_data/seq/4")
            self.block_offset_offset = self._io.read_u4le()
            self.unk_off_1 = self._io.read_u4le()
            self.unk_off_2 = self._io.read_u4le()
            self.unk_off_3 = self._io.read_u4le()
            if self.block_count == 6:
                self.unk_off_4 = self._io.read_u4le()

            if self.block_count == 6:
                self.unk_off_5 = self._io.read_u4le()

            if self.block_count == 6:
                self.unk_off_6 = self._io.read_u4le()

            if self.block_count == 6:
                self._unnamed12 = self._io.read_bytes(4)
                if not self._unnamed12 == b"\x00\x00\x00\x00":
                    raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed12, self._io, u"/types/anim_data/seq/12")

            self._unnamed13 = self._io.read_bytes(4)
            if not self._unnamed13 == b"\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed13, self._io, u"/types/anim_data/seq/13")
            self.anim_block_1 = Gan2.AnimBlock(self.unk_off_2, self._io, self, self._root)


    class AnimBlock(KaitaiStruct):
        def __init__(self, data_off, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.data_off = data_off
            self._read()

        def _read(self):
            self.unk_1 = self._io.read_u2le()
            self.block_id = self._io.read_u2le()
            self._unnamed2 = self._io.read_bytes(4)
            if not self._unnamed2 == b"\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed2, self._io, u"/types/anim_block/seq/2")
            self.unk_2 = self._io.read_u4le()
            self._unnamed4 = self._io.read_bytes(4)
            if not self._unnamed4 == b"\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed4, self._io, u"/types/anim_block/seq/4")
            self.unk_3 = self._io.read_u2le()
            self.unk_count = self._io.read_u2le()
            self.unk_4 = self._io.read_u2le()


    class AnimObject(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self._unnamed1 = self._io.read_bytes(8)
            if not self._unnamed1 == b"\x00\x00\x00\x00\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed1, self._io, u"/types/anim_object/seq/1")
            self.off_parent = self._io.read_u4le()
            self.off_first_child = self._io.read_u4le()
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.data_offset = self._io.read_u4le()
            self._unnamed7 = self._io.read_bytes(12)
            if not self._unnamed7 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed7, self._io, u"/types/anim_object/seq/7")

        @property
        def obj_anim_data(self):
            if hasattr(self, '_m_obj_anim_data'):
                return self._m_obj_anim_data

            if self.data_offset != 0:
                io = self._root._io
                _pos = io.pos()
                io.seek(self.data_offset)
                self._m_obj_anim_data = Gan2.AnimData(io, self, self._root)
                io.seek(_pos)

            return getattr(self, '_m_obj_anim_data', None)



