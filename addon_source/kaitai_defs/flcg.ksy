meta:
  id: flcg
  file-extension: GCL
  encoding: SHIFT-JIS
  endian: be
  
seq:
  - id: magic
    contents: "FLCG"
  - id: version
    type: u4le
    valid: 1
    
  - size: 4
  
  - id: num_objects
    type: u2
  - id: num_materials
    type: u2
  - id: off_objects
    type: u4
  - id: off_materials
    type: u4
    valid: 0x40
  - id: unk_0x1a
    type: u4
    doc: |
      Always a power of two?
    
  - size: 36
  
  - id: materials
    type: material(_io.pos)
    repeat: expr
    repeat-expr: num_materials
    
  - id: objects
    type: w_object(_io.pos)
    repeat: expr
    repeat-expr: num_objects
  
types:
  fl_vector_be:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
      - id: z
        type: f4
        
  norm_fl_vector_be:
    seq:
      - id: x
        type: f4
        valid:
          min: -1
          max: 1
      - id: y
        type: f4
        valid:
          min: -1
          max: 1
      - id: z
        type: f4
        valid:
          min: -1
          max: 1

  fl_vector4_be:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
      - id: z
        type: f4
      - id: w
        type: f4

  material:
    params:
      - id: offset
        type: u4
    seq:
      - id: name
        type: strz
        size: 8
      - id: off_first_object
        type: u4le
        doc: |
          Always the offset of the first object header present in the file. Unknown what it is used for.
      
      - size: 20
  
  w_object:
    params:
      - id: offset
        type: u4
    seq:
      - id: name
        type: strz
        size: 8
      - id: off_first_object
        type: u4le
        doc: |
          Always the offset of the first object header present in the file. Unknown what it is used for.
      - id: unk_0x0c
        type: u4
        
      - size: 8
      
      - id: off_prev
        type: u4
      - id: off_next
        type: u4
      - id: origin
        type: fl_vector_be
      - id: unk_0x2c
        type: f4
        doc: |
          Almost always 0. Potentially a 4th component of the previous vector?
      - id: unk_0x30
        type: f4
      - id: unk_0x34
        type: f4
        doc: |
          Almost always 0.
      - id: off_data
        type: u4
      
      - size: 20
    instances:
      model_data:
        io: _root._io
        pos: off_data
        type: col_model_data
    types:
      col_model_data:
        seq:
          - id: off_data_a
            type: u4
          - id: off_tris
            type: u4
          - id: num_data_a
            type: u4
          - id: num_tris
            type: u4
          - id: unk_0x10
            type: fl_vector_be
            doc: |
              Bounding box origin?
          - id: unk_0x1c
            type: fl_vector_be
          
          - id: col_data_a
            type: col_model_data_a
            repeat: expr
            repeat-expr: num_data_a
          
          - id: col_tris
            type: col_triangle
            repeat: expr
            repeat-expr: num_tris
      col_model_data_a:
        seq:
          - id: off_hierarchy_1
            type: u4
            doc: |
              An unknown relation of some kind.
          - id: off_hierarchy_2
            type: u4
            doc: |
              An unknown relation of some kind.
          - id: off_tri
            type: u4
          - id: unk_0x0c  # flags?
            type: u4
          - id: unk_0x10
            type: norm_fl_vector_be
            doc: |
              All values are always between -1 and 1. y is commonly either 0 or 1, but can be other values
          - id: unk_0x1c
            type: f4
      col_triangle:
        seq:
          - id: off_next
            type: u4
          - id: unused_0x04
            type: u4
            valid: 0
          - id: off_material
            type: u4
          - id: vertex1
            type: fl_vector_be
          - id: vertex2
            type: fl_vector_be
          - id: vertex3
            type: fl_vector_be