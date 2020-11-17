# a simple unnamed architecture, mainly for testing the assembler
ISA_FEATURES = ('COND')
ADDRESS_WIDTH = 16
DATA_WIDTH = 8
INSTRUCTION_ALIGNMENT = 0
ENDIANESS = 0 # Little Endian
PAD_BYTE = 0x00 # Prefered Byte to pad with

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
        ('function',0b000)
        ),
    'ret':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b001)
        ),
    'lpc':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b010)
        ),
    'ecal':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b011)
        ),
    'eret':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b110)
        ),
    'halt':  (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b111)
        ),
    # register stuff
    'not':  (
        '1b',
        ('size',0),
        ('opcode',0b0010),
        ('function','REG')
        ),
    'neg':  (
        '1b',
        ('size',0),
        ('opcode',0b0011),
        ('function','REG')
        ),
    'inc':  (
        '1b',
        ('size',0),
        ('opcode',0b0100),
        ('function','REG')
        ),
    'dec':  (
        '1b',
        ('size',0),
        ('opcode',0b0101),
        ('function','REG')
        ),
    'clr':  (
        '1b',
        ('size',0),
        ('opcode',0b0110),
        ('function','REG')
        ),
    'set':  (
        '1b',
        ('size',0),
        ('opcode',0b0111),
        ('function','REG')
        ),
    'push':  (
        '1b',
        ('size',0),
        ('opcode',0b1000),
        ('function','REG')
        ),
    'pop':  (
        '1b',
        ('size',0),
        ('opcode',0b1001),
        ('function','REG')
        ),
    'jr':  (
        '1b',
        ('size',0),
        ('opcode',0b1010),
        ('function','REG')
        ),
    'jrl':  (
        '1b',
        ('size',0),
        ('opcode',0b1011),
        ('function','REG')
        ),
    'jrz':  (
        '1b',
        ('size',0),
        ('opcode',0b1100),
        ('function','REG')
        ),
    'jrzl':  (
        '1b',
        ('size',0),
        ('opcode',0b1101),
        ('function','REG')
        ),
    # 2 Byte instructions
    }
