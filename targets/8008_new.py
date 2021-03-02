# 8008 with the new mnemonics
ISA_FEATURES = ('LITTLE','FORBID','REGS','JUMP_NPC')
INSTRUCTION_ALIGNMENT = 0
PAD_BYTE = 0x00 # Prefered Byte to pad with

FORBID = (
    'm',
    )

REGISTERS = {
    'a':    0,
    'b':    1,
    'c':    2,
    'd':    3,
    'e':    4,
    'h':    5,
    'l':    6,
    'm':    7,
    }

FORMATS = {
    '1b0':   (
        8,
        ('opcode',8)),
    '1b1':   (
        8,
        ('function',2),
        ('bank',2),
        ('port',3),
        ('opcode',1)),
    '1b2':   (
        8,
        ('function',2),
        ('port',5),
        ('opcode',1)),
    '1b3':   (
        8,
        ('function',2),
        ('imm',3),
        ('opcode',3)),
    '1b4':   (
        8,
        ('function',2),
        ('dest',3),
        ('source',3)),
    '2b0':   (
        16,
        ('imm',8),
        ('opcode',8)),
    '2b1':   (
        16,
        ('imm',8),
        ('function',2),
        ('dest',3),
        ('opcode',3)),
    '3b0':   (
        24,
        ('imm',16),
        ('opcode',8)),
    }

INSTRUCTIONS = {
    # CPU control
    ('hlt',):       ('1b0',('opcode',0b11111111)),
    # Input output
    ('in','NUM'):   ('1b1',('function',0b01),   ('bank',0b00),  ('opcode',0b1), ('port','NUM')),
    ('out','NUM'):  ('1b2',('function',0b01),   ('opcode',0b1), ('port','NUM')),
    # Jumps
    ('jmp','NUM'):  ('3b0',('opcode',0b01000100),('imm','NUM')),
    ('jnc','NUM'):  ('3b0',('opcode',0b01000000),('imm','NUM')),
    ('jnz','NUM'):  ('3b0',('opcode',0b01001000),('imm','NUM')),
    ('jp','NUM'):   ('3b0',('opcode',0b01010000),('imm','NUM')),
    ('jpo','NUM'):  ('3b0',('opcode',0b01011000),('imm','NUM')),
    ('jc','NUM'):   ('3b0',('opcode',0b01100000),('imm','NUM')),
    ('jz','NUM'):   ('3b0',('opcode',0b01101000),('imm','NUM')),
    ('jm','NUM'):   ('3b0',('opcode',0b01110000),('imm','NUM')),
    ('jpe','NUM'):  ('3b0',('opcode',0b01111000),('imm','NUM')),
    # Call
    ('call','NUM'): ('3b0',('opcode',0b01000110),('imm','NUM')),
    ('cnc','NUM'):  ('3b0',('opcode',0b01000010),('imm','NUM')),
    ('cnz','NUM'):  ('3b0',('opcode',0b01001010),('imm','NUM')),
    ('cp','NUM'):   ('3b0',('opcode',0b01010010),('imm','NUM')),
    ('cpo','NUM'):  ('3b0',('opcode',0b01011010),('imm','NUM')),
    ('cc','NUM'):   ('3b0',('opcode',0b01100010),('imm','NUM')),
    ('cz','NUM'):   ('3b0',('opcode',0b01101010),('imm','NUM')),
    ('cm','NUM'):   ('3b0',('opcode',0b01110010),('imm','NUM')),
    ('cpe','NUM'):  ('3b0',('opcode',0b01111010),('imm','NUM')),
    # Return
    ('ret',):       ('1b0',('opcode',0b00000111)),
    ('rnc',):       ('3b0',('opcode',0b00000011)),
    ('rnz',):       ('3b0',('opcode',0b00001011)),
    ('rp',):        ('3b0',('opcode',0b00010011)),
    ('rpo',):       ('3b0',('opcode',0b00011011)),
    ('rc',):        ('3b0',('opcode',0b00100011)),
    ('rz',):        ('3b0',('opcode',0b00101011)),
    ('rm',):        ('3b0',('opcode',0b00110011)),
    ('rpe',):       ('3b0',('opcode',0b00111011)),
    ('rst','NUM'):  ('1b3',('function',0b00),   ('opcode',0b101),   ('imm','NUM')),
    # Load
    ('mov','REG','REG'):    ('1b4',('function',0b11),('dest','REG'),        ('source','REG')),
    ('mvi','REG','NUM'):    ('2b1',('opcode',0b110),('function',0b00),  ('dest','REG'),     ('imm','NUM')),
    # arithmetic
    ('adi','NUM'):  ('2b0',('opcode',0b00000100),   ('imm','NUM')),
    ('aci','NUM'):  ('2b0',('opcode',0b00001100),   ('imm','NUM')),
    ('sui','NUM'):  ('2b0',('opcode',0b00010100),   ('imm','NUM')),
    ('sbi','NUM'):  ('2b0',('opcode',0b00011100),   ('imm','NUM')),
    ('ani','NUM'):  ('2b0',('opcode',0b00100100),   ('imm','NUM')),
    ('xri','NUM'):  ('2b0',('opcode',0b00101100),   ('imm','NUM')),
    ('ori','NUM'):  ('2b0',('opcode',0b00110100),   ('imm','NUM')),
    ('cpi','NUM'):  ('2b0',('opcode',0b00111100),   ('imm','NUM')),
    ('add','REG'):  ('1b4',('function',0b10),   ('dest',0b000), ('source','REG')),
    ('adc','REG'):  ('1b4',('function',0b10),   ('dest',0b001), ('source','REG')),
    ('sub','REG'):  ('1b4',('function',0b10),   ('dest',0b010), ('source','REG')),
    ('sbb','REG'):  ('1b4',('function',0b10),   ('dest',0b011), ('source','REG')),
    ('ana','REG'):  ('1b4',('function',0b10),   ('dest',0b100), ('source','REG')),
    ('xra','REG'):  ('1b4',('function',0b10),   ('dest',0b101), ('source','REG')),
    ('ora','REG'):  ('1b4',('function',0b10),   ('dest',0b110), ('source','REG')),
    ('cmp','REG'):  ('1b4',('function',0b10),   ('dest',0b111), ('source','REG')),
    ('inr','REG'):  ('1b4',('function',0b00),   ('source',0b000),   ('dest','REG')),
    ('dcr','REG'):  ('1b4',('function',0b00),   ('source',0b001),   ('dest','REG')),
    # Rotate
    ('rlc',): ('1b0',('opcode',0b00000010)),
    ('rrc',): ('1b0',('opcode',0b00001010)),
    ('ral',): ('1b0',('opcode',0b00010010)),
    ('rar',): ('1b0',('opcode',0b00011010)),
    }
