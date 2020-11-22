# Target Syntax

Targets are defined using a collection of constants, dictionaries, and tuples.

Each section below will go through all possible options and variables that can be used:

### Required Constants

|Constant|values|description|
|INSTRUCTION_ALIGNMENT|0-255|Instruction address alignment|
|PAD_BYTE|0-255|Preffered byte to use when padding/aligning|

### ISA_FEATURES

ISA_FEATURES is a tuple that contains some of the following strings to indicate the optional features the target implements:

|String|description|
|'BIG'|Indicates the target is big endian|
|'LITTLE'|Indicates the target is little endian|
|'REGS'|Indicates the target implements registers|
|'COND'|Indicates the target implements conditions|
|'JUMP_REL'|Indicates the target has relative jumps|
|'JUMP_ABS'|Indicates the target has absolute jumps|
|'JUMP_NPC'|Indicates the target uses next PC for jumps|

### REGISTERS

* 'REGS' feature required

REGISTERS is a dictionary containing all possible referenced registers in the target with their encoded values, below is an example:

`REGISTERS = {
    'register_0':   0,
    'register_1':   1,
    'register_2':   2,
    'register_3':   3,
    }`

### CONDITIONS

* 'COND' feature required

CONDITIONS is a dictionary containing all possible referenced conditions in the target with their encoded values, below is an example:

`CONDITIONS = {
    'condition_C':   0,
    'condition_N':   1,
    'condition_Z':   2,
    'condition_V':   3,
    }`

### JUMP_REL

* 'JUMP_REL' feature required

JUMP_REL is a tuple with a collection of all jumps that use relative addressing, below is an example:

`JUMP_REL = (
    'BRANCH',
    'BRANCH_CONDITIONAL',
    'BRANCH_IF_ZERO',
    )`

### JUMP_ABS

* 'JUMP_ABS' feature required

JUMP_ABS is a tuple with a collection of all jumps that use absolute addressing, below is an example:

`JUMP_ABS = (
    'JUMP',
    'JUMP_CONDITIONAL',
    'JUMP_IF_ZERO',
    )`

### FORMATS - Required

FORMATS is a dictionary containing format definitions for use with the INSTRUCTIONS dictionary, below is an example of two formats taken from the 8008_new target:

`FORMATS = {
    '1b0':   (          # Name of the format
        8,              # Bit-Width of the format
        ('opcode',8)),  # Operand format (NAME, BIT-WIDTH)
    
    '2b0':   (          # Name of the format
        16,             # Bit-Width of the format
        ('imm',8),      # 1st operand format (NAME, BIT-WIDTH)
        ('opcode',8)),  # 2nd operand format (NAME, BIT-WIDTH)
    }`

### INSTRUCTIONS - Required

INSTRUCTIONS is a dictionary containing instruction definitions

The following keywords can be present in the key after the instruction name:

|string|description|
|'NUM'|A number|
|'REG'|A register|
|'COND'|A condition|
|'_*any string*'|Any string that doesn't match the above|

Below is an example of four instructions taken from the 8008_new target:


`INSTRUCTIONS = {
    ('hlt',): (                 # Instruction name
        '1b0',                  # Format used
        ('opcode',0b11111111)), # Operand filled with a number
    
    ('jmp','NUM'): (            # Instruction name + number operand
        '3b0',                  # Format used
        ('opcode',0b01000100),  # Operand filled with a number
        ('imm','NUM')),         # Operand filled with
                                #   a number requested as an argument
    
    ('mvi','REG','NUM'): (      # Instruction name
                                #   + register operand + number operand
        '2b1',                  # Format used
        ('opcode',0b110),       # Operand filled with a number
        ('function',0b00),      # Operand filled with a number
        ('dest','REG'),         # Operand filled with
                                #   a register requested as an argument
        ('imm','NUM')),         # Operand filled with
                                #   a number requested as an argument
    
    ('mov','_m','REG'): (       # Instruction name
        '1b4',                  # Format used
        ('function',0b11),      # Operand filled with a number
        ('dest',0b111,True),    # Operand filled with a number
                                #   and a pass, meaning "_m" is skipped over
                                #   and is not used in the instruction
        ('source','REG')),      # Operand filled with
                                #   a register requested as an argument
    }`
