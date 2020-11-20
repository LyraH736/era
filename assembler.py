import re

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
        self.conditions = ()
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
    
    def formatEncode(self,line,lineNumber):
        """Encodes the instruction into the format provided by the target"""
        current_instruction = self.instructions[line[0]]
        current_format = self.formats[current_instruction[0]]
        current_element = 1
        max_elements = len(line)
        
        instruction_fields = {}
        
        for instField in current_instruction[1:]:
            if isinstance(instField[1],str): inputType = instField[1].upper()
            else: inputType = instField[1]
            
            if isinstance(inputType,int):
                selectedValue = inputType
            elif current_element >= max_elements:
                print(line)
                print(f"ERROR, line {lineNumber}: less arguments than required {current_element}, using default 0")
                selectedValue = 0
            elif inputType.startswith('REG'):
                if line[current_element] in self.registers:
                    selectedValue = self.registers[line[current_element]]
                    current_element += 1
                else:
                    print(f"ERROR, line {lineNumber}: register not found, using default 0")
                    selectedValue = 0
            elif inputType.startswith('COND'):
                if line[current_element] in self.conditions:
                    selectedValue = self.conditions[line[current_element]]
                    current_element += 1
                else:
                    print(f"ERROR, line {lineNumber}: condition not found, using default 0")
                    selectedValue = 0
            elif inputType.startswith('NUM'):
                if line[current_element].isdigit():
                    selectedValue = int(line[current_element])
                    # Shift the inputs if needed
                    if inputType.endswith('r'):
                        selectedValue = selectedValue >> instField[2]
                    else:
                        selectedValue = selectedValue << self.listGet(instField,2)
                    current_element += 1
                else:
                    print(f"ERROR, line {lineNumber}: non-numeric characters detected, using default 0")
                    selectedValue = 0
            else:
                print(f"ERROR, line {lineNumber}: invalid target value type, using default 0")
                selectedValue = 0
            instruction_fields[instField[0]] = selectedValue
        
        format_fields = []
        
        for formatField in current_format[1:]:
            try:
                format_fields.append(
                    [instruction_fields[formatField[0]],formatField[1]])
            except:
                print(f"FATAL ERROR, line {lineNumber}: invalid target formatting")
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
        """First pass, finds labels, converts numbers"""
        currentProgress = 0
        nums = {'0x':16,'0o':8,'0b':2}
        for lineNumber in self.assembly.keys():
            line = self.cleanLine(self.assembly[lineNumber])
            
            for num in range(0,len(line)):
                # Convert hex/octal/binary numbers
                if any(hob in line[num] for hob in nums):
                    self.assembly[lineNumber] = self.assembly[lineNumber].replace(
                        line[num],str(int(
                        line[num][2:],nums[line[num][0:2]])))
            
            # Instruction alignment, in case the current instruction is misaligned
            if line[0] in self.instructions and self.instAlign:
                alignPower = 2**int(self.instAlign)
                padAmount = (currentProgress % alignPower)
                padAmount = -(padAmount-alignPower) if padAmount else 0
                currentProgress += padAmount
            
            # Label assignment
            if line[0][-1] == ":":
                labelName = line[0][:-1]
                if self.labels.get(labelName,None) != None and self.verbose:
                    print(f"WARNING, line {lineNumber}: label {labelName} already exists, overwriting")
                self.labels[labelName] = currentProgress
                continue
            
            elif line[0] in self.instructions:
                instLength = self.formats[self.instructions[line[0]][0]][0]//8
                currentProgress += instLength
            
            # Align and pad by a power of two using a provided byte
            elif line[0] == ".align":
                try:
                    alignPower = 2**int(line[1])
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided, not padding")
                else:
                    padAmount = (currentProgress % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    currentProgress += padAmount
            
            # Constant assignment
            elif line[0] == '.const':
                if self.constants.get(line[1],None) != None and self.verbose:
                    print(f"WARNING, line {lineNumber}: constant {line[1]} already exists, overwriting")
                try:
                    self.constants[line[1]] = int(line[2])
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided,ignoring")
            
            # Inline bytes
            elif line[0] == '.byte':
                try:
                    currentProgress += 1
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided,ignoring")

            # Inline halfwords
            elif line[0] == '.half':
                try:
                    currentProgress += 2
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided,ignoring")

            # Inline words
            elif line[0] == '.word':
                try:
                    currentProgress += 4
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided,ignoring")
            
            # last resort
            elif self.verbose:
                print(f"WARNING, line {lineNumber}: unknown instruction")
    
    
    def labelConstConvert(self,originalValue,line,memoryLength):
        "Convert constants&labels to integers"
        if line[originalValue] in self.constants:
            line[originalValue] = self.constants[line[originalValue]]
        
        elif line[originalValue] in self.labels:
            # NPC-relative labels
            if line[0] in self.jump_rel:
                instLength = self.formats[self.instructions[line[0]][0]][0]//8
                line[originalValue] = (
                    self.labels[line[originalValue]]
                    -(memoryLength+instLength*self.jump_abs))
            # Absolute labels
            elif line[0] in self.jump_abs:
                line[originalValue] = self.labels[line[originalValue]]
            # PC-relative labels, as the default
            else:
                line[originalValue] = (self.labels[line[originalValue]]
                    -memoryLength)
    
    
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
            
            # Instruction alignment, in case the current instruction is misaligned
            if line[0] in self.instructions and self.instAlign:
                alignPower = 2**int(self.instAlign)
                padAmount = (memoryLength % alignPower)
                padAmount = -(padAmount-alignPower) if padAmount else 0
                machine_code.extend([0]*padAmount)
            
            # Align and pad by a power of two using a provided byte
            if line[0] == ".align":
                try:
                    alignPower = 2**int(line[1])
                except: pass
                else:
                    padAmount = (memoryLength % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    machine_code.extend([0]*padAmount)
            
            # Constant assignment
            elif line[0] == '.const':
                try:
                    self.constants[line[1]] = int(line[2])
                except: pass
            
            # Inline bytes
            elif line[0] == '.byte':
                try:
                    machine_code.append(self.twoComp(int(line[1]), 8) & 255)
                except: pass
            
            # Inline halfwords
            elif line[0] == '.half':
                try:
                    halfword = self.twoComp(int(line[1]), 16)
                except: pass
                else:
                    machine_code.extend([byte & 255 for byte in [
                        halfword >> (8*x) for x in range(2)
                        ][::[1,-1][self.big_endian]]])
            
            # Inline words
            elif line[0] == '.word':
                try:
                    word = self.twoComp(int(line[1]), 32)
                except: pass
                else:
                    machine_code.extend([byte & 255 for byte in [
                        word >> (8*x) for x in range(4)
                        ][::[1,-1][self.big_endian]]])
            
            elif line[0] in self.instructions:
                machine_code.extend(self.formatEncode(line,lineNumber))
        
        return machine_code
