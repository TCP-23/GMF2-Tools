meta:
  id: gmf2
  file-extension: GM2
  encoding: SHIFT-JIS
  endian: be

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
    type: material
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
      data:
        io: _root._io
        pos: off_data
        size: len_data
  
  # --- Materials
  
  material:
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
      - id: off
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
      - id: unk_0x28
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
      surfaces:
        io: _root._io
        pos: off_surfaces
        type: surface(off_v_buf, v_divisor)
        repeat: until
        repeat-until: _.off_next == 0
        if: off_surfaces != 0
        
    types:
      surface:
        params:
          - id: off_v_buf
            type: u4
          - id: v_divisor
            type: s4
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
          - id: num_v
            type: u2le
          - id: unk_0x14
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
          v_buf:
            io: _root._io
            pos: off_v_buf
            type:
              switch-on: v_divisor
              cases:
                -1: fl_vector_be
                _: short_vector
            repeat: expr
            repeat-expr: num_v
          tristrip_type_data:
            io: _root._io
            type: tristrip_type_info
          strips:
            io: _root._io
            pos: off_data + 32
            type: tristrip
            repeat: until
            repeat-until: _.command != 0x99
            
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
          
          tristrip:
            seq:
              - id: command
                type: u2be
              - id: num_v
                type: u2be
              - id: idx_data
                type:
                  switch-on: _parent.tristrip_type_data.tristrip_type
                  cases:
                    0x474D: index_11b_b
                    0x474D4632: index_9b
                    _: index_11b_a
                repeat: expr
                repeat-expr: num_v
            types:
              index_11b_a:
                seq:
                  - id: idx
                    type: u2be
                  - id: normal
                    type: u1_vector
                  - id: color
                    type: u2be
                  - id: u
                    type: u2be
                  - id: v
                    type: u2be
              index_11b_b:
                seq:
                  - id: unk_6
                    type: u2be
                  - id: idx
                    type: u2be
                  - id: normal
                    type: u1_vector
                  - id: u
                    type: u2be
                  - id: v
                    type: u2be
              index_9b:
                seq:
                  - id: idx
                    type: u2be
                  - id: normal
                    type: u1_vector
                  - id: u
                    type: u2be
                  - id: v
                    type: u2be
          tristrip_type_info:
            instances:
              tr_len_8:
                io: _root._io
                pos: _parent.off_data + 34
                type: u2be
              second_strip_command:
                io: _root._io
                pos: _parent.off_data + 32 + (tr_len_8 * 11 + 4)
                type: u2be
              tristrip_length:
                value: 11
                if: (second_strip_command == 153) or ((second_strip_command == 0) and (tr_len_8 == _parent.surface_data.num_vertices))
              tristrip_type:
                pos: 0
                type:
                  switch-on: tristrip_length
                  cases:
                    11: u2
                    9: u4
                if: _parent._parent.off_v_format == 0x3f800000 or _parent._parent.off_v_format == 0
                