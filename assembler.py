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
        self.endianess = target.ENDIANESS
        self.pad_byte = target.PAD_BYTE
        self.registers = target.REGISTERS
        self.formats = target.FORMATS
        self.instructions = target.INSTRUCTIONS
        # Import optional definitions
        if "COND" in target.ISA_FEATURES:
            self.conditions = target.CONDITIONS
            self.enable_cond = True
        
        # Initialize variables
        self.constants = {}
        self.verbose = verbose
        
    
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
            if isinstance(instField[1],int):
                selectedValue = instField[1]
            elif current_element >= max_elements:
                print(f"ERROR, line {lineNumber}: less arguments than required {current_element}, using default 0")
                selectedValue = 0
            elif instField[1].upper() == 'REG':
                if line[current_element] in self.registers:
                    selectedValue = self.registers[line[current_element]]
                    current_element += 1
                else:
                    print(f"ERROR, line {lineNumber}: register not found, using default 0")
                    selectedValue = 0
            elif instField[1].upper() == 'COND':
                if line[current_element] in self.conditions:
                    selectedValue = self.conditions[line[current_element]]
                    current_element += 1
                else:
                    print(f"ERROR, line {lineNumber}: condition not found, using default 0")
                    selectedValue = 0
            elif instField[1].upper() == 'NUM':
                if line[current_element].isdigit():
                    selectedValue = int(line[current_element])
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
            current_format[0]//8)][::[1,-1][self.endianess]]]
        
    
    def cleanLine(self,line):
        """cleans the line and prepares it for easier reading"""
        return(' '.join(
            line.replace('=', ' ').replace(',', ' ').split()).split(' '))
    
    def assemble(self):
        machine_code = []
        for lineNumber in self.assembly.keys():
            line = self.cleanLine(self.assembly[lineNumber])
            memoryLength = len(machine_code)
            
            
            # Label assignment
            if line[0][-1] == ":":
                constantName = line[0][:-1]
                if self.constants.get(constantName,None) != None and self.verbose:
                    print(f"WARNING, line {lineNumber}: constant {constantName} already exists, overwriting")
                self.constants[constantName] = memoryLength
                continue
            
            # Convert constant to integer
            for originalValue in range(1,len(line)):
                if line[originalValue] in self.constants:
                    line[originalValue] = self.constants[line[originalValue]]
            
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
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided, not padding")
                else:
                    padAmount = (memoryLength % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    machine_code.extend([0]*padAmount)
            
            # Constant assignment
            elif line[0] == '.const':
                try:
                    self.constants[line[1]] = int(line[2])
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided,ignoring")
            
            # Inline bytes
            elif line[0] == '.byte':
                try:
                    machine_code.append(self.twoComp(int(line[1]), 8) & 255)
                except:
                    print(f"ERROR, line {lineNumber}: non-integer character provided,ignoring")
            
            elif line[0] in self.instructions:
                machine_code.extend(self.formatEncode(line,lineNumber))
            
            # last resort
            elif self.verbose:
                print(f"WARNING, line {lineNumber}: unknown instruction")
        
        return machine_code
