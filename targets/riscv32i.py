# a simple unnamed architecture, mainly for testing the assembler
ISA_FEATURES = ('LITTLE','REGS','JUMP_REL','JUMP_NPC','POST_SHIFT')
INSTRUCTION_ALIGNMENT = 0
PAD_BYTE = 0x00 # Prefered Byte to pad with

REGISTERS = {
    # Base registers
    'x0':   0   ,'x1':   1  ,'x2':   2  ,'x3':   3  ,'x4':   4,
    'x5':   5   ,'x6':   6  ,'x7':   7  ,'x8':   8  ,'x9':   9,
    'x10':  10  ,'x11':  11 ,'x12':  12 ,'x13':  13 ,'x14':  14,
    'x15':  15  ,'x16':  16 ,'x17':  17 ,'x18':  18 ,'x19':  19,
    'x20':  20  ,'x21':  21 ,'x22':  22 ,'x23':  23 ,'x24':  24,
    'x25':  25  ,'x26':  26 ,'x27':  27 ,'x28':  28 ,'x29':  29,
    'x30':  30  ,'x31':  31,
    'zero': 0   ,'ra':   1  ,'sp':   2  ,'gp':   3  ,'tp':   4,
    't0':   5   ,'t1':   6  ,'t2':   7  ,'s0':   8  ,'fp':   8,
    's1':   9   ,'a0':   10 ,'a1':   11 ,'a2':   12 ,'a3':   13,
    'a4':   14  ,'a5':   15 ,'a6':   16 ,'a7':   17 ,'s2':   18,
    's3':   19  ,'s4':   20 ,'s5':   21 ,'s6':   22 ,'s7':   23,
    's8':   24  ,'s9':   25 ,'s10':  26 ,'s11':  27 ,'t3':   28,
    't4':   29  ,'t5':   30 ,'t6':   31,
    # Floating point registers
    'f0':   0   ,'f1':   1  ,'f2':   2  ,'f3':   3  ,'f4':   4,
    'f5':   5   ,'f6':   6  ,'f7':   7  ,'f8':   8  ,'f9':   9,
    'f10':  10  ,'f11':  11 ,'f12':  12 ,'f13':  13 ,'f14':  14,
    'f15':  15  ,'f16':  16 ,'f17':  17 ,'f18':  18 ,'f19':  19,
    'f20':  20  ,'f21':  21 ,'f22':  22 ,'f23':  23 ,'f24':  24,
    'f25':  25  ,'f26':  26 ,'f27':  27 ,'f28':  28 ,'f29':  29,
    'f30':  30  ,'f31':  31,
    'ft0':  0   ,'ft1':  1  ,'ft2':  2  ,'ft3':  3  ,'ft4':  4,
    'ft5':  5   ,'ft6':  6  ,'ft7':  7  ,'fs0':  8  ,'fs1':  9,
    'fa0':  10  ,'fa1':  11 ,'fa2':  12 ,'fa3':  13 ,'fa4':  14,
    'fa5':  15  ,'fa6':  16 ,'fa7':  17 ,'fs2':  18 ,'fs3':  19,
    'fs4':  20  ,'fs5':  21 ,'fs6':  22 ,'fs7':  23 ,'fs8':  24,
    'fs9':  25  ,'fs10': 26 ,'fs11': 27 ,'ft8':  28 ,'ft9':  29,
    'ft10': 30  ,'ft11': 31,
    # Fence instruction things
    'i':    8   ,'iw':   9  ,'ir':  10  ,'irw': 11  ,'io':  12,
    'iow': 13   ,'ior': 14  ,'iorw':15,
    'o':    4   ,'ow':   5  ,'or':   6  ,'orw':  7,
    'r':    2   ,'rw':   3,
    'w':    1,
    }

