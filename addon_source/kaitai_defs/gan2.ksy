meta:
  id: gan2
  file-extension: ga2
  encoding: SHIFT-JIS
  endian: be

seq:
  - id: magic
    contents: "GAN2"
  - id: version
    type: u4be
  
  - contents: [0, 0, 0, 0]
  
  - id: anim_time # Always divisible by 3000? Maybe animation time in milliseconds?
    type: u4le
    
  - contents: [0, 0, 0, 0]
  
  - id: num_obj
    type: u4le
  
  - contents: [0, 0, 0, 0, 0, 0, 0, 0]
  
  - id: off_obj
    type: u4le
  
  - id: unk_4
    type: u4le
    
  - id: unk_5
    type: u4le
  
  - id: unk_6 # Potentially always zero?
    type: u4le
  
  - id: anim_objects
    type: anim_object(_io.pos)
    repeat: expr
    repeat-expr: num_obj
    
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

  # --- other
  anim_object:
    params:
      - id: offset
        type: u4
    seq:
      - id: name
        type: strz
        size: 8
      
      - contents: [0, 0, 0, 0, 0, 0, 0, 0]
      
      - id: off_parent
        type: u4le
      - id: off_first_child
        type: u4le
      - id: off_prev
        type: u4le
      - id: off_next
        type: u4le
      
      - id: data_offset
        type: u4le
      
      - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    instances:
      obj_anim_data:
        io: _root._io
        pos: data_offset
        type: anim_data
        if: data_offset != 0
  
  anim_data:
    seq:
      - id: unk_1
        type: u4be
        
      - contents: [0, 0, 0, 0]
      
      - id: unk_3 # Always the same as anim_time
        type: u4le
      - id: block_count
        type: u4le
        
      - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      
      - id: block_offset_offset
        type: u4le
        
      - id: pos_x_off # Block 0 offset
        type: u4le
      - id: pos_y_off # Block 1 offset
        type: u4le
      - id: pos_z_off # Block 2 ofset
        type: u4le
      - id: rot_x_off # Block 3 offset
        type: u4le
        if: block_count == 6
      - id: rot_y_off # Block 4 offset
        type: u4le
        if: block_count == 6
      - id: rot_z_off # Block 5 offset
        type: u4le
        if: block_count == 6
      
      - contents: [0, 0, 0, 0]
        if: block_count == 6
      - contents: [0, 0, 0, 0]
        
    instances:
      pos_x_block:
        io: _root._io
        pos: pos_x_off
        type: anim_data_block(pos_x_off)
      pos_y_block:
        io: _root._io
        pos: pos_y_off
        type: anim_data_block(pos_y_off)
      pos_z_block:
        io: _root._io
        pos: pos_z_off
        type: anim_data_block(pos_z_off)
      rot_x_block:
        io: _root._io
        pos: rot_x_off
        type: anim_data_block(rot_x_off)
        if: block_count == 6
      rot_y_block:
        io: _root._io
        pos: rot_y_off
        type: anim_data_block(rot_y_off)
        if: block_count == 6
      rot_z_block:
        io: _root._io
        pos: rot_z_off
        type: anim_data_block(rot_z_off)
        if: block_count == 6
        
  anim_data_block:
    params:
      - id: data_off
        type: u4
    seq:
      - id: unk_1 # Always 1?
        type: u2le
      - id: block_id
        type: u2le
      
      - contents: [0, 0, 0, 0]
      
      - id: block_data_off
        type: u4le
        
      - contents: [0, 0, 0, 0]
      
      - id: v_divisor
        type: u1
        
      - id: unk_4
        type: u1
        
      - id: data_pair_count # The number of data pairs?
        type: u2le
        
      - id: data_pairs
        type:
          switch-on: block_id
          cases:
            0: s2le
            1: s2le
            2: s2le
            3: u2le
            4: u2le
            5: u2le
        repeat: expr
        repeat-expr: data_pair_count
        
      - id: unk_line_ending
        type: u2le
        if: v_divisor == 5