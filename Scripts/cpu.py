import disks
import random

class x8:
    """Standard format for all bytes in this CPU"""
    def __init__(self, b1=0|1,b2=0|1,b3=0|1,b4=0|1,b5=0|1,b6=0|1,b7=0|1,b8=0|1):
        self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8= b1, b2, b3, b4, b5, b6, b7, b8
    def __str__(self):
        return str(self.b1) + str(self.b2) + str(self.b3) + str(self.b4) + str(self.b5) + str(self.b6) + str(self.b7) + str(self.b8)
    def __eq__(self, other):
        if type(other) != type(x8()):
            return False
        else:
            return str(self) == str(other)
        
def x8ToNum(CODE):
    return CODE.b1 * 2**7 + CODE.b2 * 2**6 + CODE.b3 * 2**5 + CODE.b4 * 2**4 + CODE.b5 * 2**3 + CODE.b6 * 2**2 + CODE.b7 * 2 + CODE.b8

memLen = 2**4
binMemLen = 2**8

memory = [x8(0,0,0,0,0,0,0,0) for i in range(memLen)]
disp = [(x8(0,0,0,0,0,0,0,0), x8(0,0,0,0,0,0,0,0), x8(0,0,0,0,0,0,0,0)) for _ in range(100 * 150)]
binaryMem = [0 for i in range(binMemLen)]

clock = x8(0,0,0,0,0,0,0,0)
carry = 0

rax = x8(0,0,0,0,0,0,0,0)
rdi = ""

SPECS = {
    "CPU": {
        "Name": "PyBit",
        "IntSize": "x8",
        "Hertz": "30Hz"
    },
    "GPU": {
        "Name": "PyGraphics Integrated",
        "IntSize": "x8",
        "Hertz": "30Hz"
    },
    "Instruction set": {
        "Name": "PB8 Assembly",
        "Assembler": "Interpreted"
    },
    "Disk": {
        "Name": "InfraDisk",
        "Size": "Unbound",
        "I/O Speed": "Unbound",
        "System": "RiverCape Disk Technology"
    }
}

VERSION = "halfdev 0.\u00BD.0"
"""The version"""
LICENSE = "MIT License"
"""The license"""
WELCOME_MSG = """\033[33;1;4mPyBit $cpu.intsize $cpu.hertz ($version)\033[0m
\033[1m$license\033[0m"""
"""The message to be displayed in the bios

`$version` will be replaced with the version and `$license` will be replaced with the license

Supports ASCII colour codes (`\\033[XXXm`)"""
def BIOS() -> None:
    print(WELCOME_MSG.replace("$version", VERSION).replace("$license", LICENSE).replace("$cpu.intsize", SPECS["CPU"]["IntSize"]).replace("$cpu.hertz", SPECS["CPU"]["Hertz"]))

CHARS = ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"£$%^&*()-+#~:;{}[]<>,./?\\|`¬¦\'\b\t\n\f\r '

def genHash() -> str:
    _hashChars = "01234567890123456789qwertyuiopasdfghjklzxcvbnm!\"£$%^&*()"
    _hash = ""
    for _ in range(16):
        _hash += _hashChars[random.randint(0, len(_hashChars))]
    return _hash

def badd(b1, b2, carry):
    result = 0
    ncarry = 0
    if b1 == b2:
        result = carry
        if b1 == 1:
            ncarry = 1
    else:
        result = 1 - carry
        if carry == 1:
            ncarry = 1
            
    return result, ncarry

def add(by1 : x8, by2 : x8, carry = 0):
    """Adds 2 bytes"""
    r8 = badd(by1.b8, by2.b8, carry)
    r7 = badd(by1.b7, by2.b7, r8[1])
    r6 = badd(by1.b6, by2.b6, r7[1])
    r5 = badd(by1.b5, by2.b5, r6[1])
    r4 = badd(by1.b4, by2.b4, r5[1])
    r3 = badd(by1.b3, by2.b3, r4[1])
    r2 = badd(by1.b2, by2.b2, r3[1])
    r1 = badd(by1.b1, by2.b1, r2[1])

    return x8(r1[0], r2[0], r3[0], r4[0], r5[0], r6[0], r7[0], r8[0]), r1[1]

def sub(by1 : x8, by2 : x8):

    by2Neg = x8(by2.b1, by2.b2, by2.b3, by2.b4, by2.b5, by2.b6, by2.b7, by2.b8)
    index = str(by2).find("1")
    if index == -1: return add(by1, x8())
    elif index == 0: return add(by1, by2)
    else:
        if index >= 1: by2Neg.b1 = 1 - by2Neg.b1
        if index >= 2: by2Neg.b2 = 1 - by2Neg.b2
        if index >= 3: by2Neg.b3 = 1 - by2Neg.b3
        if index >= 4: by2Neg.b4 = 1 - by2Neg.b4
        if index >= 5: by2Neg.b5 = 1 - by2Neg.b5
        if index >= 6: by2Neg.b6 = 1 - by2Neg.b6
        if index >= 7: by2Neg.b7 = 1 - by2Neg.b7
    answer = add(by1, by2Neg)
    return answer[0]

