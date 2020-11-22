import re

ERRORS = {
    0:  "ERROR, line {}: less arguments than required {}, using default 0",
    1:  "ERROR, line {}: register not found, using default 0",
    2:  "ERROR, line {}: condition not found, using default 0",
    3:  "ERROR, line {}: non-digit characters detected, using default 0",
    4:  "ERROR, line {}: invalid target value type, using default 0",
    5:  "FATAL ERROR, line {}: invalid target formatting",
    6:  "WARNING, line {}: label {} already exists, ignoring",
    7:  "WARNING, line {}: constant {} already exists, ignoring",
    8:  "WARNING, line {}: unknown instruction",
    }


class Assembler:
    """
    Assembly interpreter and binary assembler class
    """
    
    def __init__(self,assembly,target,verbose):
        # Clean assembly and number the lines
        self.assembly = self.cleanAssembly(assembly)
        # Load target definitions
        self.instAlign = target.INSTRUCTION_ALIGNMENT
        self.pad_byte = target.PAD_BYTE
        self.registers = target.REGISTERS
        self.formats = target.FORMATS
        self.instructions = target.INSTRUCTIONS
        # Default variables
        self.big_endian = False
        self.conditions = {}
        self.jump_rel = ()
        self.jump_abs = ()
        self.jump_npc = False
        # Import optional overrides
        if "BIG" in target.ISA_FEATURES:
            self.big_endian = 1
        if "COND" in target.ISA_FEATURES:
            self.conditions = target.CONDITIONS
        if "JUMP_REL" in target.ISA_FEATURES:
            self.jump_rel = target.JUMP_REL
        if "JUMP_ABS" in target.ISA_FEATURES:
            self.jump_abs = target.JUMP_ABS
        if "JUMP_NPC" in target.ISA_FEATURES:
            self.jump_npc = True
            
        
        # Initialize variables
        self.constants = {}
        self.labels = {}
        self.verbose = verbose
        
        if verbose:
            print(f"Target has the following features: {target.ISA_FEATURES}.\n"
                +f"Target has {len(target.INSTRUCTIONS)} instructions available")
    
    
    def listGet(self,l,index,default=False):
        """Dict's get method for a list"""
        try:
            return(l[index])
        except:
            return(default)
    
    
    def twoComp(self,num,length):
        """Converts number(if negative) into 2's complement"""
        return(
            (num - (1 << length)) & ((2 ** length) - 1) if num < 0 else num)
    
    def cleanAssembly(self,assembly):
        """Initial assembly cleaning and line numbering"""
        cleaned = {}
        lineNumber = 0
        
        for line in assembly:
            # Increment the line
            lineNumber += 1
            # Remove comments
            uncommented = re.sub('#.*','',line)
            # Remove empty lines
            if not uncommented or uncommented.isspace():
                continue
            # Remove any spaces or tabs before text
            cleaned[lineNumber] = re.sub('^[\s\t]*','',uncommented).lower()
        
        return cleaned
    
    # Converts an instruction format into an instruction, recursive.
    def instFormatter(self, bitsLeft, inFormat, instruction):
        """Formatter for instructions"""
        # Pop the field
        currentValue = inFormat.pop(0)
        # Subtract the number of bits in the field from the current bits
        bitsLeft -= currentValue[1]
        # Insert value from the field into the instruction
        instruction = instruction | (
            self.twoComp(int(currentValue[0]), currentValue[1]) << bitsLeft)
        # Repeat until out of bits
        if bitsLeft > 0:
            instruction = self.instFormatter(bitsLeft, inFormat, instruction)
        return(instruction)
    
    def formatEncode(self,categorizedLine,line,lineNumber):
        """Encodes the instruction into the format provided by the target"""
        current_instruction = self.instructions[categorizedLine]
        current_format = self.formats[current_instruction[0]]
        current_element = 1
        max_elements = len(line)
        
        instruction_fields = {}
        
        for instField in current_instruction[1:]:
            if isinstance(instField[1],str): inputType = instField[1].upper()
            else: inputType = instField[1]
            if self.listGet(instField,2): is_pass = True
            else: is_pass = False
            
            if isinstance(inputType,int):
                selectedValue = inputType
            elif current_element >= max_elements:
                print(ERRORS[0].format(lineNumber,current_element))
                selectedValue = 0
            # Detect register
            elif inputType.startswith('REG'):
                if line[current_element] in self.registers:
                    selectedValue = self.registers[line[current_element]]
                    current_element += 1
                else:
                    print(ERRORS[1].format(lineNumber))
                    selectedValue = 0
            # Detect condition
            elif inputType.startswith('COND'):
                if line[current_element] in self.conditions:
                    selectedValue = self.conditions[line[current_element]]
                    current_element += 1
                else:
                    print(ERRORS[2].format(lineNumber))
                    selectedValue = 0
            # Detect numbers
            elif inputType.startswith('NUM'):
                if line[current_element][1:].isdigit() and line[current_element][0] == '#':
                    selectedValue = int(line[current_element][1:])
                    # Shift the inputs if needed
                    if inputType.endswith('r'):
                        selectedValue = selectedValue >> instField[2]
                    else:
                        selectedValue = selectedValue << self.listGet(instField,2)
                    current_element += 1
                else:
                    print(ERRORS[3].format(lineNumber))
                    selectedValue = 0
            else:
                print(ERRORS[4].format(lineNumber))
                selectedValue = 0
            
            # Skip over the next element if pass
            if is_pass:
                current_element += 1
            
            instruction_fields[instField[0]] = selectedValue
        
        format_fields = []
        
        for formatField in current_format[1:]:
            try:
                format_fields.append(
                    [instruction_fields[formatField[0]],formatField[1]])
            except:
                print(ERRORS[5].format(lineNumber))
                return []
        
        instruction = self.instFormatter(current_format[0],format_fields,0)
        
        return [byte & 255 for byte in [
            instruction >> (8*x) for x in range(
            current_format[0]//8)][::[1,-1][self.big_endian]]]
        
    
    def cleanLine(self,line):
        """cleans the line and prepares it for easier reading"""
        return(' '.join(
            line.replace('=', ' ').replace(',', ' ').split()).split(' '))
    
    
    def firstPass(self):
        """First pass, finds labels, converts numbers, cleans code further"""
        currentProgress = 0
        delList = []
        nums = {'0x':16,'0o':8,'0b':2}
        for lineNumber in self.assembly.keys():
            line = self.cleanLine(self.assembly[lineNumber])
            
            for num in range(0,len(line)):
                is_imm = line[num].startswith('#')
                # Convert hex/octal/binary numbers
                if any(line[num][is_imm:].startswith(hob) for hob in nums):
                    self.assembly[lineNumber] = self.assembly[lineNumber].replace(
                        line[num],('#'*is_imm)+str(int(
                        line[num][2+is_imm:],nums[line[num][is_imm:2+is_imm]])))
            
            # Instruction alignment, in case the current instruction is misaligned
            if line[0] in self.instructions and self.instAlign:
                alignPower = 2**int(self.instAlign)
                padAmount = (currentProgress % alignPower)
                padAmount = -(padAmount-alignPower) if padAmount else 0
                currentProgress += padAmount
            
            # Categorize operands for easy identification
            categorizedLine = self.categorizeOperands(line)
            
            # Label assignment
            if line[0][-1] == ":":
                labelName = line[0][:-1]
                if self.labels.get(labelName,None) != None and self.verbose:
                    print(ERRORS[6].format(lineNumber,labelName))
                    delList.append(lineNumber)
                else: self.labels[labelName] = currentProgress
                continue
            
            elif categorizedLine in self.instructions:
                instLength = self.formats[self.instructions[
                    categorizedLine][0]][0]//8
                currentProgress += instLength
            
            # Align and pad by a power of two using a provided byte
            elif line[0] == ".align":
                try:
                    is_imm = line[1].startswith('#')
                    alignPower = 2**int(line[1][is_imm:])
                except:
                    print(ERRORS[3].format(lineNumber))
                else:
                    padAmount = (currentProgress % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    currentProgress += padAmount
            
            # Constant assignment
            elif line[0] == '.const':
                if self.constants.get(line[1],None) != None and self.verbose:
                    print(ERRORS[7].format(lineNumber,line[1]))
                    delList.append(lineNumber)
                else:
                    try:
                        is_imm = line[2].startswith('#')
                        self.constants[line[1]] = int(line[2][is_imm:])
                    except:
                        print(ERRORS[3].format(lineNumber))
            
            # Inline bytes
            elif line[0] == '.byte':
                currentProgress += 1

            # Inline halfwords
            elif line[0] == '.half':
                currentProgress += 2

            # Inline words
            elif line[0] == '.word':
                currentProgress += 4
            
            # last resort
            elif self.verbose:
                print(ERRORS[8].format(lineNumber))
                delList.append(lineNumber)
        
        for lineNumber in delList:
            del self.assembly[lineNumber]
    
    
    def labelConstConvert(self,originalValue,line,memoryLength):
        """Convert constants&labels to integers"""
        if line[originalValue] in self.constants:
            line[originalValue] = '#'+str(self.constants[line[originalValue]])
        
        elif line[originalValue] in self.labels:
            # NPC-relative labels
            if line[0] in self.jump_rel:
                instLength = self.formats[self.instructions[line[0]][0]][0]//8
                line[originalValue] = '#'+str(
                    self.labels[line[originalValue]]
                    -(memoryLength+instLength*self.jump_abs))
            # Absolute labels
            elif line[0] in self.jump_abs:
                line[originalValue] = '#'+str(self.labels[line[originalValue]])
            # PC-relative labels, as the default
            else:
                line[originalValue] = '#'+str(self.labels[line[originalValue]]
                    -memoryLength)
    
    
    def categorizeOperands(self,line):
        """Categorize operands and pass any unknown strings"""
        categorizedLine = [line[0]]
        for operand in line[1:]:
            if operand in self.conditions.keys():
                categorizedLine.append('COND')
            elif operand in self.registers.keys():
                categorizedLine.append('REG')
            elif operand[0] == '#':
                categorizedLine.append('NUM')
            else:
                categorizedLine.append('_'+operand)
        return tuple(categorizedLine)
    
    
    def assemble(self):
        machine_code = []
        for lineNumber in self.assembly.keys():
            line = self.cleanLine(self.assembly[lineNumber])
            memoryLength = len(machine_code)
            
            # Label assignment
            if line[0][-1] == ":":
                labelName = line[0][:-1]
                self.labels[labelName] = memoryLength
                continue
            
            # Convert constants&labels into integers
            for originalValue in range(1,len(line)):
                self.labelConstConvert(originalValue,line,memoryLength)
            
            # Categorize operands for easy identification
            categorizedLine = self.categorizeOperands(line)
            
            # Instruction alignment, in case the current instruction is misaligned
            if line[0] in self.instructions and self.instAlign:
                alignPower = 2**int(self.instAlign)
                padAmount = (memoryLength % alignPower)
                padAmount = -(padAmount-alignPower) if padAmount else 0
                machine_code.extend([0]*padAmount)
            
            # Align and pad by a power of two using a provided byte
            if line[0] == ".align":
                try:
                    is_imm = line[1].startswith('#')
                    alignPower = 2**int(line[1][is_imm:])
                except:
                    print(ERRORS[3].format(lineNumber))
                else:
                    padAmount = (memoryLength % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    machine_code.extend([0]*padAmount)
            
            # Constant assignment
            elif line[0] == '.const':
                try:
                    is_imm = line[2].startswith('#')
                    self.constants[line[1]] = int(line[2][is_imm:])
                except:
                    print(ERRORS[3].format(lineNumber))
            
            # Inline bytes
            elif line[0] == '.byte':
                try:
                    is_imm = line[1].startswith('#')
                    machine_code.append(self.twoComp(int(line[1][is_imm:]), 8) & 255)
                except:
                    print(ERRORS[3].format(lineNumber))
            
            # Inline halfwords
            elif line[0] == '.half':
                try:
                    is_imm = line[1].startswith('#')
                    halfword = self.twoComp(int(line[1][is_imm:]), 16)
                except:
                    print(ERRORS[3].format(lineNumber))
                else:
                    machine_code.extend([byte & 255 for byte in [
                        halfword >> (8*x) for x in range(2)
                        ][::[1,-1][self.big_endian]]])
            
            # Inline words
            elif line[0] == '.word':
                try:
                    is_imm = line[1].startswith('#')
                    word = self.twoComp(int(line[1][is_imm:]), 32)
                except:
                    print(ERRORS[3].format(lineNumber))
                else:
                    machine_code.extend([byte & 255 for byte in [
                        word >> (8*x) for x in range(4)
                        ][::[1,-1][self.big_endian]]])
            
            elif categorizedLine in self.instructions.keys():
                machine_code.extend(self.formatEncode(categorizedLine,
                    line,lineNumber))
            else:
                print('Something went wrong. :(')
        return machine_code
