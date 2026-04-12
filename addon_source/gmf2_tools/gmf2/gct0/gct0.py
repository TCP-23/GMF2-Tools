# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Gct0(KaitaiStruct):

    class TextureEncoding(Enum):
        i4 = 0
        i8 = 1
        ia4 = 2
        ia8 = 3
        rgb565 = 4
        rgb5a3 = 5
        rgba32 = 6
        c4 = 8
        c8 = 9
        c14x2 = 10
        cmpr = 14
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x47\x43\x54\x30":
            raise kaitaistruct.ValidationNotEqualError(b"\x47\x43\x54\x30", self.magic, self._io, u"/seq/0")
        self._unnamed1 = self._io.read_bytes(2)
        if not self._unnamed1 == b"\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00", self._unnamed1, self._io, u"/seq/1")
        self.encoding = KaitaiStream.resolve_enum(Gct0.TextureEncoding, self._io.read_u2be())
        self.width = self._io.read_u2be()
        self.height = self._io.read_u2be()
        self.unk_1 = self._io.read_u1()
        self._unnamed6 = self._io.read_bytes(3)
        if not self._unnamed6 == b"\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00", self._unnamed6, self._io, u"/seq/6")
        self.data_offset = self._io.read_u4be()
        self._unnamed8 = self._io.read_bytes(8)
        if not self._unnamed8 == b"\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed8, self._io, u"/seq/8")
        self.unk_2 = self._io.read_u2be()
        self._unnamed10 = self._io.read_bytes(2)
        if not self._unnamed10 == b"\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00", self._unnamed10, self._io, u"/seq/10")
        self.unk_3 = self._io.read_u4be()
        self._unnamed12 = self._io.read_bytes(12)
        if not self._unnamed12 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed12, self._io, u"/seq/12")
        self._unnamed13 = self._io.read_bytes(16)
        if not self._unnamed13 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed13, self._io, u"/seq/13")
        self.texture_data = self._io.read_bytes_full()


