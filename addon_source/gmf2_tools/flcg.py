# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Flcg(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x46\x4C\x43\x47":
            raise kaitaistruct.ValidationNotEqualError(b"\x46\x4C\x43\x47", self.magic, self._io, u"/seq/0")
        self.version = self._io.read_u4le()
        if not self.version == 1:
            raise kaitaistruct.ValidationNotEqualError(1, self.version, self._io, u"/seq/1")
        self._unnamed2 = self._io.read_bytes(4)
        self.num_objects = self._io.read_u2be()
        self.num_materials = self._io.read_u2be()
        self.off_objects = self._io.read_u4be()
        self.off_materials = self._io.read_u4be()
        if not self.off_materials == 64:
            raise kaitaistruct.ValidationNotEqualError(64, self.off_materials, self._io, u"/seq/6")
        self.unk_0x1a = self._io.read_u4be()
        self._unnamed8 = self._io.read_bytes(36)
        self.materials = []
        for i in range(self.num_materials):
            self.materials.append(Flcg.Material(self._io.pos(), self._io, self, self._root))

        self.objects = []
        for i in range(self.num_objects):
            self.objects.append(Flcg.WObject(self._io.pos(), self._io, self, self._root))


    class FlVector4Be(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4be()
            self.y = self._io.read_f4be()
            self.z = self._io.read_f4be()
            self.w = self._io.read_f4be()


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


    class NormFlVectorBe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4be()
            if not self.x >= -1:
                raise kaitaistruct.ValidationLessThanError(-1, self.x, self._io, u"/types/norm_fl_vector_be/seq/0")
            if not self.x <= 1:
                raise kaitaistruct.ValidationGreaterThanError(1, self.x, self._io, u"/types/norm_fl_vector_be/seq/0")
            self.y = self._io.read_f4be()
            if not self.y >= -1:
                raise kaitaistruct.ValidationLessThanError(-1, self.y, self._io, u"/types/norm_fl_vector_be/seq/1")
            if not self.y <= 1:
                raise kaitaistruct.ValidationGreaterThanError(1, self.y, self._io, u"/types/norm_fl_vector_be/seq/1")
            self.z = self._io.read_f4be()
            if not self.z >= -1:
                raise kaitaistruct.ValidationLessThanError(-1, self.z, self._io, u"/types/norm_fl_vector_be/seq/2")
            if not self.z <= 1:
                raise kaitaistruct.ValidationGreaterThanError(1, self.z, self._io, u"/types/norm_fl_vector_be/seq/2")


    class Material(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self.off_first_object = self._io.read_u4le()
            self._unnamed2 = self._io.read_bytes(20)


    class WObject(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self.off_first_object = self._io.read_u4le()
            self.unk_0x0c = self._io.read_u4be()
            self._unnamed3 = self._io.read_bytes(8)
            self.off_prev = self._io.read_u4be()
            self.off_next = self._io.read_u4be()
            self.origin = Flcg.FlVectorBe(self._io, self, self._root)
            self.unk_0x2c = self._io.read_f4be()
            self.unk_0x30 = self._io.read_f4be()
            self.unk_0x34 = self._io.read_f4be()
            self.off_data = self._io.read_u4be()
            self._unnamed11 = self._io.read_bytes(20)

        class ColModelData(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.off_data_a = self._io.read_u4be()
                self.off_tris = self._io.read_u4be()
                self.num_data_a = self._io.read_u4be()
                self.num_tris = self._io.read_u4be()
                self.unk_0x10 = Flcg.FlVectorBe(self._io, self, self._root)
                self.unk_0x1c = Flcg.FlVectorBe(self._io, self, self._root)
                self.col_data_a = []
                for i in range(self.num_data_a):
                    self.col_data_a.append(Flcg.WObject.ColModelDataA(self._io, self, self._root))

                self.col_tris = []
                for i in range(self.num_tris):
                    self.col_tris.append(Flcg.WObject.ColTriangle(self._io, self, self._root))



        class ColModelDataA(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.off_hierarchy_1 = self._io.read_u4be()
                self.off_hierarchy_2 = self._io.read_u4be()
                self.off_tri = self._io.read_u4be()
                self.unk_0x0c = self._io.read_u4be()
                self.unk_0x10 = Flcg.NormFlVectorBe(self._io, self, self._root)
                self.unk_0x1c = self._io.read_f4be()


        class ColTriangle(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.off_next = self._io.read_u4be()
                self.unused_0x04 = self._io.read_u4be()
                if not self.unused_0x04 == 0:
                    raise kaitaistruct.ValidationNotEqualError(0, self.unused_0x04, self._io, u"/types/w_object/types/col_triangle/seq/1")
                self.off_material = self._io.read_u4be()
                self.vertex1 = Flcg.FlVectorBe(self._io, self, self._root)
                self.vertex2 = Flcg.FlVectorBe(self._io, self, self._root)
                self.vertex3 = Flcg.FlVectorBe(self._io, self, self._root)


        @property
        def model_data(self):
            if hasattr(self, '_m_model_data'):
                return self._m_model_data

            io = self._root._io
            _pos = io.pos()
            io.seek(self.off_data)
            self._m_model_data = Flcg.WObject.ColModelData(io, self, self._root)
            io.seek(_pos)
            return getattr(self, '_m_model_data', None)



