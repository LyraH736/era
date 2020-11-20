# Era

An Easily Retargetable Assembler

Designed for maximum compatability with different architectures, allowing the user to easily create a new target that works with all features of the assembler right out of the box.


# Features

* Two-pass processing
* Comments
* Constants
* Labels
* Support for binary, octal, hexadecimal, and negative decimal numbers
* TODO - String support
* TODO - Error reporting
* TODO - Misspelling suggestions
* TODO - Pseudo-instruction support
* TODO - Macro support

# Goals

* Keep both the assembler code and target definition simple and readable
* Allow every aspect of the assembler to be used on any target
* Any target errors should be reported in an easily debugable way

# Limitations

Currently the assembler doesn't allow for multiple instructions with the same name(i.e different addressing modes/widths), thus requiring renaming instructions to maintain compatability.
