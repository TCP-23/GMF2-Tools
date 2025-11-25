# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from .gct0 import Gct0
class Gmf2(KaitaiStruct):

    class GameName(Enum):
        unk = 0
        blood = 1
        nmh1 = 112
        nmh2 = 128
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
        self.unk_0x30 = self._io.read_u4le()
        self.unk_0x34 = self._io.read_u4le()
        self._unnamed13 = self._io.read_bytes(56)
        if self.game_id == Gmf2.GameName.nmh2:
            self.unk_0x70 = self._io.read_u4le()

        if self.game_id == Gmf2.GameName.nmh2:
            self._unnamed15 = self._io.read_bytes(12)

        self.textures = []
        for i in range(self.num_textures):
            self.textures.append(Gmf2.Texture(self._io.pos(), self._io, self, self._root))

        self.materials = []
        for i in range(self.num_materials):
            self.materials.append(Gmf2.Material(self._io.pos(), self._io, self, self._root))

        self.world_objects = []
        for i in range(self.num_objects):
            self.world_objects.append(Gmf2.WorldObject(self._io.pos(), self._io, self, self._root))


    class WorldObject(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
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
            self.position = Gmf2.FlVector4Le(self._io, self, self._root)
            self.rotation = Gmf2.FlVector4Le(self._io, self, self._root)
            self.scale = Gmf2.FlVectorLe(self._io, self, self._root)
            self.off_v_format = self._io.read_u4le()
            self.cullbox_position = Gmf2.FlVector4Le(self._io, self, self._root)
            self.cullbox_size = Gmf2.FlVector4Le(self._io, self, self._root)
            if self._root.game_id == Gmf2.GameName.nmh2:
                self._unnamed17 = self._io.read_bytes(64)


        class VertexData(KaitaiStruct):
            def __init__(self, off_v_count, v_divisor, off_v_format, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.off_v_count = off_v_count
                self.v_divisor = v_divisor
                self.off_v_format = off_v_format
                self._read()

            def _read(self):
                self.v_buffer = []
                for i in range(self.num_verts):
                    _on = self.v_divisor
                    if _on == 4294967295:
                        self.v_buffer.append(Gmf2.FlVectorBe(self._io, self, self._root))
                    else:
                        self.v_buffer.append(Gmf2.ShortVector(self._io, self, self._root))


            @property
            def v_format(self):
                if hasattr(self, '_m_v_format'):
                    return self._m_v_format

                if  ((self.off_v_format != 1065353216) and (self.off_v_format != 0)) :
                    io = self._root._io
                    _pos = io.pos()
                    io.seek(self.off_v_format)
                    self._m_v_format = io.read_bytes(6)
                    io.seek(_pos)

                return getattr(self, '_m_v_format', None)

            @property
            def num_verts(self):
                if hasattr(self, '_m_num_verts'):
                    return self._m_num_verts

                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_v_count)
                self._m_num_verts = io.read_u2le()
                io.seek(_pos)
                return getattr(self, '_m_num_verts', None)


        class Surface(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.off_prev = self._io.read_u4le()
                self.off_next = self._io.read_u4le()
                self.off_data = self._io.read_u4le()
                self.off_material = self._io.read_u4le()
                self.unk_0x10 = self._io.read_u2le()
                self.obj_vert_count = self._io.read_u2le()
                self.off_skinning = self._io.read_u4le()
                self.unk_0x18 = self._io.read_u2le()
                self.unk_0x1a = self._io.read_u2le()
                self.unk_0x1c = self._io.read_u2le()
                self.unk_0x1e = self._io.read_u2le()

            class Surfdata(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.len_data = self._io.read_u4be()
                    self.num_vertices = self._io.read_u2be()
                    self.unknown = self._io.read_u2be()
                    self._unnamed3 = self._io.read_bytes(24)
                    if not self._unnamed3 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
                        raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed3, self._io, u"/types/world_object/types/surface/types/surfdata/seq/3")
                    self.strip_data = self._io.read_bytes(self.len_data)


            class Skindata(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.off_prev = self._io.read_u4le()
                    self.off_next = self._io.read_u4le()
                    self.off_bone_connect = self._io.read_u4le()
                    self._unnamed3 = self._io.read_bytes(4)
                    if not self._unnamed3 == b"\x00\x00\x00\x00":
                        raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed3, self._io, u"/types/world_object/types/surface/types/skindata/seq/3")

                class Boneconnectdata(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.off_prev = self._io.read_u4le()
                        self.off_next = self._io.read_u4le()
                        self.off_bind = self._io.read_u4le()
                        self._unnamed3 = self._io.read_bytes(4)
                        if not self._unnamed3 == b"\x00\x00\x00\x00":
                            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self._unnamed3, self._io, u"/types/world_object/types/surface/types/skindata/types/boneconnectdata/seq/3")

                    class Chainboneoffsets(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            self._io = _io
                            self._parent = _parent
                            self._root = _root if _root else self
                            self._read()

                        def _read(self):
                            self.off_prev = self._io.read_u4le()
                            self.off_next = self._io.read_u4le()
                            self.off_bone = self._io.read_u4le()
                            self.unk_float_35 = self._io.read_f4le()

                        @property
                        def bone_name(self):
                            if hasattr(self, '_m_bone_name'):
                                return self._m_bone_name

                            io = self._root._io
                            _pos = io.pos()
                            io.seek(self.off_bone)
                            self._m_bone_name = (KaitaiStream.bytes_terminate(io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
                            io.seek(_pos)
                            return getattr(self, '_m_bone_name', None)


                    @property
                    def chain_bone_offsets(self):
                        if hasattr(self, '_m_chain_bone_offsets'):
                            return self._m_chain_bone_offsets

                        io = self._root._io
                        _pos = io.pos()
                        io.seek(self.off_bind)
                        self._m_chain_bone_offsets = []
                        i = 0
                        while True:
                            _ = Gmf2.WorldObject.Surface.Skindata.Boneconnectdata.Chainboneoffsets(io, self, self._root)
                            self._m_chain_bone_offsets.append(_)
                            if _.off_next == 0:
                                break
                            i += 1
                        io.seek(_pos)
                        return getattr(self, '_m_chain_bone_offsets', None)


                @property
                def bone_connect_data(self):
                    if hasattr(self, '_m_bone_connect_data'):
                        return self._m_bone_connect_data

                    io = self._root._io
                    _pos = io.pos()
                    io.seek(self.off_bone_connect)
                    self._m_bone_connect_data = []
                    i = 0
                    while True:
                        _ = Gmf2.WorldObject.Surface.Skindata.Boneconnectdata(io, self, self._root)
                        self._m_bone_connect_data.append(_)
                        if _.off_next == 0:
                            break
                        i += 1
                    io.seek(_pos)
                    return getattr(self, '_m_bone_connect_data', None)


            @property
            def surface_data(self):
                if hasattr(self, '_m_surface_data'):
                    return self._m_surface_data

                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_data)
                self._m_surface_data = Gmf2.WorldObject.Surface.Surfdata(io, self, self._root)
                io.seek(_pos)
                return getattr(self, '_m_surface_data', None)

            @property
            def skinning_data(self):
                if hasattr(self, '_m_skinning_data'):
                    return self._m_skinning_data

                if self.off_skinning != 0:
                    io = self._root._io
                    _pos = io.pos()
                    io.seek(self.off_skinning)
                    self._m_skinning_data = Gmf2.WorldObject.Surface.Skindata(io, self, self._root)
                    io.seek(_pos)

                return getattr(self, '_m_skinning_data', None)


        @property
        def v_data(self):
            if hasattr(self, '_m_v_data'):
                return self._m_v_data

            if self.off_surfaces != 0:
                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_v_buf)
                self._m_v_data = Gmf2.WorldObject.VertexData((self.off_surfaces + 18), self.v_divisor, self.off_v_format, io, self, self._root)
                io.seek(_pos)

            return getattr(self, '_m_v_data', None)

        @property
        def surfaces(self):
            if hasattr(self, '_m_surfaces'):
                return self._m_surfaces

            if self.off_surfaces != 0:
                io = self._root._io
                _pos = io.pos()
                io.seek(self.off_surfaces)
                self._m_surfaces = []
                i = 0
                while True:
                    _ = Gmf2.WorldObject.Surface(io, self, self._root)
                    self._m_surfaces.append(_)
                    if _.off_next == 0:
                        break
                    i += 1
                io.seek(_pos)

            return getattr(self, '_m_surfaces', None)


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


    class Material(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.unk_3 = self._io.read_u4le()
            self.off_data = self._io.read_u4le()
            self._unnamed5 = self._io.read_bytes(8)
            if not self._unnamed5 == b"\x00\x00\x00\x00\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00\x00\x00\x00\x00", self._unnamed5, self._io, u"/types/material/seq/5")

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
                self.off_ramp_data = self._io.read_u4le()
                self.off_main_tex = self._io.read_u4le()
                self.unk_0xc = self._io.read_u4le()
                self.shaderparams_main_a = Gmf2.FlVector4Le(self._io, self, self._root)
                self.shaderparams_main_tint = Gmf2.FlVector4Le(self._io, self, self._root)
                self.off_main_data = self._io.read_u4le()
                self._unnamed7 = self._io.read_bytes(4)
                self.off_ramp_tex = self._io.read_u4le()
                self.unk_0x3c = self._io.read_u4le()
                self.shaderparams_ramp_a = Gmf2.FlVector4Le(self._io, self, self._root)
                self.shaderparams_ramp_tint = Gmf2.FlVector4Le(self._io, self, self._root)


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


    class Texture(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.offset = offset
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"SHIFT-JIS")
            self.off_prev = self._io.read_u4le()
            self.off_next = self._io.read_u4le()
            self.off_data = self._io.read_u4le()
            self.unk_0x14 = self._io.read_u4le()
            self.len_data = self._io.read_u4le()
            self.unk_string = (KaitaiStream.bytes_terminate(self._io.read_bytes(4), 0, False)).decode(u"SHIFT-JIS")

        @property
        def gct0_texture(self):
            if hasattr(self, '_m_gct0_texture'):
                return self._m_gct0_texture

            io = self._root._io
            _pos = io.pos()
            io.seek(self.off_data)
            self._raw__m_gct0_texture = io.read_bytes(self.len_data)
            _io__raw__m_gct0_texture = KaitaiStream(BytesIO(self._raw__m_gct0_texture))
            self._m_gct0_texture = Gct0(_io__raw__m_gct0_texture)
            io.seek(_pos)
            return getattr(self, '_m_gct0_texture', None)


    @property
    def game_id(self):
        if hasattr(self, '_m_game_id'):
            return self._m_game_id

        self._m_game_id = KaitaiStream.resolve_enum(Gmf2.GameName, self.off_textures)
        return getattr(self, '_m_game_id', None)


