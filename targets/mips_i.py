ISA_FEATURES = ()
ADDRESS_WIDTH = 32
DATA_WIDTH = 32
INSTRUCTION_ALIGNMENT = 2
ENDIANESS = 1 # Big Endian
PAD_BYTE = 0x00 # Prefered Byte to pad with

REGISTERS = {
    'zero':   0,
    'at':     1,
    'v0':     2,
    'v1':     3,
    'a0':     4,
    'a1':     5,
    'a2':     6,
    'a3':     7,
    't0':     8,
    't1':     9,
    't2':     10,
    't3':     11,
    't4':     12,
    't5':     13,
    't6':     14,
    't7':     15,
    's0':     16,
    's1':     17,
    's2':     18,
    's3':     19,
    's4':     20,
    's5':     21,
    's6':     22,
    's7':     23,
    't8':     24,
    't9':     25,
    'k0':     26,
    'k1':     27,
    'gp':     28,
    'sp':     29,
    'fp':     30,
    'ra':     31
    }

FORMATS = {
    'R':   (
        32,
        ('opcode',6),
        ('rs',5),
        ('rt',5),
        ('rd',5),
        ('shamt',5),
        ('funct',6)),
    'I':   (
        32,
        ('opcode',6),
        ('rs',5),
        ('rt',5),
        ('immediate',16)),
    'J':   (
        32,
        ('opcode',6),
        ('address',26)),
    }

INSTRUCTIONS = {
    # Shifts
    'SLL':  (
        'R',
        (
            ('opcode',0),
            ('rs',0),
            ('rd','REG'),
            ('rt','REG'),
            ('shamt','NUM'),
            ('funct',0)
            )
        ),
    'SRL':  (
        'R',
        (
            ('opcode',0),
            ('rs',0),
            ('rd','REG'),
            ('rt','REG'),
            ('shamt','NUM'),
            ('funct',2)
            )
        ),
    'SRA':  (
        'R',
        (
            ('opcode',0),
            ('rs',0),
            ('rd','REG'),
            ('rt','REG'),
            ('shamt','NUM'),
            ('funct',3)
            )
        ),
    'SLLV':  (
        'R',
        (
            ('opcode',0),
            ('rd','REG'),
            ('rs','REG'),
            ('rt','REG'),
            ('shamt',0),
            ('funct',4)
            )
        ),
    'SRLV':  (
        'R',
        (
            ('opcode',0),
            ('rd','REG'),
            ('rs','REG'),
            ('rt','REG'),
            ('shamt',0),
            ('funct',6)
            )
        ),
    'SRAV':  (
        'R',
        (
            ('opcode',0),
            ('rd','REG'),
            ('rs','REG'),
            ('rt','REG'),
            ('shamt',0),
            ('funct',7)
            )
        ),
    # Jumps and branches
    'JR':  (
        'R',
        (
            ('opcode',0),
            ('rt',0),
            ('rd',0),
            ('rs','REG'),
            ('shamt',0),
            ('funct',8)
            )
        ),
    'JALR':  (
        'R',
        (
            ('opcode',0),
            ('rt',0),
            ('rd','REG'),
            ('rs','REG'),
            ('shamt',0),
            ('funct',9)
            )
        ),
    'LB':  (
        'I',
        (
            ('opcode',32),
            ('rt','REG'),
            ('rs','REG'),
            ('immediate','NUM')
            )
        ),
    }
