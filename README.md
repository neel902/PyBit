# PyBit x8 CPU

The PyBit is a VM written in completely python. It has its own instruction set, **PB8**, with all the necessary commands.

## Usage

First, install this repo. Then, you can edit the ROM.pb8 in scripts to program the VM

## Commands

### DATA SECTION
_data

**REG** {name} {address} *- Intitialise a register for use, with a name*

**DISP** *- Intitialise the GPU*

**LET** {name} {value} *- Create a variable*

**LTR** {name} {lowercase letter} *- Access the binary code of a lowercase letter or other supported character*

### START SECTION
_start

**ADD** {r1} {r2} {out}

**SUB** {r1} {r2} {out}

**OUT/BOUT/PRN/PRL** {reg(char_code)(str)}

**NOT, AND, OR, XOR, NOR, NAND, XNOR** {out} {reg1} (reg2[optional])

**SET/BSET/SSET** {reg} {value|bit|string}

**MOV** {reg} {out}

**SYSCALL** *-Used registries rax, rdi*

### UPDATE SECTION
_tick

**PXL** {x} {y} {ColR:reg} {ColG:reg} {ColB:reg}

***+START SECTION***

More details on [the wiki](https://github.com/neel902/PyBit/wiki)