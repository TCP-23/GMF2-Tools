# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Flcg(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Flcg, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
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



    def _fetch_instances(self):
        pass
        for i in range(len(self.materials)):
            pass
            self.materials[i]._fetch_instances()

        for i in range(len(self.objects)):
            pass
            self.objects[i]._fetch_instances()


    class FlVector4Be(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Flcg.FlVector4Be, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.x = self._io.read_f4be()
            self.y = self._io.read_f4be()
            self.z = self._io.read_f4be()
            self.w = self._io.read_f4be()


        def _fetch_instances(self):
            pass


    class FlVectorBe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Flcg.FlVectorBe, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.x = self._io.read_f4be()
            self.y = self._io.read_f4be()
            self.z = self._io.read_f4be()


        def _fetch_instances(self):
            pass


    class Material(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            super(Flcg.Material, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"Shift_JIS")
            self.unk_0x04 = self._io.read_u4le()
            if not self.unk_0x04 == 128:
                raise kaitaistruct.ValidationNotEqualError(128, self.unk_0x04, self._io, u"/types/material/seq/1")
            self._unnamed2 = self._io.read_bytes(20)


        def _fetch_instances(self):
            pass


    class WObject(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            super(Flcg.WObject, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"Shift_JIS")
            self.unk_0x04 = self._io.read_u4le()
            if not self.unk_0x04 == 128:
                raise kaitaistruct.ValidationNotEqualError(128, self.unk_0x04, self._io, u"/types/w_object/seq/1")
            self.unk_0x0c = self._io.read_u4be()
            self.off_parent = self._io.read_u4be()
            self.off_first_child = self._io.read_u4be()
            self.off_prev = self._io.read_u4be()
            self.off_next = self._io.read_u4be()
            self.origin = Flcg.FlVectorBe(self._io, self, self._root)
            self.unk_0x2c = self._io.read_f4be()
            self.unk_0x30 = self._io.read_f4be()
            self.unk_0x34 = self._io.read_f4be()
            self.off_data = self._io.read_u4be()
            self._unnamed12 = self._io.read_bytes(20)


        def _fetch_instances(self):
            pass
            self.origin._fetch_instances()
            _ = self.model_data
            if hasattr(self, '_m_model_data'):
                pass
                self._m_model_data._fetch_instances()


        class ColModelData(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                super(Flcg.WObject.ColModelData, self).__init__(_io)
                self._parent = _parent
                self._root = _root
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



            def _fetch_instances(self):
                pass
                self.unk_0x10._fetch_instances()
                self.unk_0x1c._fetch_instances()
                for i in range(len(self.col_data_a)):
                    pass
                    self.col_data_a[i]._fetch_instances()

                for i in range(len(self.col_tris)):
                    pass
                    self.col_tris[i]._fetch_instances()



        class ColModelDataA(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                super(Flcg.WObject.ColModelDataA, self).__init__(_io)
                self._parent = _parent
                self._root = _root
                self._read()

            def _read(self):
                self.off_hierarchy_1 = self._io.read_u4be()
                self.off_hierarchy_2 = self._io.read_u4be()
                self.off_tri = self._io.read_u4be()
                self.unk_0x0c = self._io.read_u4be()
                self.unk_0x10 = Flcg.FlVectorBe(self._io, self, self._root)
                self.unk_0x1c = self._io.read_f4be()


            def _fetch_instances(self):
                pass
                self.unk_0x10._fetch_instances()


        class ColTriangle(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                super(Flcg.WObject.ColTriangle, self).__init__(_io)
                self._parent = _parent
                self._root = _root
                self._read()

            def _read(self):
                self.off_next = self._io.read_u4be()
                self.unk_0x04 = self._io.read_u4be()
                if not self.unk_0x04 == 0:
                    raise kaitaistruct.ValidationNotEqualError(0, self.unk_0x04, self._io, u"/types/w_object/types/col_triangle/seq/1")
                self.off_material = self._io.read_u4be()
                self.vertex1 = Flcg.FlVectorBe(self._io, self, self._root)
                self.vertex2 = Flcg.FlVectorBe(self._io, self, self._root)
                self.vertex3 = Flcg.FlVectorBe(self._io, self, self._root)


            def _fetch_instances(self):
                pass
                self.vertex1._fetch_instances()
                self.vertex2._fetch_instances()
                self.vertex3._fetch_instances()


        @property
        def is_model_object(self):
            """Does the object have collision model data?
            """
            if hasattr(self, '_m_is_model_object'):
                return self._m_is_model_object

            self._m_is_model_object = self.off_data != 0
            return getattr(self, '_m_is_model_object', None)

        @property
        def model_data(self):
            if hasattr(self, '_m_model_data'):
                return self._m_model_data

            if self.is_model_object:
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_data)
                self._m_model_data = Flcg.WObject.ColModelData(io, self, self._root)
                io.seek(_pos)

            return getattr(self, '_m_model_data', None)



