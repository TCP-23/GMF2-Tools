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
    
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  
  - id: anim_objects
    type: anim_object
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
    instances:
      obj_anim_data:
        io: _root._io
        pos: data_offset
        type: anim_data
        if: data_offset != 0
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
        
      - id: unk_off_1
        type: u4le
      - id: unk_off_2
        type: u4le
      - id: unk_off_3
        type: u4le
      - id: unk_off_4
        type: u4le
        if: block_count == 6
      - id: unk_off_5
        type: u4le
        if: block_count == 6
      - id: unk_off_6
        type: u4le
        if: block_count == 6
      
      - contents: [0, 0, 0, 0]
        if: block_count == 6
      - contents: [0, 0, 0, 0]
        
      - id: anim_block_1
        type: anim_block(unk_off_2)
  
  anim_block:
    params:
      - id: data_off
        type: u4
    seq:
      - id: unk_1 # Always 1?
        type: u2le
      - id: block_id
        type: u2le
      
      - contents: [0, 0, 0, 0]
      
      - id: unk_2
        type: u4le
        
      - contents: [0, 0, 0, 0]
      
      - id: unk_3
        type: u2le
        
      - id: unk_count
        type: u2le
      
      - id: unk_4 # Always 0, 6433, or -6433
        type: u2le 