def x4to10(val):
    return {"0000" : 0,
    "0001" : 1,
    "0010" : 2,
    "0011" : 3,
    "0100" : 4,
    "0101" : 5,
    "0110" : 6,
    "0111" : 7,
    "1000" : 8,
    "1001" : 9,
    "1010" : 10,
    "1011" : 11,
    "1100" : 12,
    "1101" : 13,
    "1110" : 14,
    "1111" : 15}[val]

def mul(by1 : x8, by2 : x8):
    result = x8(0,0,0,0,0,0,0,0)
    for _ in range(x8ToNum(by2)):
        result = add(result, by1)[0]
    
    return result

def shift(byte : x8, dir : str | None = None):
    """Use LEFT or RIGHT"""
    if dir == None:
        return byte
    if dir == "LEFT":
        return mul(byte, x8(0,0,0,0,0,0,1,0))
    return x8(0, byte.b1, byte.b2, byte.b3, byte.b4, byte.b5, byte.b6, byte.b7)

def getReg(id : str):
    global rax, rdi, clock, carry, memory
    if id == "clock":
        return clock
    elif id == "carry":
        return carry
    elif id == "rax":
        return rax
    elif id == "rdi":
        return rdi
    else:
        return memory[x4to10(id)]
    
def setReg(id : str, val):
    global rax, rdi, memory, clock, carry
    if id == "rax":
        rax = val
    elif id == "rdi":
        rdi = val
    elif id == "clock":
        clock = val
    elif id == "carry":
        carry = val
    else: memory[x4to10(id)] = val

def getSection(name, code : str):
    index1, index2 = -1, -1
    index1 = code.find(name) + len(name)
    index21 = code.find("_", index1)
    index22 = code.find(".", index1)
    index2 = min(index21, index22)
    if index1 != len(name) - 1:
        if index2 != -1:
            return code[index1+1:index2]
        else:
            return code[index1+1:]
    return None

def getFunctions(code : str) -> dict[str, str]:
    index1, index2 = 0, 0
    result = {}
    while index1 != -1 and index2 != -1:
        index1 = code.find(".", index2)
        index21 = (code.find("_", index1+1))
        index22 = (code.find(".", index1+1))
        if index21 == -1: index2 = index22
        elif index22 == -1: index2 = index21
        else: index2 = min(index21, index22)
        if index2 > 0 and index1 > 0:
            func = code[index1:index2]
            funcName = func.split("\n")[0]
            funcCont = "\n".join(func.split("\n")[1:])[:-1]
            result[funcName] = funcCont
    return result

file_descriptor = ""
link = ""

#SYSCALL IDS HELP (DO NOT EDIT, THIS IS JUST FOR QOL)
{
    "00000001" : "open",
    "00000010" : "write",
    "00000011" : "read",
    "00000100" : "close",
    "00000101" : "request",
    "00000110" : "read (link)"
}

import urllib
import urllib.request
import os

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
hostPath = os.path.dirname(dir_path) + "\\hostingLocal"

def urlRead(link) -> str:
    global hostPath
    if link.split("/")[0] == "localpb:":
        with open(hostPath + "\\".join(link.split("/")[1:])[:-1]) as f:
            l = f.read()
        return l
    u2 = urllib.request.urlopen(link)
    lines = u2.readlines()
    u2.close()
    ms = ""
    for i in lines:
        a1 = "'"
        ms += f"{str(i).removeprefix('b' + a1).removesuffix(a1)}"
    return (ms.replace("\\n", "\n").replace("\\t", "\t"))

def sysCall():
    global rax, rdi, file_descriptor, link
    # file access
    if rax == x8(0,0,0,0,0,0,0,1):
        file_descriptor = rdi
    if rax == x8(0,0,0,0,0,0,1,0):
        disks.setFile(file_descriptor, rdi)
    if rax == x8(0,0,0,0,0,0,1,1):
        rdi = disks.getFile(file_descriptor)
    if rax == x8(0,0,0,0,0,1,0,0):
        file_descriptor = ""
    # web access
    if rax == x8(0,0,0,0,0,1,0,1):
        link = rdi.replace("@", ".")
    if rax == x8(0,0,0,0,0,1,1,0):
        rdi = urlRead(link)
        #u2 = urllib.request.urlopen(link)
        #lines = u2.readlines()
        #u2.close()
        #ms = ""
        #for i in lines:
        #    a1 = "'"
        #    ms += f"{str(i).removeprefix('b' + a1).removesuffix(a1)}"
        #rdi = (ms.replace("\\n", "\n").replace("\\t", "\t"))



def main() -> None:
    BIOS()

if __name__ == "__main__":
    main()