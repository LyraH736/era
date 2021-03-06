# a simple unnamed architecture, mainly for testing the assembler
ISA_FEATURES = ('LITTLE','REGS','COND','JUMP_REL','JUMP_NPC')
INSTRUCTION_ALIGNMENT = 0
PAD_BYTE = 0x00 # Prefered Byte to pad with

REGISTERS = {
    'ar':   0,
    'sp':   1,
    't0':   2,
    't1':   3,
    't2':   4,
    's0':   5,
    's1':   6,
    's2':   7,
    'fp':   7,
    'x0':   0,
    'x1':   1,
    'x2':   2,
    'x3':   3,
    'x4':   4,
    'x5':   5,
    'x6':   6,
    'x7':   7
    }

FORMATS = {
    '1b':   (
        8,
        ('function',3),
        ('opcode',4),
        ('size',1)),
    '2b_reg':   (
        16,
        ('dst',3),
        ('src',3),
        ('func',5),
        ('mjropc',3),
        ('size',2)),
    '2b_imm5':   (
        16,
        ('dst',3),
        ('imm',5),
        ('func',3),
        ('mjropc',3),
        ('size',2)),
    '2b_imm8':   (
        16,
        ('dst',3),
        ('imm',8),
        ('mjropc',3),
        ('size',2)),
    '2b_off8':   (
        16,
        ('imm',8),
        ('func',3),
        ('mjropc',3),
        ('size',2)),
    '2b_off9':   (
        16,
        ('imm',9),
        ('func',2),
        ('mjropc',3),
        ('size',2)),
    }

CONDITIONS = {
    'zs':   0,
    'zc':   1,
    'cs':   2,
    'cc':   3,
    'ns':   4,
    'nc':   5,
    'al':   7,
    'eq':   0,
    'ne':   1,
    'hs':   2,
    'lo':   3,
    'mi':   4,
    'pl':   5
    }

