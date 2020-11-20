# a simple unnamed architecture, mainly for testing the assembler
ISA_FEATURES = ('LITTLE','COND','JUMP_REL','JUMP_NPC')
ADDRESS_WIDTH = 16
DATA_WIDTH = 8
INSTRUCTION_ALIGNMENT = 0
ENDIANESS = 0 # Little Endian
PAD_BYTE = 0x00 # Prefered Byte to pad with
JUMP_REL = (
    'bc',
    'bcl',
    )

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
    'notb':  (
        '1b',
        ('size',0),
        ('opcode',0b0010),
        ('function','REG')),
    'negb':  (
        '1b',
        ('size',0),
        ('opcode',0b0011),
        ('function','REG')),
    'incb':  (
        '1b',
        ('size',0),
        ('opcode',0b0100),
        ('function','REG')),
    'decb':  (
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
    'jrb':  (
        '1b',
        ('size',0),
        ('opcode',0b1010),
        ('function','REG')),
    'jrlb':  (
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
    'and':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00000000),
        ('dest','REG'),
        ('source','REG')),
    'bic':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10000000),
        ('dest','REG'),
        ('source','REG')),
    'or':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01000000),
        ('dest','REG'),
        ('source','REG')),
    'xor':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11000000),
        ('dest','REG'),
        ('source','REG')),
    'nor':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00100000),
        ('dest','REG'),
        ('source','REG')),
    'not':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10100000),
        ('dest','REG'),
        ('source','REG')),
    'sll':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01100000),
        ('dest','REG'),
        ('source','REG')),
    'srl':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11100000),
        ('dest','REG'),
        ('source','REG')),
    'sra':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00010000),
        ('dest','REG'),
        ('source','REG')),
    'add':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10010000),
        ('dest','REG'),
        ('source','REG')),
    'sub':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01010000),
        ('dest','REG'),
        ('source','REG')),
    'adc':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11010000),
        ('dest','REG'),
        ('source','REG')),
    'sbb':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00110000),
        ('dest','REG'),
        ('source','REG')),
    'inc':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10110000),
        ('dest','REG'),
        ('source','REG')),
    'dec':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01110000),
        ('dest','REG'),
        ('source','REG')),
    'neg':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11110000),
        ('dest','REG'),
        ('source','REG')),
    'mov':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00001000),
        ('dest','REG'),
        ('source','REG')),
    'cmp':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10001000),
        ('dest','REG'),
        ('source','REG')),
    'cmn':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01001000),
        ('dest','REG'),
        ('source','REG')),
    'cma':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11001000),
        ('dest','REG'),
        ('source','REG')),
    'cmx':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00101000),
        ('dest','REG'),
        ('source','REG')),
    'lb':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10101000),
        ('dest','REG'),
        ('source','REG')),
    'sb':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01101000),
        ('dest','REG'),
        ('source','REG')),
    'orn':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b11101000),
        ('dest','REG'),
        ('source','REG')),
    'slli':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b00011000),
        ('dest','REG'),
        ('source','NUM')),
    'srli':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b10011000),
        ('dest','REG'),
        ('source','NUM')),
    'srai':  (
        '2b0',
        ('size',0b01),
        ('opcode',0b01011000),
        ('dest','REG'),
        ('source','NUM')),
    # Immediate/offset land
    'andi':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0000100),
        ('dest','REG'),
        ('imm','NUM')),
    'xori':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b1000100),
        ('dest','REG'),
        ('imm','NUM')),
    'ori':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0100100),
        ('dest','REG'),
        ('imm','NUM')),
    'addi':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b1100100),
        ('dest','REG'),
        ('imm','NUM')),
    'cmpi':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0010100),
        ('dest','REG'),
        ('imm','NUM')),
    'lbsp':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b1010100),
        ('dest','REG'),
        ('imm','NUM')),
    'sbsp':  (
        '2b1',
        ('size',0b01),
        ('opcode',0b0110100),
        ('dest','REG'),
        ('imm','NUM')),
    'jr':  (
        '2b2',
        ('size',0b01),
        ('opcode',0b01100),
        ('dest','REG'),
        ('imm','NUM')),
    'jrl':  (
        '2b2',
        ('size',0b01),
        ('opcode',0b11100),
        ('dest','REG'),
        ('imm','NUM')),
    'lcsr':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b010),
        ('dest','REG'),
        ('imm','REG')),
    'scsr':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b110),
        ('dest','REG'),
        ('imm','REG')),
    'bc':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b001),
        ('dest','COND'),
        ('imm','NUM')),
    'bcl':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b101),
        ('dest','COND'),
        ('imm','NUM')),
    'li':  (
        '2b3',
        ('size',0b01),
        ('opcode',0b011),
        ('dest','REG'),
        ('imm','NUM')),
    }
