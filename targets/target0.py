# a simple unnamed architecture, mainly for testing the assembler
ISA_FEATURES = ('COND')
ADDRESS_WIDTH = 16
DATA_WIDTH = 8
INSTRUCTION_ALIGNMENT = 0
ENDIANESS = 0 # Little Endian
PAD_BYTE = 0x00 # Prefered Byte to pad with
BRANCHES = {
    'bc':   0,
    'bcl':  0,
    } # (instruction,alignment)

REGISTERS = {
    'ar':   0,
    't0':   1,
    't1':   2,
    't2':   3,
    's0':   4,
    's1':   5,
    's2':   6,
    's3':   7,
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
    '2b0':   (
        16,
        ('dest',3),
        ('source',3),
        ('opcode',8),
        ('size',2)),
    '2b1':   (
        16,
        ('dest',3),
        ('imm',4),
        ('opcode',7),
        ('size',2)),
    '2b2':   (
        16,
        ('dest',3),
        ('imm',6),
        ('opcode',5),
        ('size',2)),
    '2b3':   (
        16,
        ('dest',3),
        ('imm',8),
        ('opcode',3),
        ('size',2)),
    }

CONDITIONS = {
    'zs':   0,
    'zc':   1,
    'cs':   2,
    'cc':   3,
    'ns':   4,
    'nc':   5,
    'vs':   6,
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
    'nop':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b000)),
    'ret':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b001)),
    'lpc':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b010)),
    'ecal':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b011)),
    'eret':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b110)),
    'halt':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b111)),
    # register stuff
    'not':  (
        '1b',
        ('size',0),
        ('opcode',0b0010),
        ('function','REG')),
    'neg':  (
        '1b',
        ('size',0),
        ('opcode',0b0011),
        ('function','REG')),
    'inc':  (
        '1b',
        ('size',0),
        ('opcode',0b0100),
        ('function','REG')),
    'dec':  (
        '1b',
        ('size',0),
        ('opcode',0b0101),
        ('function','REG')),
    'clr':  (
        '1b',
        ('size',0),
        ('opcode',0b0110),
        ('function','REG')),
    'set':  (
        '1b',
        ('size',0),
        ('opcode',0b0111),
        ('function','REG')),
    'push':  (
        '1b',
        ('size',0),
        ('opcode',0b1000),
        ('function','REG')),
    'pop':  (
        '1b',
        ('size',0),
        ('opcode',0b1001),
        ('function','REG')),
    'jr':  (
        '1b',
        ('size',0),
        ('opcode',0b1010),
        ('function','REG')),
    'jrl':  (
        '1b',
        ('size',0),
        ('opcode',0b1011),
        ('function','REG')),
    'jrz':  (
        '1b',
        ('size',0),
        ('opcode',0b1100),
        ('function','REG')),
    'jrzl':  (
        '1b',
        ('size',0),
        ('opcode',0b1101),
        ('function','REG')),
    # 2 Byte instructions
    '2and':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00000000),
        ('dest','REG'),
        ('source','REG')),
    '2bic':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10000000),
        ('dest','REG'),
        ('source','REG')),
    '2or':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01000000),
        ('dest','REG'),
        ('source','REG')),
    '2xor':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11000000),
        ('dest','REG'),
        ('source','REG')),
    '2nor':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00100000),
        ('dest','REG'),
        ('source','REG')),
    '2not':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10100000),
        ('dest','REG'),
        ('source','REG')),
    '2sll':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01100000),
        ('dest','REG'),
        ('source','REG')),
    '2srl':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11100000),
        ('dest','REG'),
        ('source','REG')),
    '2sra':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00010000),
        ('dest','REG'),
        ('source','REG')),
    '2add':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10010000),
        ('dest','REG'),
        ('source','REG')),
    '2sub':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01010000),
        ('dest','REG'),
        ('source','REG')),
    '2adc':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11010000),
        ('dest','REG'),
        ('source','REG')),
    '2sbb':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00110000),
        ('dest','REG'),
        ('source','REG')),
    '2inc':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10110000),
        ('dest','REG'),
        ('source','REG')),
    '2dec':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01110000),
        ('dest','REG'),
        ('source','REG')),
    '2neg':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11110000),
        ('dest','REG'),
        ('source','REG')),
    '2mov':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00001000),
        ('dest','REG'),
        ('source','REG')),
    '2cmp':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10001000),
        ('dest','REG'),
        ('source','REG')),
    '2cmn':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01001000),
        ('dest','REG'),
        ('source','REG')),
    '2cma':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11001000),
        ('dest','REG'),
        ('source','REG')),
    '2cmx':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00101000),
        ('dest','REG'),
        ('source','REG')),
    '2lb':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10101000),
        ('dest','REG'),
        ('source','REG')),
    '2sb':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01101000),
        ('dest','REG'),
        ('source','REG')),
    '2slli':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00011000),
        ('dest','REG'),
        ('source','NUM')),
    '2srli':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10011000),
        ('dest','REG'),
        ('source','NUM')),
    '2srai':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01011000),
        ('dest','REG'),
        ('source','NUM')),
    # Immediate/offset land
    '2andi':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0000100),
        ('dest','REG'),
        ('imm','NUM')),
    '2xori':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b1000100),
        ('dest','REG'),
        ('imm','NUM')),
    '2ori':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0100100),
        ('dest','REG'),
        ('imm','NUM')),
    '2addi':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b1100100),
        ('dest','REG'),
        ('imm','NUM')),
    '2cmpi':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0010100),
        ('dest','REG'),
        ('imm','NUM')),
    '2lbsp':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b1010100),
        ('dest','REG'),
        ('imm','NUM')),
    '2sbsp':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0110100),
        ('dest','REG'),
        ('imm','NUM')),
    '2jr':  (
        '2b2',
        ('size',0b01),
        ('opcode',0b01100),
        ('dest','REG'),
        ('imm','NUM')),
    '2jrl':  (
        '2b2',
        ('size',0b01),
        ('opcode',0b11100),
        ('dest','REG'),
        ('imm','NUM')),
    '2lcsr':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b010),
        ('dest','REG'),
        ('imm','REG')),
    '2scsr':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b110),
        ('dest','REG'),
        ('imm','REG')),
    '2bc':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b001),
        ('dest','COND'),
        ('imm','NUM')),
    '2bcl':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b101),
        ('dest','COND'),
        ('imm','NUM')),
    '2li':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b011),
        ('dest','REG'),
        ('imm','NUM')),
    }
