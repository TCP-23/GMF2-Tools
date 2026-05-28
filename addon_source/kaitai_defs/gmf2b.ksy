meta:
  id: gmf2b
  file-extension: GM2, gm2
  encoding: SHIFT-JIS
  endian: be
  imports:
    - tme

doc: |
  Planned to be merged into the main gmf2.ksy file soon.

seq:
  - id: magic
    type: str
    size: 4
    valid:
      any-of: ['"GMF2"', '"GM2F"', '"GMDF"']
  - id: version
    type: u4le
    valid: 2
    
  - size: 16
  
  - id: num_objects
    type: u2le
  - id: num_textures
    type: u2le
  - id: unused_0x1c
    type: u2le
    valid: 0
  - id: num_materials
    type: u2le
    
  - id: off_objects
    type: u4le
  - id: off_textures
    type: u4le
    valid: 0x70
  - id: unused_0x28
    type: u4le
    valid: 0
  - id: off_materials
    type: u4le
  
  - id: unk_0x30
    type: u4le
  - id: unk_0x34
    type: u4le
    
  - size: 56
  
  - id: textures
    type: texture(_io.pos)
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
      - id: off_data
        type: u4le
      - id: unk_0x14
        type: u4le
        doc: |
          Maybe a flag of some kind?
      - id: unused_0x18
        type: u4le
        valid: 0
        doc: |
          In later versions of the GMF2 format,
          this value is used to store the length
          of the texture data in bytes.
      - id: unk_string
        doc: |
          Seems to be the name of the model?
        type: strz
        size: 4
    
    instances:
      texture_data:
        io: _root._io
        pos: off_data
        type: tme
  
  # --- Materials
  
  material:
    doc: |
      A LOT of this material information is inaccurate,
      particularly involving the shadow ramps.
      Update this soon.
  
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
      
      - size: 8
    
    instances:
      data:
        io: _root._io
        pos: off_data
        type: material_data
    
    types:
      material_data:
        seq:
          - id: unused_0x00
            type: u4le
            valid: 0
          - id: off_ramp_data
            type: u4le
          - id: off_main_tex
            type: u4le
          - id: unk_0xc
            type: u4le
            doc: |
              Probably serves the same purpose that unk_0x3c does for the ramp part of the mat
          
          - id: shaderparams_main_a
            type: fl_vector4_le
          - id: shaderparams_main_tint
            type: fl_vector4_le
          
          - id: off_main_data
            type: u4le
          - id: unk_0x34
            type: u4le
          - id: off_ramp_tex
            type: u4le
          - id: unk_0x3c
            type: u4le
            doc: |
              Probably serves the same purpose that unk_0xc does for the main part of the mat
          
          - id: shaderparams_ramp_a
            type: fl_vector4_le
            doc: |
              Always zero?
          - id: shaderparams_ramp_tint
            type: fl_vector4_le
            
  # --- Objects
  
  world_object:
    doc: |
      Please remember to figure out how to actually grab the proper strips.
      Please.
      
      Most of the bone/skin weighting data is incorrect.
      Update soon.
  
    params:
      - id: offset
        type: u4
    seq:
      - id: name
        type: strz
        size: 8
      - id: flags
        type: u4le
        doc: |
          0x11 = bone
      - id: unused_0x0c
        type: u4le
        valid: 0
        
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
      - id: unused_0x2c
        type: u4le
        valid: 0
      
      - id: position
        type: fl_vector4_le
      - id: rotation
        type: fl_vector4_le
      - id: scale
        type: fl_vector4_le
        
      - id: cullbox_position
        type: fl_vector4_le
      - id: cullbox_size
        type: fl_vector4_le
    instances:
      surfaces:
        io: _root._io
        pos: off_surfaces
        type: surface(_io.pos, _index)
        repeat: until
        repeat-until: _.off_next == 0
        if: off_surfaces != 0
    types:
      surface:
        params:
          - id: offset
            type: u4
          - id: surf_idx
            type: u4
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
            type: u4le
          - id: off_skin_data
            type: u4le
          
          - id: unused_0x1c
            size: 8
        instances:
          skin_data:
            io: _root._io
            pos: off_skin_data
            type: skinning_data
            if: off_skin_data != 0
          data_strips:
            io: _root._io
            pos: off_data
            type: surface_data(_io.pos)
            repeat: until
            repeat-until: _.is_final_strip.is_final == true
        types:
          surface_data:
            params:
              - id: offset
                type: u4
            seq:
              - size: 8
              
              - id: off_prevstrip
                type: u4le
              
              - id: unk_0x0c
                type: u2le
                valid: 0x8000
              - id: unk_0x0e
                type: u2le
              
              - id: count
                type: u4le
              - id: dir_val
                type: u4le
              - id: unused_0x18
                type: u8
                valid: 0
            
              - id: vertices
                type: vertex
                repeat: expr
                repeat-expr: count
              
              - id: unk_1
                type: u4be
                valid: 17
              - id: unk_2
                type: u4be
                valid: 23
              
              - size: 8
            instances:
              is_final_strip:
                type: data_end_calc
            types:
              data_end_calc:
                instances:
                  sentinel_check:
                    io: _root._io
                    pos: ending_pos + 8
                    type: u4le
                    if: ending_pos != _io.size
                  is_final_surf_of_obj:
                    value: >-
                      _parent._parent._parent.surfaces.size ==
                      _parent._parent.surf_idx + 1
                  ending_pos:
                    value: >-
                      _parent.offset + 48 + (64 * _parent.count)
                  is_final:
                    value: >-
                      is_final_surf_of_obj == false
                      ? _parent._parent._parent.surfaces[_parent._parent.surf_idx + 1].off_data == ending_pos
                      : ending_pos == _io.size
                      ? true
                      : sentinel_check != 0x0
              vertex:
                seq:
                  - id: position
                    type: fl_vector_le
          
                  - id: unk_0x0c
                    type: f4le
          
                  - id: unk_0x10
                    type: fl_vector_le
                  - id: unused_0x1c
                    type: u4
                    valid: 0
          
                  - id: unk_0x20
                    type: f4le
                  - id: unk_0x24
                    type: f4le
                  - id: unk_0x28
                    type: f4le
                  - id: unk_0x2c
                    type: f4le
          
                  - id: u
                    type: f4le
                  - id: v_tex
                    type: f4le
          
                  - id: unk_0x38
                    type: f4le
                    valid: 1
                  - id: unused_0x3c
                    type: u4
                    valid: 0
                instances:
                  v:
                    value: 1 - v_tex
          skinning_data:
            seq:
              - id: off_prev
                type: u4le
              - id: off_next
                type: u4le
              - id: off_data
                type: u4le
              - id: unused_0x0c
                type: u4
                valid: 0
            instances:
              ub:
                io: _root._io
                pos: off_data
                type: unk_binding_02
                repeat: until
                repeat-until: _.off_next == 0
            types:
              unk_binding_02:
                seq:
                  - id: off_prev
                    type: u4le
                  - id: off_next
                    type: u4le
                  - id: off_data
                    type: u4le
                  - id: unused_0x0c
                    type: u4
                    valid: 0
                instances:
                  weight_binds:
                    io: _root._io
                    pos: off_data
                    type: bone_weight_binding
                    repeat: until
                    repeat-until: _.off_next == 0
                types:
                  bone_weight_binding:
                    seq:
                      - id: off_prev
                        type: u4le
                      - id: off_next
                        type: u4le
                      - id: off_bone
                        type: u4le
                      - id: weight_strength
                        type: f4le