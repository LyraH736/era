import argparse
import sys
import assembler


def main():
    """Initial setup operation function"""
    parser = argparse.ArgumentParser(
        description='Era - an Easy Retargetable Assembler')
    parser.add_argument('-t','--target',help='target')
    parser.add_argument('-i','--input',help='input file')
    parser.add_argument('-o','--output',help='output file')
    parser.add_argument('-v','--verbose',help='Verbose output',
        action='store_true')
    args = parser.parse_args()
    
    # Set targets path and import set target or default(MIPS I)
    sys.path.append('./targets')
    
    if args.target:
        target = __import__(args.target)
    else:
        target = __import__('target0')
    
    # Import assembly file
    with open(args.input,'r') as asmfile:
        asmLines = asmfile.readlines()
    
    # Initialize 
    asm_object = assembler.Assembler(asmLines,target,args.verbose)
    
    # Assemble and convert to a binary object
    memoryArray = bytes(asm_object.assemble())
        
    # Assembled file writer
    outname = args.output if args.output else 'a.out'
    with open(outname,'wb') as outfile:
        outfile.write(memoryArray)


if __name__ == '__main__':
    main()
