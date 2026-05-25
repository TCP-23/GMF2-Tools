# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class BloodTex(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(BloodTex, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.unparsed_1 = self._io.read_bytes(4)
        self._unnamed1 = self._io.read_bytes(4)
        self.unparsed_2 = self._io.read_bytes(2)
        self.csm_flags = self._io.read_u1()
        self.unparsed_3 = self._io.read_bytes(53)
        self.img_width = self._io.read_u4le()
        self.img_height = self._io.read_u4le()
        self.unparsed_4 = self._io.read_bytes(40)
        self.pixels_data = self._io.read_bytes(self.pixel_size)
        self.unparsed_5 = self._io.read_bytes(96)
        self.palette_data = self._io.read_bytes(1024)


    def _fetch_instances(self):
        pass

    @property
    def pixel_size(self):
        if hasattr(self, '_m_pixel_size'):
            return self._m_pixel_size

        self._m_pixel_size = self.img_width * self.img_height
        return getattr(self, '_m_pixel_size', None)


