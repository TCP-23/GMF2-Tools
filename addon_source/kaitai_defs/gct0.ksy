meta:
  id: gct0
  file-extension: GCT, BIN
  endian: be

seq:
  - id: magic
    contents: "GCT0"
    
  - contents: [0, 0]
  
  - id: encoding
    enum: texture_encoding
    type: u2be
  - id: width
    type: u2be
  - id: height
    type: u2be
  
  - contents: [0, 0, 0, 0]
  
  - id: unk_1
    type: u4be
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  - id: unk_2
    type: u4be
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  - contents: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  
  - id: texture_data
    size-eos: true
    

enums:
  texture_encoding:
    0x00: "i4"
    0x01: "i8"
    0x02: "ia4"
    0x03: "ia8"
    0x04: "rgb565"
    0x05: "rgb5a3" # used
    0x06: "rgba32" # used
    0x08: "c4"
    0x09: "c8"
    0x0A: "c14x2"
    0x0E: "cmpr" # used