FORMATS = {
    'r':   (
        32,
        ('funct7',7),
        ('rs2',5),
        ('rs1',5),
        ('funct3',3),
        ('rd',5),
        ('opcode',7)),
    'i':   (
        32,
        ('imm12',12),
        ('rs1',5),
        ('funct3',3),
        ('rd',5),
        ('opcode',7)),
    's':   (
        37,
        ('imm12',12),
        ('rs2',5),
        ('rs1',5),
        ('funct3',3),
        ('blank',5),
        ('opcode',7)),
    'b':   (
        37,
        ('imm12',12),
        ('rs2',5),
        ('rs1',5),
        ('funct3',3),
        ('blank',5),
        ('opcode',7)),
    'u':   (
        32,
        ('imm20',20),
        ('rd',5),
        ('opcode',7)),
    'j':    (
        32,
        ('imm20',20),
        ('rd',5),
        ('opcode',7)),
    'fence':(
        32,
        ('fm',4),
        ('pred',4),
        ('succ',4),
        ('rs1',5),
        ('funct3',3),
        ('rd',5),
        ('opcode',7)),
    }

POST_SHIFT = {
    's':   (32,
        (0x0001FFF07F),
        (0x003E000000,18),
        (0x1FC0000000,5)),
    'b':   (32,
        (0x0001FFF07F),
        (0x1000000000,5),
        (0x0800000000,28),
        (0x07E0000000,4),
        (0x001E000000,17)),
    'j':    (32,
        (0x80000FFF),
        (0x7F800000,11),
        (0x00400000,2),
        (0x003FF000,-9)),
    }


