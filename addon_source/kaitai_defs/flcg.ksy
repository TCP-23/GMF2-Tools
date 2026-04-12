meta:
  id: flcg
  file-extension: GCL, gcl
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
      Seems to always be around 1024, give or take one or two?
    
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
      - id: unk_0x04
        type: u4le
        valid: 128
        doc: |
          Always 128? Unknown what it is used for.
      
      - size: 20
  
  w_object:
    params:
      - id: offset
        type: u4
    seq:
      - id: name
        type: strz
        size: 8
      - id: unk_0x04
        type: u4le
        valid: 128
        doc: |
          Always 128? Unknown what it is used for.
      - id: unk_0x0c
        type: u4
        doc: |
          Potentially some sort of flag?
          Is always 3 on objects that have model data,
          and always 0xFFFFFFFF on objects that don't.
      
      - id: off_parent
        type: u4
      - id: off_first_child
        type: u4
      - id: off_prev
        type: u4
      - id: off_next
        type: u4
      
      - id: origin
        type: fl_vector_be
      - id: unk_0x2c
        type: f4
        doc: |
          Potentially a 4th component of the previous vector?
          Is only ever used if this object does not contain model data,
          but even then it can still be 0.
          This and the following two floats might be rotation data.
      - id: unk_0x30
        type: f4
      - id: unk_0x34
        type: f4
        doc: |
          Is only ever used if this object does not contain model data,
          but even then it can still be 0.
      
      - id: off_data
        type: u4
      
      - size: 20
    instances:
      is_model_object:
        #value: unk_0x0c != 0xFFFFFFFF
        value: off_data != 0
        doc: |
          Does the object have collision model data?
      model_data:
        io: _root._io
        pos: off_data
        type: col_model_data
        if: is_model_object
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
          - id: unk_0x0c
            type: u4
            doc: |
              Most likely flags.
          - id: unk_0x10
            type: fl_vector_be
            doc: |
              All values are always between -1 and 1. y is commonly either 0 or 1, but can be other values
          - id: unk_0x1c
            type: f4
      col_triangle:
        seq:
          - id: off_next
            type: u4
          - id: unk_0x04
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