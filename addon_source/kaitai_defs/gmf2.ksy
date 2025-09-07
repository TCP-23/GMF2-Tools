meta:
  id: gmf2
  file-extension: GM2
  encoding: SHIFT-JIS
  endian: be
  imports: gct0

instances:
  game_identifier:
    pos: 0x70
    type: u4be
seq:
  - id: magic
    contents: "GMF2"
  - id: version
    type: u4le
    valid: 2
    
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  
  - id: num_objects
    type: u2le
  - id: num_textures
    type: u2le
  - contents: [0, 0]
  - id: num_materials
    type: u2le
    
  - id: off_objects
    type: u4le
  - id: off_textures
    type: u4le
  - contents: [0, 0, 0, 0]
  - id: off_materials
    type: u4le
    
  - id: unk_0x30
    type: u4le
  - id: unk_0x34
    type: u4le
  
  # 56B zeros
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  - contents: [0, 0, 0, 0, 0, 0, 0, 0]
  
  - contents: [255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if: game_identifier == 0xFFFFFFFF
    
  # --- Content Headers
    
  - id: textures
    type: texture
    repeat: expr
    repeat-expr: num_textures
    
  - id: materials
    type: material(_io.pos)
    repeat: expr
    repeat-expr: num_materials
    
  - id: world_objects
    type: world_object(_io.pos)
    repeat: expr
    repeat-expr: num_objects

types:
  # --- Common
  
  fl_vector_le:
    seq:
      - id: x
        type: f4le
      - id: y
        type: f4le
      - id: z
        type: f4le
        
  fl_vector_be:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
      - id: z
        type: f4
  
  fl_vector4_le:
    seq:
      - id: x
        type: f4le
      - id: y
        type: f4le
      - id: z
        type: f4le
      - id: w
        type: f4le
  
  u1_vector:
    seq:
      - id: x
        type: u1
      - id: y
        type: u1
      - id: z
        type: u1
  
  short_vector:
    seq:
      - id: x
        type: s2
      - id: y
        type: s2
      - id: z
        type: s2
  
  # --- Textures
  
  texture:
    seq:
      - id: name
        type: strz
        size: 8
      - id: off_prev
        type: u4le
      - id: off_next
        type: u4le
      - id: off_data
        type: u4le
      - id: unk_0x14
        type: u4le
      - id: len_data
        type: u4le
      - id: unk_string
        doc: "Seems to be the name of the model?"
        type: strz
        size: 4
    
    instances:
      gct0_texture:
        io: _root._io
        pos: off_data
        type: gct0
        size: len_data
  
  # --- Materials
  
  material:
    params:
      - id: offset
        type: u4
    seq:
      - id: name
        type: strz
        size: 8
      - id: off_prev
        type: u4le
      - id: off_next
        type: u4le
      - id: unk_3
        type: u4le
      - id: off_data
        type: u4le
      - contents: [0, 0, 0, 0, 0, 0, 0, 0]
    
    instances:
      data:
        io: _root._io
        pos: off_data
        type: material_data
    
    types:
      material_data:
        seq:
          - contents: [0, 0, 0, 0]
          - id: off_texture
            type: u4le
          - id: unk_3
            type: u4le
          - id: unk_4
            type: u4le
          - id: shaderparams_a
            type: fl_vector4_le
          - id: shaderparams_tint
            type: fl_vector4_le
  # --- Objects
  
  world_object:
    params:
      - id: offset
        type: u4
    seq:
      - id: name
        type: strz
        size: 8
      - id: flags
        type: u4le
      - id: off_v_buf
        type: u4le
      - id: off_parent
        type: u4le
      - id: off_first_child
        type: u4le
      - id: off_prev
        type: u4le
      - id: off_next
        type: u4le
      - id: off_surfaces
        type: u4le
      - id: unk_0x24
        type: f4le
      - id: off_first_bone
        type: u4le
      - id: v_divisor
        type: u4le
      - id: position
        type: fl_vector4_le
      - id: rotation
        type: fl_vector4_le
      - id: scale
        type: fl_vector_le
      - id: off_v_format
        type: u4le
      - id: cullbox_position
        type: fl_vector4_le
      - id: cullbox_size
        type: fl_vector4_le
      - id: unk_padding
        size: 64
        if: _root.game_identifier == 0xFFFFFFFF
    instances:
      v_format:
        io: _root._io
        pos: off_v_format
        size: 6
        if: off_v_format != 0x3f800000 and off_v_format != 0

      v_data:
        io: _root._io
        pos: off_v_buf
        type: vertex_data(off_surfaces + 18, v_divisor)
        if: off_surfaces != 0
      surfaces:
        io: _root._io
        pos: off_surfaces
        type: surface
        repeat: until
        repeat-until: _.off_next == 0
        if: off_surfaces != 0
        
    types:
      vertex_data:
        params:
          - id: off_v_count
            type: u4
          - id: v_divisor
            type: u4
        seq:
          - id: v_buffer
            type:
              switch-on: v_divisor
              cases:
                0xFFFFFFFF: fl_vector_be
                _: short_vector
            repeat: expr
            repeat-expr: num_verts
        instances:
          num_verts:
            io: _root._io
            pos: off_v_count
            type: u2le
      surface:
        seq:
          - id: off_prev
            type: u4le
          - id: off_next
            type: u4le
          - id: off_data
            type: u4le
          - id: off_material
            type: u4le
          - id: unk_0x10
            type: u2le
          - id: obj_vert_count
            type: u2le
          - id: off_skinning
            type: u4le
          - id: unk_0x18
            type: u2le
          - id: unk_0x1a
            type: u2le
          - id: unk_0x1c
            type: u2le
          - id: unk_0x1e
            type: u2le
        instances:
          surface_data:
            io: _root._io
            pos: off_data
            type: surfdata
          skinning_data:
            io: _root._io
            pos: off_skinning
            type: skindata
            if: off_skinning != 0
        types:
          surfdata:
            seq:
              - id: len_data
                type: u4be
              - id: num_vertices
                type: u2be
              - id: unknown
                type: u2be
              - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              
              - id: strip_data
                size: len_data
          skindata:
            seq:
              - id: off_prev
                type: u4le
              - id: off_next
                type: u4le
              - id: off_bone_connect
                type: u4le
              - contents: [0, 0, 0, 0]
            instances:
              bone_connect_data:
                io: _root._io
                pos: off_bone_connect
                type: boneconnectdata
                repeat: until
                repeat-until: _.off_next == 0
            types:
              boneconnectdata:
                seq:
                  - id: off_prev
                    type: u4le
                  - id: off_next
                    type: u4le
                  - id: off_bind
                    type: u4le
                  - contents: [0, 0, 0, 0]
                instances:
                  chain_bone_offsets:
                    io: _root._io
                    pos: off_bind
                    type: chainboneoffsets
                    repeat: until
                    repeat-until: _.off_next == 0
                types:
                  chainboneoffsets:
                    seq:
                      - id: off_prev
                        type: u4le
                      - id: off_next
                        type: u4le
                      - id: off_bone
                        type: u4le
                      - id: unk_float_35 # This value has to total 1 between all chain bones
                        type: f4le
                    instances:
                      bone_name:
                        io: _root._io
                        pos: off_bone
                        type: strz
                        size: 8