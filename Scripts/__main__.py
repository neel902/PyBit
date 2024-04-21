from cpu import *
from gpu import *
from disks import *
import keyboard
import time
import sys

variables = {}
functions = {}

def call(name):
    global functions, variables
    for i in functions[f".{name}"].split("\n"):
        
        if i != "":
            line = i.split(" ")
            sec(line)

import keyboard

lastKey = "space"

def on_key_event(event):
    global lastKey
    lastKey = event.name

def currentKey():
    global lastKey
    try:
        if keyboard.is_pressed(lastKey):
            indexBin = bin(CHARS.find(lastKey)).replace("0b", "")
            indexBin = "0" * (8 - len(indexBin)) + indexBin
            return x8(int(indexBin[-8]),int(indexBin[-7]),int(indexBin[-6]),int(indexBin[-5]),int(indexBin[-4]),int(indexBin[-3]),int(indexBin[-2]),int(indexBin[-1]))
        else:
            return x8()
    except:
        return x8()

keyboard.on_press(on_key_event)

def sec(line):
    global variables, functions, clock
    if line[0] == "var":
        variables[line[1]] == line[2]
    if line[0] == "inp":
        binaryMem[variables[line[1]]] == input("1|0")
    if line[0] == "key":
        setReg(variables[line[1]][1:], currentKey())
    if line[0] == "call":
        call(line[1])
    if line[0] == "if":
        if binaryMem[int(variables[line[1]][1:])] == 1:
            call(line[2])
        elif line[3] == "else":
            call(line[4])
    if line[0] == "if>":
        if x8ToNum(getReg((variables[line[1]][1:]))) > x8ToNum(getReg((variables[line[2]][1:]))):
            call(line[3])
    if line[0] == "if<":
        if x8ToNum(getReg((variables[line[1]][1:]))) < x8ToNum(getReg((variables[line[2]][1:]))):
            call(line[3])
    if line[0] == "if=":
        if x8ToNum(getReg((variables[line[1]][1:]))) == x8ToNum(getReg((variables[line[2]][1:]))):
            call(line[3])
    if line[0] == "exit":
        sys.exit()
    if line[0] == "add":
        result = add(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
        setReg(variables[line[3]][1:], result[0])
        setReg("carry", result[1])
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
    if line[0] == "sset":
        l = " ".join(line[2:])
        if l in variables.keys():
            l = variables[l]
        
        setReg(variables[line[1]][1:], l)
    if line[0] == "mov":
        l = line[2]
        setReg(variables[line[2]][1:], getReg(variables[line[1]][1:]))

    if line[0] == "syscall":
        sysCall()
    if line[0] == "pxl":
        pos = int(line[2]) + 100 + (150 * (int(line[1])-1))
        disp[pos] = (getReg(variables[line[3]][1:]), getReg(variables[line[4]][1:]), getReg(variables[line[5]][1:]))

def run(codeRaw : str):
    global variables, functions, clock
    display = None

    code = codeRaw.lower()
    dataSec = getSection("_data", code)
    startSec = getSection("_start", code)
    updateSec = getSection("_tick", code)
    functions = getFunctions(code)
    #DATA
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
                    variables[line[1]] = line[2:]
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
                sec(line)
    
    if updateSec:
        running = True
        while running:
            update = updateSec.split("\n")
            for i in update:
                if i != "":
                    line = i.split(" ")
                    
                    sec(line)
                    setReg("clock", add(getReg("clock"), x8(0,0,0,0,0,0,0,1))[0])
                    if line[0] == "break":
                        running = False
                if display: display.tick(disp)
            if display:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
    else:
        pygame.quit()

if __name__ == "__main__":
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    with open(dir_path + "\\ROM.pb8") as f:
        run(f"\n{f.read()}\n")