INSTRUCTIONS = {
    # RV32I instructions
    # u&j format
    ('lui'  ,'REG','NUM'):      ('u',('opcode',0b0110111),('rd','REG'),('imm20','NUM',12)),
    ('auipc','REG','NUM'):      ('u',('opcode',0b0010111),('rd','REG'),('imm20','NUM',12)),
    ('jal'  ,'REG','NUM'):      ('j',('opcode',0b1101111),('rd','REG'),('imm20','NUM',1)),
    # i format
    ('jalr' ,'REG','NUM','REG'):('i',('opcode',0b1101111),('rd','REG'),('funct3',0b000),('imm12','NUM'),('rs1','REG')),
    ('lb'   ,'REG','NUM','REG'):('i',('opcode',0b0000011),('rd','REG'),('funct3',0b000),('imm12','NUM'),('rs1','REG')),
    ('lh'   ,'REG','NUM','REG'):('i',('opcode',0b0000011),('rd','REG'),('funct3',0b001),('imm12','NUM'),('rs1','REG')),
    ('lw'   ,'REG','NUM','REG'):('i',('opcode',0b0000011),('rd','REG'),('funct3',0b010),('imm12','NUM'),('rs1','REG')),
    ('lbu'  ,'REG','NUM','REG'):('i',('opcode',0b0000011),('rd','REG'),('funct3',0b100),('imm12','NUM'),('rs1','REG')),
    ('lhu'  ,'REG','NUM','REG'):('i',('opcode',0b0000011),('rd','REG'),('funct3',0b101),('imm12','NUM'),('rs1','REG')),
    ('addi' ,'REG','REG','NUM'):('i',('opcode',0b0010011),('rd','REG'),('funct3',0b000),('rs1','REG'),('imm12','NUM')),
    ('slti' ,'REG','REG','NUM'):('i',('opcode',0b0010011),('rd','REG'),('funct3',0b010),('rs1','REG'),('imm12','NUM')),
    ('sltiu','REG','REG','NUM'):('i',('opcode',0b0010011),('rd','REG'),('funct3',0b011),('rs1','REG'),('imm12','NUM')),
    ('xori' ,'REG','REG','NUM'):('i',('opcode',0b0010011),('rd','REG'),('funct3',0b100),('rs1','REG'),('imm12','NUM')),
    ('ori'  ,'REG','REG','NUM'):('i',('opcode',0b0010011),('rd','REG'),('funct3',0b110),('rs1','REG'),('imm12','NUM')),
    ('andi' ,'REG','REG','NUM'):('i',('opcode',0b0010011),('rd','REG'),('funct3',0b111),('rs1','REG'),('imm12','NUM')),
    ('ecall',):                 ('i',('opcode',0b1110011),('rd',0)    ,('funct3',0b000),('rs1',0)    ,('imm12',0)),
    ('ebreak',):                ('i',('opcode',0b1110011),('rd',0)    ,('funct3',0b000),('rs1',0)    ,('imm12',1)),
    # b format
    ('beq'  ,'REG','REG','NUM'):('b',('opcode',0b1100011),('funct3',0b000),('rs1','REG'),('rs2','REG'),('imm12','NUM',1),('blank',0)),
    ('bne'  ,'REG','REG','NUM'):('b',('opcode',0b1100011),('funct3',0b001),('rs1','REG'),('rs2','REG'),('imm12','NUM',1),('blank',0)),
    ('blt'  ,'REG','REG','NUM'):('b',('opcode',0b1100011),('funct3',0b100),('rs1','REG'),('rs2','REG'),('imm12','NUM',1),('blank',0)),
    ('bge'  ,'REG','REG','NUM'):('b',('opcode',0b1100011),('funct3',0b101),('rs1','REG'),('rs2','REG'),('imm12','NUM',1),('blank',0)),
    ('bltu' ,'REG','REG','NUM'):('b',('opcode',0b1100011),('funct3',0b110),('rs1','REG'),('rs2','REG'),('imm12','NUM',1),('blank',0)),
    ('bgeu' ,'REG','REG','NUM'):('b',('opcode',0b1100011),('funct3',0b111),('rs1','REG'),('rs2','REG'),('imm12','NUM',1),('blank',0)),
    # s format
    ('sb'   ,'REG','REG','NUM'):('s',('opcode',0b0100011),('funct3',0b000),('rs1','REG'),('rs2','REG'),('imm12','NUM'),('blank',0)),
    ('sh'   ,'REG','REG','NUM'):('s',('opcode',0b0100011),('funct3',0b001),('rs1','REG'),('rs2','REG'),('imm12','NUM'),('blank',0)),
    ('sw'   ,'REG','REG','NUM'):('s',('opcode',0b0100011),('funct3',0b010),('rs1','REG'),('rs2','REG'),('imm12','NUM'),('blank',0)),
    # r format
    ('slli' ,'REG','REG','NUM'):('r',('opcode',0b0010011),('rd','REG'),('funct3',0b001),('rs1','REG'),('rs2','NUM'),('funct7',0b0000000)),
    ('srli' ,'REG','REG','NUM'):('r',('opcode',0b0010011),('rd','REG'),('funct3',0b101),('rs1','REG'),('rs2','NUM'),('funct7',0b0000000)),
    ('srai' ,'REG','REG','NUM'):('r',('opcode',0b0010011),('rd','REG'),('funct3',0b101),('rs1','REG'),('rs2','NUM'),('funct7',0b0100000)),
    ('add'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b000),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    ('sub'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b000),('rs1','REG'),('rs2','REG'),('funct7',0b0100000)),
    ('sll'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b001),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    ('slt'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b010),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    ('sltu' ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b011),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    ('xor'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b100),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    ('srl'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b101),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    ('sra'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b101),('rs1','REG'),('rs2','REG'),('funct7',0b0100000)),
    ('or'   ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b110),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    ('and'  ,'REG','REG','REG'):('r',('opcode',0b0110011),('rd','REG'),('funct3',0b111),('rs1','REG'),('rs2','REG'),('funct7',0b0000000)),
    # Fence instructions
    ('fence','REG','REG'):      ('fence',('opcode',0b0001111),('rd',0),('funct3',0b000),('rs1',0),('fm',0b0000),('pred','REG'),('succ','REG')),
    ('fence.tso',):             ('fence',('opcode',0b0001111),('rd',0),('funct3',0b000),('rs1',0),('fm',0b1000),('pred',0x3),('succ',0x3)),
    ('fence.i',):               ('fence',('opcode',0b0001111),('rd',0),('funct3',0b001),('rs1',0),('fm',0b0000),('pred',0x0),('succ',0x0)),
    }