INSTRUCTIONS = {
    # 1 Byte instructions
    ('nop',):  ('1b',('size',0),('opcode',0b0000),('function',0b000)),
    ('ret',):  ('1b',('size',0),('opcode',0b0000),('function',0b100)),
    ('lpc',):  ('1b',('size',0),('opcode',0b0000),('function',0b010)),
    ('lnpc',): ('1b',('size',0),('opcode',0b0000),('function',0b010)),
    ('ecal',): ('1b',('size',0),('opcode',0b0000),('function',0b001)),
    ('eret',): ('1b',('size',0),('opcode',0b0000),('function',0b011)),
    ('halt',): ('1b',('size',0),('opcode',0b0000),('function',0b111)),
    # 1 Byte register based instructions
    ('clr','REG'): ('1b',('size',0),('opcode',0b1000),('function','REG')),
    ('set','REG'): ('1b',('size',0),('opcode',0b0100),('function','REG')),
    ('sll','REG'): ('1b',('size',0),('opcode',0b1100),('function','REG')),
    ('srl','REG'): ('1b',('size',0),('opcode',0b0010),('function','REG')),
    ('sra','REG'): ('1b',('size',0),('opcode',0b1010),('function','REG')),
    ('adc','REG'): ('1b',('size',0),('opcode',0b0110),('function','REG')),
    ('sbb','REG'): ('1b',('size',0),('opcode',0b1110),('function','REG')),
    ('jr','REG'):  ('1b',('size',0),('opcode',0b0001),('function','REG')),
    ('jrl','REG'): ('1b',('size',0),('opcode',0b1001),('function','REG')),
    ('not','REG'): ('1b',('size',0),('opcode',0b0101),('function','REG')),
    ('neg','REG'): ('1b',('size',0),('opcode',0b1101),('function','REG')),
    ('inc','REG'): ('1b',('size',0),('opcode',0b0011),('function','REG')),
    ('dec','REG'): ('1b',('size',0),('opcode',0b1011),('function','REG')),
    # 2 Byte instructions
    # Register based ones first
    ('and','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b00000),('dst','REG'),('src','REG')),
    ('or','REG','REG'):   ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b10000),('dst','REG'),('src','REG')),
    ('xor','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b01000),('dst','REG'),('src','REG')),
    ('not','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b11000),('dst','REG'),('src','REG')),
    ('sll','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b00100),('dst','REG'),('src','REG')),
    ('srl','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b10100),('dst','REG'),('src','REG')),
    ('sra','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b01100),('dst','REG'),('src','REG')),
    ('add','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b11100),('dst','REG'),('src','REG')),
    ('sub','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b00010),('dst','REG'),('src','REG')),
    ('inc','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b10010),('dst','REG'),('src','REG')),
    ('dec','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b01010),('dst','REG'),('src','REG')),
    ('adc','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b11010),('dst','REG'),('src','REG')),
    ('sbb','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b00110),('dst','REG'),('src','REG')),
    ('neg','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b10110),('dst','REG'),('src','REG')),
    ('mov','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b01110),('dst','REG'),('src','REG')),
    ('lb','REG','REG'):   ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b00001),('dst','REG'),('src','REG')),
    ('sb','REG','REG'):   ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b10001),('dst','REG'),('src','REG')),
    ('cmp','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b01001),('src','REG'),('dst','REG')),
    ('cmn','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b11001),('src','REG'),('dst','REG')),
    ('cma','REG','REG'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b00101),('src','REG'),('dst','REG')),
    # 3bit immediates     
    ('sll','REG','NUM'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b10101),('dst','REG'),('src','NUM')),
    ('srl','REG','NUM'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b01101),('dst','REG'),('src','NUM')),
    ('sra','REG','NUM'):  ('2b_reg',('size',0b01),('mjropc',0b000),('func',0b11101),('dst','REG'),('src','NUM')),
    # 5bit immediates     
    ('and','REG','NUM'):  ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b000),('dst','REG'),('imm','NUM')),
    ('xor','REG','NUM'):  ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b100),('dst','REG'),('imm','NUM')),
    ('or','REG','NUM'):   ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b010),('dst','REG'),('imm','NUM')),
    ('add','REG','NUM'):  ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b110),('dst','REG'),('imm','NUM')),
    ('cmp','REG','NUM'):  ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b001),('dst','REG'),('imm','NUM')),
    ('cma','REG','NUM'):  ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b101),('dst','REG'),('imm','NUM')),
    ('lcsr','REG','REG'): ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b011),('dst','REG'),('imm','REG')),
    ('scsr','REG','REG'): ('2b_imm5',('size',0b01),('mjropc',0b100),('func',0b111),('dst','REG'),('imm','REG')),
    # 8bit immediate
    ('mov','REG','NUM'):  ('2b_imm8',('size',0b01),('mjropc',0b101),('dst','REG'),('imm','NUM')),
    # 8bit offsets
    ('b.zs','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b000),('imm','NUM')),
    ('b.eq','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b000),('imm','NUM')),
    ('b.zc','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b100),('imm','NUM')),
    ('b.ne','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b100),('imm','NUM')),
    ('b.cs','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b010),('imm','NUM')),
    ('b.hs','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b010),('imm','NUM')),
    ('b.cc','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b110),('imm','NUM')),
    ('b.lo','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b110),('imm','NUM')),
    ('b.ns','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b001),('imm','NUM')),
    ('b.mi','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b001),('imm','NUM')),
    ('b.nc','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b101),('imm','NUM')),
    ('b.pl','NUM'): ('2b_off8',('size',0b01),('mjropc',0b011),('func',0b101),('imm','NUM')),
    ('bl.zs','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b000),('imm','NUM')),
    ('bl.eq','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b000),('imm','NUM')),
    ('bl.zc','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b100),('imm','NUM')),
    ('bl.ne','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b100),('imm','NUM')),
    ('bl.cs','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b010),('imm','NUM')),
    ('bl.hs','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b010),('imm','NUM')),
    ('bl.cc','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b110),('imm','NUM')),
    ('bl.lo','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b110),('imm','NUM')),
    ('bl.ns','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b001),('imm','NUM')),
    ('bl.mi','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b001),('imm','NUM')),
    ('bl.nc','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b101),('imm','NUM')),
    ('bl.pl','NUM'):('2b_off8',('size',0b01),('mjropc',0b111),('func',0b101),('imm','NUM')),
    # 9bit offsets
    ('b','NUM'):    ('2b_off9',('size',0b01),('mjropc',0b111),('func',0b11),('imm','NUM')),
    ('bl','NUM'):   ('2b_off9',('size',0b01),('mjropc',0b111),('func',0b11),('imm','NUM')),
    }
