# a simple unnamed architecture, mainly for testing the assembler
ISA_FEATURES = ('LITTLE','REGS','COND','JUMP_REL','JUMP_NPC')
INSTRUCTION_ALIGNMENT = 0
PAD_BYTE = 0x00 # Prefered Byte to pad with
JUMP_REL = (
    'bc',
    'bcl',
    )

REGISTERS = {
    'ar':   0,
    'la':  1,
    't0':   2,
    't1':   3,
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
        ('imm',5),
        ('opcode',6),
        ('size',2)),
    '2b2':   (
        16,
        ('dest',3),
        ('imm',7),
        ('opcode',4),
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
    ('nop',): (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b000)),
    ('ret',): (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b100)),
    ('lpc',): (
        '1b',
        ('size',0),
        ('opcode',0b0000),
        ('function',0b010)),
    ('ecal',): (
        '1b',
        ('size',0),
        ('opcode',0b1000),
        ('function',0b000)),
    ('eret',): (
        '1b',
        ('size',0),
        ('opcode',0b1000),
        ('function',0b011)),
    ('halt',): (
        '1b',
        ('size',0),
        ('opcode',0b1000),
        ('function',0b111)),
    # register stuff
    ('clr','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b0100),
        ('function','REG')),
    ('set','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b1100),
        ('function','REG')),
    ('push','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b0010),
        ('function','REG')),
    ('pop','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b1010),
        ('function','REG')),
    ('jr','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b0110),
        ('function','REG')),
    ('jrl','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b1110),
        ('function','REG')),
    ('not','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b0001),
        ('function','REG')),
    ('neg','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b1001),
        ('function','REG')),
    ('inc','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b0101),
        ('function','REG')),
    ('dec','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b1101),
        ('function','REG')),
    ('sll','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b0011),
        ('function','REG')),
    ('srl','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b1011),
        ('function','REG')),
    ('sra','REG'): (
        '1b',
        ('size',0),
        ('opcode',0b0111),
        ('function','REG')),
    # 2 Byte instructions
    ('and','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b00000000),
        ('dest','REG'),
        ('source','REG')),
    ('bic','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b10000000),
        ('dest','REG'),
        ('source','REG')),
    ('or','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b01000000),
        ('dest','REG'),
        ('source','REG')),
    ('xor','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b11000000),
        ('dest','REG'),
        ('source','REG')),
    ('not','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b00100000),
        ('dest','REG'),
        ('source','REG')),
    ('sll','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b10100000),
        ('dest','REG'),
        ('source','REG')),
    ('srl','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b01100000),
        ('dest','REG'),
        ('source','REG')),
    ('sra','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b11100000),
        ('dest','REG'),
        ('source','REG')),
    ('add','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b00010000),
        ('dest','REG'),
        ('source','REG')),
    ('sub','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b10010000),
        ('dest','REG'),
        ('source','REG')),
    ('adc','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b01010000),
        ('dest','REG'),
        ('source','REG')),
    ('sbb','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b11010000),
        ('dest','REG'),
        ('source','REG')),
    ('inc','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b00110000),
        ('dest','REG'),
        ('source','REG')),
    ('dec','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b10110000),
        ('dest','REG'),
        ('source','REG')),
    ('neg','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b01110000),
        ('dest','REG'),
        ('source','REG')),
    ('mov','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b11110000),
        ('dest','REG'),
        ('source','REG')),
    ('lb','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b00001000),
        ('dest','REG'),
        ('source','REG')),
    ('sb','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b10001000),
        ('dest','REG'),
        ('source','REG')),
    ('cmp','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b01001000),
        ('source','REG'),
        ('dest','REG')),
    ('cmn','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b11001000),
        ('source','REG'),
        ('dest','REG')),
    ('cma','REG','REG'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b00101000),
        ('source','REG'),
        ('dest','REG')),
    # Immediate/offset land
    ('sll','REG','NUM'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b10101000),
        ('dest','REG'),
        ('source','NUM')),
    ('srl','REG','NUM'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b01101000),
        ('dest','REG'),
        ('source','NUM')),
    ('sra','REG','NUM'): (
        '2b0',
        ('size',0b01),
        ('opcode',0b11101000),
        ('dest','REG'),
        ('source','NUM')),
    ('and','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b000100),
        ('dest','REG'),
        ('imm','NUM')),
    ('xor','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b100100),
        ('dest','REG'),
        ('imm','NUM')),
    ('or','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b010100),
        ('dest','REG'),
        ('imm','NUM')),
    ('add','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b110100),
        ('dest','REG'),
        ('imm','NUM')),
    ('cmp','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b001100),
        ('dest','REG'),
        ('imm','NUM')),
    ('cma','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b101100),
        ('dest','REG'),
        ('imm','NUM')),
    ('lbsp','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b011100),
        ('dest','REG'),
        ('imm','NUM')),
    ('sbsp','REG','NUM'): (
        '2b1',
        ('size',0b01),
        ('opcode',0b111100),
        ('dest','REG'),
        ('imm','NUM')),
    ('lcsr','REG','REG'): (
        '2b2',
        ('size',0b01),
        ('opcode',0b0010),
        ('dest','REG'),
        ('imm','REG')),
    ('scsr','REG','REG'): (
        '2b2',
        ('size',0b01),
        ('opcode',0b1010),
        ('dest','REG'),
        ('imm','REG')),
    ('mov','REG','NUM'): (
        '2b3',
        ('size',0b01),
        ('opcode',0b110),
        ('dest','REG'),
        ('imm','NUM')),
    ('bc','COND','NUM'): (
        '2b3',
        ('size',0b01),
        ('opcode',0b001),
        ('dest','COND'),
        ('imm','NUM')),
    ('bcl','COND','NUM'): (
        '2b3',
        ('size',0b01),
        ('opcode',0b101),
        ('dest','COND'),
        ('imm','NUM')),
    }
