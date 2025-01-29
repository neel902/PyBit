# PyBit x8 30Hz CPU

The PyBit is a virtual machine (VM) written entirely in Python. It features its own instruction set, known as **PB8 ASM**, which allows users to program the VM effectively. 

**THIS IS FOR WINDOWS; IT HAS NOT BEEN TESTED ON OTHER HOST OSs.**

<details>
<summary>Requirements</summary>

- tkinter
- keyboard
- time
- sys
- python 3.x
- win32clipboard
- functools
- pygame
- pathlib

</details>

## Overview of the PyBit Virtual Machine

The PyBit VM is designed to execute a custom assembly language, enabling users to write low-level programs that interact with the virtual hardware. The VM simulates a CPU with a set of registers and memory, allowing for operations such as arithmetic, logic, and control flow.

## PB8 ASM Instruction Set

The PB8 ASM instruction set includes various commands that can be used to manipulate data, control program flow, and interact with the virtual environment.

## Usage

To get started with the PyBit VM, follow these steps:

1. Clone the repository and install the required dependencies.
2. Edit the `ROM.pb8` file in the `scripts` directory to program the VM.
3. Optionally, set `run_py_bit.pb8.bat` as your default for `.pb8` files (not recommended).

For more details, visit the [wiki](https://github.com/neel902/PyBit/wiki).

