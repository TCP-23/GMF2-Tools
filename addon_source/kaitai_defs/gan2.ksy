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
  
  - id: unk_1 # Always divisible by 3000? Maybe animation time in milliseconds?
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
      
      - id: unk_3 # Always the same as unk_1
        type: u4le
      - id: unk_4
        type: u4le
        
      - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      
      - id: unk_5
        type: u4le
        
      - id: unk_off_1
        type: u4le
      - id: unk_off_2
        type: u4le
      - id: unk_off_3
        type: u4le
      - id: unk_off_4
        type: u4le
      - id: unk_off_5
        type: u4le
      - id: unk_off_6
        type: u4le
        
      - id: unk_6
        type: u4le
      
      - contents: [0, 0, 0, 0]
        
      #- id: anim_block_1
        #type: anim_block(unk_off_2)
  
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
      
      - id: temp_data
        size: (data_off - unk_2)
        if: block_id != 5
      
      - id: temp_data_2
        size-eos: true
        if: block_id == 5