# Era

An Easily Retargetable Assembler

Designed for maximum compatability with different architectures, allowing the user to easily create a new target that works with all features of the assembler right out of the box.


# Features

* Two-pass processing
* Comments
* Constants
* Labels
* Support for binary, octal, hexadecimal, and negative decimal numbers
* Pseudo-instruction support
* TODO - String support
* TODO - Macro support

# Goals

* Keep both the assembler code and target definition simple and readable
* Allow every aspect of the assembler to be used on any target
* Any target errors should be reported in an easily debugable way

# Supported targets

* 8008 old&new mnemonics
* RISC-V 32I

# Requirements

The assembler currently requires numpy and numexpr installed, which can be done by running the following command:

`pip3 install numexpr`

# Usage

`main.py [-t TARGET] [-i INPUT] [-o OUTPUT]`
