import re
import numexpr

ERRORS = {
    0:  "ERROR, line {}: less arguments than required {}, using default 0",
    1:  "ERROR, line {}: register not found, using default 0",
    2:  "ERROR, line {}: condition not found, using default 0",
    3:  "ERROR, line {}: non-digit characters detected, using default 0",
    4:  "ERROR, line {}: invalid target value type, using default 0",
    5:  "FATAL ERROR, line {}: invalid target formatting",
    6:  "WARNING, line {}: label {} already exists, ignoring",
    7:  "WARNING, line {}: constant {} already exists, ignoring",
    }

ERROR_FATAL = {
    0:  "FATAL ERROR, line{}: Invalid characters in constant/label name(allowed: a-z, 0-9, _)",
    1:  "FATAL ERROR: Cannot find links, I give up.",
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
        self.formats = target.FORMATS
        self.instructions = target.INSTRUCTIONS
        # Default variables
        self.big_endian = False
        self.forbid = ()
        self.registers = {}
        self.conditions = {}
        self.jump_rel = ()
        self.jump_abs = ()
        self.jump_npc = False
        # Import optional overrides
        if "BIG" in target.ISA_FEATURES:
            self.big_endian = 1
        if "FORBID" in target.ISA_FEATURES:
            self.forbid = target.FORBID
        if "REGS" in target.ISA_FEATURES:
            self.registers = target.REGISTERS
        if "COND" in target.ISA_FEATURES:
            self.conditions = target.CONDITIONS
        if "JUMP_NPC" in target.ISA_FEATURES:
            self.jump_npc = True
            
        
        # Initialize variables
        self.links = []
        self.constants = {}
        self.labels = {}
        self.markedLines = {}
        self.linePos = {}
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
            # Remove comments and newlines
            uncommented = re.sub('//.*','',line).strip('\n')
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
                if re.search('[\-]*\d+',line[current_element]):
                    selectedValue = int(line[current_element])
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
        return re.findall(
            '(?<![\w~%^&*()\-+<>/_!])[!]*<link_[a-z]{1}[\w_]*/>[:]*(?![\w~%^&*()\-+<>/_!])|(?<![<])[.]*[\d]*[-]*[\w]{1}[^,\s]*|(?<=[\s,])[!]*[\w()<]{1}[\w~%^&*()\-+<>/]*(?![\w])',
            line)
    
    
    def linkIdentityPass(self):
        """
        Link Identity pass, finds labels and constants,
        assigns them to temporary links which are easier to identify
        """
        for lineNumber in self.assembly.keys():
            line = re.findall('[a-z]{1}[\w_:]*',self.assembly[lineNumber])
            
            # Label assignment
            if line[0][-1] == ":":
                if re.search('[^\w_]',line[0][:-1]):
                    print(ERROR_FATAL[0].format(lineNumber))
                else:
                    linkName = '<link_'+line[0][:-1]+'/>'
                    self.links.append(linkName)
                    self.assembly[lineNumber] = linkName+':'
            
            # All other cases
            for word in line[1:]:
                forbidden = (word in self.conditions.keys()
                    or word in self.registers.keys()
                    or word in self.forbid)
                if forbidden:
                    continue
                linkName = '<link_'+word+'/>'
                self.links.append(linkName)
                self.assembly[lineNumber] = re.sub(
                    '(?<![\w_])%s(?![\w_])' % word, linkName,
                    self.assembly[lineNumber])
    
    
    def secondPass(self):
        """
        Second pass, finds labels, converts numbers, turns links into numbers,
        marks empty links, cleans code further
        """
        pass_tainted = False
        currentProgress = 0
        delList = []
        nums = {'0x':16,'0o':8,'0b':2}
        # Find labels, constant assignments, use temporary values if unavailable
        for lineNumber in self.assembly.keys():
            markLine = False
            # Find hex/octal/binary numbers and convert them to decimal
            # A non-math-hostile version that allows everything to be converted
            # without spaces inbetweem every number
            numberSet = set(re.findall(
                '(?<![\w_])(0x[0-9a-f]+|0o[0-7]+|0b[0-1]+)(?![\w_])',
                self.assembly[lineNumber]))
            for number in numberSet:
                self.assembly[lineNumber] = re.sub('(?<![\w_])%s(?![\w_])' % number,
                    str(int(number[2:],nums[number[:2]])),
                    self.assembly[lineNumber])
            
            line = self.cleanLine(self.assembly[lineNumber])
            
            # Save position before any changes
            self.linePos[lineNumber] = currentProgress
            
            # Label assignment
            if line[0][-1] == ":":
                labelName = line[0][:-1]
                if self.labels.get(labelName,None) != None:
                    delList.append(lineNumber)
                    print(ERRORS[6].format(lineNumber,labelName))
                elif pass_tainted:
                    markLine = True
                else:
                    self.labels[labelName] = currentProgress
                    delList.append(lineNumber)
            
            # Constant assignment
            elif line[0] == '.const':
                if self.constants.get(line[1],None) != None:
                    delList.append(lineNumber)
                    print(ERRORS[7].format(lineNumber,line[1]))
                elif re.search('[\-]*\d+',line[2]):
                    self.constants[line[1]] = numexpr.evaluate(line[2]).item()
                    delList.append(lineNumber)
                else:
                    markLine = True
            
            # Replace constants, absolute labels, and mark empty links
            linkList = set(re.findall('[!]*<link_[a-z]{1}[\w_]*/>',self.assembly[lineNumber]))
            for linkName in linkList:
                absoluteLabel = linkName.startswith('!')
                if linkName in self.constants:
                    self.assembly[lineNumber] = re.sub(
                        '(?<![\w_])%s(?![\w_])' % linkName, str(self.constants[linkName]),
                        self.assembly[lineNumber])
                elif linkName[absoluteLabel:] in self.labels:
                    # Absolute labels, always assignable
                    if absoluteLabel:
                        self.assembly[lineNumber] = re.sub(
                            '(?<![\w_])%s(?![\w_])' % linkName,
                            str(self.labels[linkName[1:]]),
                            self.assembly[lineNumber])
                else:
                    markLine = True
            
            
            # Align and pad by a power of two using a provided byte
            if line[0] == ".align":
                if line[1].isdigit():
                    alignPower = 2**int(line[1])
                    padAmount = (currentProgress % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    currentProgress += padAmount
                else:
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
            
            newLine = [line[0]]
            
            # Find links and replace them with zero
            for operand in line[1:]:
                if re.search('[<>/~%^&*()-+]',operand):
                    newLine.append(str(numexpr.evaluate(re.sub('[!]*<link_[a-z]{1}[\w_]*/>','0',operand)).item()))
                else:
                    newLine.append(operand)
                            
            
            # Categorize operands for easy identification
            categorizedLine = self.categorizeOperands(newLine)
            
            # Find untainted Links and replace them
            linkList = set(re.findall('[!]*<link_[a-z]{1}[\w_]*/>',self.assembly[lineNumber]))
            for linkName in linkList:
                absoluteLabel = linkName.startswith('!')
                if linkName[absoluteLabel:] in self.labels:
                    # Can't assign relative labels if pass tainted
                    if pass_tainted:
                        markLine = True
                    # N/PC-relative labels
                    else:
                        # Check whether it's an instruction we're making a
                        # relative label for and if architecture uses NPC
                        instruction = self.instructions.get(
                            categorizedLine, None)
                        instLength = 0
                        # It is an instruction and NPC, calculate length
                        if instruction and self.jump_npc:
                            instLength = self.formats[instruction[0]][0]//8
                        self.assembly[lineNumber] = re.sub(
                            '(?<![\w_])%s(?![\w_])' % linkName,
                            str(self.labels[linkName]
                            -(currentProgress+instLength)),
                            self.assembly[lineNumber])
            
            line = self.cleanLine(self.assembly[lineNumber])
            
            # Find unmarked operands and attempt to evaluate them
            if not markLine and lineNumber not in delList:
                for operand in line[1:]:
                    if re.search('[<>/~%^&*()-+]',operand):
                        self.assembly[lineNumber] = re.sub(
                            '(?<![\w<>?/~!%%^&*()\-+])%s(?![\w<>?/~!%%^&*()\-+])' % re.escape(operand),
                            str(numexpr.evaluate(operand).item()),self.assembly[lineNumber])
            
            # Instruction alignment, in case the current instruction is misaligned
            if categorizedLine in self.instructions.keys():
                if self.instAlign:
                    alignPower = 2**int(self.instAlign)
                    padAmount = (currentProgress % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    currentProgress += padAmount
                currentProgress += self.formats[self.instructions[
                    categorizedLine][0]][0]//8
            
            # Store line for third+ pass(es)
            if markLine:
                pass_tainted = True
                self.markedLines[lineNumber] = self.assembly[lineNumber]
        
        for lineNumber in delList:
            del self.assembly[lineNumber]
    
    
    def linkPasses(self):
        """
        Link passes, tries to find empty links and assign them
        """
        asmDelList = []
        while self.markedLines:
            pass_tainted = False
            watchdog_markedLength = len(self.markedLines)
            delList = []
            for lineNumber in self.markedLines.keys():
                currentProgress = self.linePos[lineNumber]
                line = self.cleanLine(self.assembly[lineNumber])
                markLine = 0
                
                # Label assignment
                if line[0][-1] == ":":
                    labelName = line[0][:-1]
                    if self.labels.get(labelName,None) != None:
                        print(ERRORS[6].format(lineNumber,labelName))
                    else:
                        self.labels[labelName] = currentProgress
                    asmDelList.append(lineNumber)
                
                # Constant assignment
                elif line[0] == '.const':
                    if self.constants.get(line[1],None) != None:
                        print(ERRORS[7].format(lineNumber,line[1]))
                    elif re.search('[\-]*\d+',line[2]):
                        self.constants[line[1]] = numexpr.evaluate(line[2]).item()
                    else:
                        markLine = True
                    asmDelList.append(lineNumber)
                
                # Replace constants, absolute labels, and mark empty links
                linkList = set(re.findall('[!]*<link_[a-z]{1}[\w_]*/>',self.assembly[lineNumber]))
                for linkName in linkList:
                    absoluteLabel = linkName.startswith('!')
                    if linkName in self.constants:
                        self.assembly[lineNumber] = re.sub(
                            '(?<![\w_])%s(?![\w_])' % linkName, str(self.constants[linkName]),
                            self.assembly[lineNumber])
                    elif linkName[absoluteLabel:] in self.labels:
                        # Absolute labels, always assignable
                        if absoluteLabel:
                            self.assembly[lineNumber] = re.sub(
                                '(?<![\w_])%s(?![\w_])' % linkName,
                                str(self.labels[linkName[1:]]),
                                self.assembly[lineNumber])
                    else:
                        markLine = True
                
                newLine = [line[0]]
                
                # Find links and replace them with zero
                for operand in line[1:]:
                    newLine.append(str(numexpr.evaluate(re.sub('[!]*<link_[a-z]{1}[\w_]*/>','0',operand)).item()))
                
                # Categorize operands for easy identification
                categorizedLine = self.categorizeOperands(newLine)
                
                # Find untainted Links and replace them
                linkList = set(re.findall('[!]*<link_[a-z]{1}[\w_]*/>',self.assembly[lineNumber]))
                for linkName in linkList:
                    absoluteLabel = linkName.startswith('!')
                    if linkName[absoluteLabel:] in self.labels:
                        # N/PC-relative labels
                        # Check whether it's an instruction we're making a
                        # relative label for and if architecture uses NPC
                        instruction = self.instructions.get(
                            categorizedLine, None)
                        instLength = 0
                        # It is an instruction and NPC, calculate length
                        if instruction and self.jump_npc:
                            instLength = self.formats[instruction[0]][0]//8
                        self.assembly[lineNumber] = re.sub(
                            '(?<![\w_])%s(?![\w_])' % linkName,
                            str(self.labels[linkName]
                            -(currentProgress+instLength)),
                            self.assembly[lineNumber])
                
                line = self.cleanLine(self.assembly[lineNumber])
                
                # Find unmarked operands and attempt to evaluate them
                if not markLine and lineNumber not in delList:
                    for operand in line[1:]:
                        if re.search('[<>/~%^&*()-+]',operand):
                            self.assembly[lineNumber] = re.sub(
                                '(?<![\w<>?/~!%%^&*()\-+])%s(?![\w<>?/~!%%^&*()\-+])' % re.escape(operand),
                                str(numexpr.evaluate(operand).item()),self.assembly[lineNumber])
                
                # Store line for further pass(es)
                if markLine:
                    pass_tainted = True
                    self.markedLines[lineNumber] = self.assembly[lineNumber]
                else:
                    delList.append(lineNumber)
            
            for lineNumber in set(delList):
                del self.markedLines[lineNumber]
            
            if watchdog_markedLength == len(self.markedLines):
                print(ERROR_FATAL[1])
                for lineNumber in self.markedLines.keys():
                    print(self.markedLines[lineNumber])
                print(self.labels)
                quit(101)
        
        for lineNumber in set(asmDelList):
            del self.assembly[lineNumber]
    
    
    def categorizeOperands(self,line):
        """Categorize operands and pass any unknown strings"""
        categorizedLine = [line[0]]
        for operand in line[1:]:
            if operand in self.conditions.keys():
                categorizedLine.append('COND')
            elif operand in self.registers.keys():
                categorizedLine.append('REG')
            elif re.search('<link_[a-z]{1}[\w_]*/>|[\-]*\d+',operand):
                categorizedLine.append('NUM')
            else:
                categorizedLine.append('_'+operand)
        return tuple(categorizedLine)
    
    
    def assemble(self):
        machine_code = []
        for lineNumber in self.assembly.keys():
            line = self.cleanLine(self.assembly[lineNumber])
            memoryLength = len(machine_code)
            
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
                    alignPower = 2**int(line[1])
                except:
                    print(ERRORS[3].format(lineNumber))
                else:
                    padAmount = (memoryLength % alignPower)
                    padAmount = -(padAmount-alignPower) if padAmount else 0
                    machine_code.extend([0]*padAmount)
            
            # Inline bytes
            elif line[0] == '.byte':
                try:
                    machine_code.append(self.twoComp(int(line[1]), 8) & 255)
                except:
                    print(ERRORS[3].format(lineNumber))
            
            # Inline halfwords
            elif line[0] == '.2byte':
                try:
                    halfword = self.twoComp(int(line[1]), 16)
                except:
                    print(ERRORS[3].format(lineNumber))
                else:
                    machine_code.extend([byte & 255 for byte in [
                        halfword >> (8*x) for x in range(2)
                        ][::[1,-1][self.big_endian]]])
            
            # Inline words
            elif line[0] == '.4byte':
                try:
                    word = self.twoComp(int(line[1]), 32)
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
                print(line,categorizedLine,self.assembly[lineNumber])
                print('Something went wrong. :(')
        return machine_code
