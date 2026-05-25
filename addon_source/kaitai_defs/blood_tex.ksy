meta:
  id: blood_tex
  file-extension: blood_tex
  encoding: SHIFT_JIS
  endian: le

seq:
  - id: unparsed_1
    size: 4
  
  - size: 4
  
  - id: unparsed_2
    size: 2
  
  - id: csm_flags
    type: u1
  
  - id: unparsed_3
    size: 53
  
  - id: img_width
    type: u4
  - id: img_height
    type: u4
  
  - id: unparsed_4
    size: 40
  
  - id: pixels_data
    size: pixel_size
    
  - id: unparsed_5
    size: 96
  
  - id: palette_data
    size: 1024
instances:
  pixel_size:
    value: img_width * img_height