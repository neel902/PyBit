from cpu import *
from gpu import *

def run(codeRaw : str):

    display = None

    code = codeRaw.lower()
    dataSec = getSection("_data", code)
    startSec = getSection("_start", code)
    updateSec = getSection("_tick", code)
    #DATA
    variables = {}
    if dataSec:
        data = dataSec.split("\n")
        for i in data:
            if i != "":
                line = i.split(" ")
                if line[0] == "reg":
                    variables[line[1]] = line[2]
                if line[0] == "disp":
                    display = gpu()
                if line[0] == "let":
                    variables[line[1]] = line[2]
                if line[0] == "ltr":
                    index = CHARS.index(line[2])
                    indexBin = bin(index).replace("0b", "")
                    indexBin = "0" * (8 - len(indexBin)) + indexBin
                    variables[line[1]] = indexBin
    #START
    if startSec:
        start = startSec.split("\n")
        for i in start:
            if i != "":
                line = i.split(" ")
                if line[0] == "add":
                    result = add(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
                    setReg(variables[line[3]][1:], result[0])
                    carry = result[1]
                if line[0] == "sub":
                    result = sub(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
                    setReg(variables[line[3]][1:], result)
                if line[0] == "out":
                    print(getReg(variables[line[1]][1:]))
                if line[0] == "prn":
                    letter = ""
                    CODE = getReg(variables[line[1]][1:])
                    NUM_CODE = x8ToNum(CODE)
                    if NUM_CODE <= len(CHARS):
                        letter = CHARS[NUM_CODE]
                    else:
                        letter = variables[line[1]]
                    print(letter, end="")
                if line[0] == "prl":
                    letter = ""
                    CODE = getReg(variables[line[1]][1:])
                    NUM_CODE = x8ToNum(CODE)
                    if NUM_CODE <= len(CHARS):
                        letter = CHARS[NUM_CODE]
                    else:
                        letter = variables[line[1]]
                    print(letter)
                if line[0] == "not":
                    binaryMem[int(variables[line[1]][1:])] = 1 - binaryMem[int(variables[line[2]][1:])]
                if line[0] == "bset":
                    binaryMem[int(variables[line[1]][1:])] = int(line[2])
                if line[0] == "bout":
                    print(binaryMem[int(variables[line[1]][1:])])
                if line[0] == "xor":
                    binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == binaryMem[int(variables[line[3]][1:])] else 1
                if line[0] == "or":
                    binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == 1 or binaryMem[int(variables[line[3]][1:])] == 1 else 0
                if line[0] == "and":
                    binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == 1 and binaryMem[int(variables[line[3]][1:])] == 1 else 0
                if line[0] == "nor":
                    binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == 1 or binaryMem[int(variables[line[3]][1:])] == 1 else 1
                if line[0] == "nand":
                    binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == 1 and binaryMem[int(variables[line[3]][1:])] == 1 else 1
                if line[0] == "xnor":
                    binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == binaryMem[int(variables[line[3]][1:])] else 0
                if line[0] == "set":
                    l = line[2]
                    if l in variables.keys():
                        l = variables[l]
                    setReg(variables[line[1]][1:], x8(*[int(i) for i in l]))
                if line[0] == "mov":
                    l = line[2]
                    setReg(variables[line[2]][1:], getReg(variables[line[1]][1:]))
    
    running = True
    while running:
        if updateSec:
            update = updateSec.split("\n")
            for i in update:
                if i != "":
                    line = i.split(" ")
                    if line[0] == "pxl":
                        pos = int(line[2]) + 100 + (150 * (int(line[1])-1))
                        disp[pos] = (getReg(variables[line[3]][1:]), getReg(variables[line[4]][1:]), getReg(variables[line[5]][1:]))
                    if line[0] == "add":
                        result = add(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
                        setReg(variables[line[3]][1:], result[0])
                        carry = result[1]
                    if line[0] == "sub":
                        result = sub(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
                        setReg(variables[line[3]][1:], result)
                    if line[0] == "out":
                        print(getReg(variables[line[1]][1:]))
                    if line[0] == "prn":
                        letter = ""
                        CODE = getReg(variables[line[1]][1:])
                        NUM_CODE = x8ToNum(CODE)
                        if NUM_CODE <= len(CHARS):
                            letter = CHARS[NUM_CODE]
                        else:
                            letter = variables[line[1]]
                        print(letter, end="")
                    if line[0] == "prl":
                        letter = ""
                        CODE = getReg(variables[line[1]][1:])
                        NUM_CODE = x8ToNum(CODE)
                        if NUM_CODE <= len(CHARS):
                            letter = CHARS[NUM_CODE]
                        else:
                            letter = variables[line[1]]
                        print(letter)
                    if line[0] == "not":
                        binaryMem[int(variables[line[1]][1:])] = 1 - binaryMem[int(variables[line[2]][1:])]
                    if line[0] == "bset":
                        binaryMem[int(variables[line[1]][1:])] = int(line[2])
                    if line[0] == "bout":
                        print(binaryMem[int(variables[line[1]][1:])])
                    if line[0] == "xor":
                        binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == binaryMem[int(variables[line[3]][1:])] else 1
                    if line[0] == "or":
                        binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == 1 or binaryMem[int(variables[line[3]][1:])] == 1 else 0
                    if line[0] == "and":
                        binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == 1 and binaryMem[int(variables[line[3]][1:])] == 1 else 0
                    if line[0] == "nor":
                        binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == 1 or binaryMem[int(variables[line[3]][1:])] == 1 else 1
                    if line[0] == "nand":
                        binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == 1 and binaryMem[int(variables[line[3]][1:])] == 1 else 1
                    if line[0] == "xnor":
                        binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == binaryMem[int(variables[line[3]][1:])] else 0
                    if line[0] == "set":
                        l = line[2]
                        if l in variables.keys():
                            l = variables[l]
                        setReg(variables[line[1]][1:], x8(*[int(i) for i in l]))
                    if line[0] == "mov":
                        l = line[2]
                        setReg(variables[line[2]][1:], getReg(variables[line[1]][1:]))
                display.tick(disp)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

if __name__ == "__main__":
    run(
    """
_data
REG out $0000
REG red $0001
DISP
_tick
SET out 11111111
SET red 00000000
PXL 1 1 out red red""")