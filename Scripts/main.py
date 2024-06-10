from cpu import *
from gpu import *
from disks import *
import keyboard
import time
import sys
import Font

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
    global variables, functions, clock, display
    try:
        match line[0]:
            case "run":
                _hash = genHash()
                functions[f".{_hash}"] = getReg("rdi")
                call(_hash)
                functions[f".{_hash}"] = "data destroyed"
            case "var":
                variables[line[1]] == line[2]
            case "inp":
                binaryMem[int(variables[line[1]][1:])] = input("1|0")
            case "md": 
                binaryMem[int(variables[line[1]][1:])] = 1 if pygame.mouse.get_pressed()[0] else 0
            case "mpx":
                x = int(pygame.mouse.get_pos()[0]/2)
                xBin = bin(x).replace("0b", "")
                xBin = "0" * (8 - len(xBin)) + xBin
                setReg(variables[line[1]][1:], x8(*[int(i) for i in xBin]))
            case "mpy":
                y = int(pygame.mouse.get_pos()[1]/2)
                yBin = bin(y).replace("0b", "")
                yBin = "0" * (8 - len(yBin)) + yBin
                setReg(variables[line[1]][1:], x8(*[int(i) for i in yBin]))
            case "key":
                setReg(variables[line[1]][1:], currentKey())
            case "call":
                call(line[1])
            case "if":
                if binaryMem[int(variables[line[1]][1:])] == 1:
                    call(line[2])
                elif line[3] == "else":
                    call(line[4])
            case "if>":
                if x8ToNum(getReg((variables[line[1]][1:]))) > x8ToNum(getReg((variables[line[2]][1:]))):
                    call(line[3])
            case "if<":
                if x8ToNum(getReg((variables[line[1]][1:]))) < x8ToNum(getReg((variables[line[2]][1:]))):
                    call(line[3])
            case "ife":
                if x8ToNum(getReg((variables[line[1]][1:]))) % 2 == 0:
                    call(line[2])
            case "ifo":
                if x8ToNum(getReg((variables[line[1]][1:]))) % 2 == 1:
                    call(line[2])
            case "if=":
                if x8ToNum(getReg((variables[line[1]][1:]))) == int(str(getReg((variables[line[2]][1:]))), 2):
                    call(line[3])
            case "exit":
                sys.exit()
            case "add":
                result = add(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
                setReg(variables[line[3]][1:], result[0])
                setReg("carry", result[1])
            case "mul":
                result = mul(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
                setReg(variables[line[3]][1:], result[0])
                setReg("carry", result[1])
            case "shl":
                """Shift left"""
                setReg(variables[line[2]][1:], shift(getReg(variables[line[1]][1:]), "LEFT"))
            case "shr":
                """Shift right"""
                setReg(variables[line[2]][1:], shift(getReg(variables[line[1]][1:]), "RIGHT"))
            case "sub":
                result = sub(getReg(variables[line[1]][1:]), getReg(variables[line[2]][1:]))
                if type(result) ==  type((1, 1)):
                    result = result[0]
                setReg(variables[line[3]][1:], result)
            case "out":
                print(getReg(variables[line[1]][1:]))
            case "prn":
                letter = ""
                CODE = getReg(variables[line[1]][1:])
                NUM_CODE = x8ToNum(CODE)
                if NUM_CODE <= len(CHARS):
                    letter = CHARS[NUM_CODE]
                else:
                    letter = variables[line[1]]
                print(letter, end="")
            case "prl":
                letter = ""
                CODE = getReg(variables[line[1]][1:])
                NUM_CODE = x8ToNum(CODE)
                if NUM_CODE <= len(CHARS):
                    letter = CHARS[NUM_CODE]
                else:
                    letter = variables[line[1]]
                print(letter)
            case "not":
                binaryMem[int(variables[line[1]][1:])] = 1 - binaryMem[int(variables[line[2]][1:])]
            case "bset":
                binaryMem[int(variables[line[1]][1:])] = int(line[2])
            case "bout":
                print(binaryMem[int(variables[line[1]][1:])])
            case "xor":
                binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == binaryMem[int(variables[line[3]][1:])] else 1
            case "or":
                binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == 1 or binaryMem[int(variables[line[3]][1:])] == 1 else 0
            case "and":
                binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == 1 and binaryMem[int(variables[line[3]][1:])] == 1 else 0
            case "nor":
                binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == 1 or binaryMem[int(variables[line[3]][1:])] == 1 else 1
            case "nand":
                binaryMem[int(variables[line[1]][1:])] = 0 if binaryMem[int(variables[line[2]][1:])] == 1 and binaryMem[int(variables[line[3]][1:])] == 1 else 1
            case "xnor":
                binaryMem[int(variables[line[1]][1:])] = 1 if binaryMem[int(variables[line[2]][1:])] == binaryMem[int(variables[line[3]][1:])] else 0
            case "set":
                l = line[2]
                if l in variables.keys():
                    l = variables[l]
                setReg(variables[line[1]][1:], x8(*[int(i) for i in l]))
            case "char":
                index = getReg(variables[line[2]][1:])
                string = getReg(variables[line[1]][1:])
                setReg(variables[line[3]][1:], string[index])
            case "sset":
                l = " ".join(line[2:])
                if l in variables.keys():
                    l = variables[l]
                
                setReg(variables[line[1]][1:].strip(), l)
            case "mov":
                l = line[2]
                setReg(variables[line[2]][1:], getReg(variables[line[1]][1:]))

            case "syscall":
                sysCall()
            case "pxl":
                sx = line[1]
                sy = line[2]
                if sx in variables:
                    sx = x8ToNum(getReg(variables[sx][1:]))
                if sy in variables:
                    sy = x8ToNum(getReg(variables[sy][1:]))
                pos = int(sx) + (150 * (int(sy))) - 1
                disp[pos] = (getReg(variables[line[3]][1:]), getReg(variables[line[4]][1:]), getReg(variables[line[5]][1:]))
            case "ftxt":
                sx = line[1]
                sy = line[2]
                if sx in variables:
                    sx = x8ToNum(getReg(variables[sx][1:]))
                if sy in variables:
                    sy = x8ToNum(getReg(variables[sy][1:]))
                col = getReg(variables[line[4]][1:]) if len(line) > 4 else x8()
                origin = int(sx) + (150 * (int(sy))) - 1
                sent = getReg(variables[line[3]][1:])
                FontLookupTable = Font.LookUp
                for charC in sent:
                    char = charC.lower()
                    FontImage = FontLookupTable[char] if char in FontLookupTable else FontLookupTable["UNKNOWN"]
                    pos = 0
                    offset = 0
                    for x in range(6):
                        for y in range(6):
                            Col1 = col if FontImage[pos] == 1 else x8(0,0,0,0,0,0,0,0)
                            Col2 = Col1
                            Col3 = Col1
                            if (len(disp) > origin+offset) and Col1 != x8(0,0,0,0,0,0,0,0):
                                disp[(offset+origin)] = (Col1, Col2, Col3)

                            pos += 1
                            offset += 1
                            if pos >= 36: pos -= 36
                        offset += 150 - y - 1
                    origin += 6
            case "img":
                OimgData = getReg("rdi")
                OimgData = OimgData.replace("\n", "").replace(" ", "").split("-")
                imgData = [OimgData[0], OimgData[1]]
                OimgData = OimgData[2:]
                for i in OimgData:
                    split = i.split("*")
                    times = split[0]
                    rgb = split[1].split(",")
                    for i in range(int(times)):
                        imgData.append(rgb[0])
                        imgData.append(rgb[1])
                        imgData.append(rgb[2])
                pos = 0
                offset = 0
                sx = line[1]
                sy = line[2]
                if sx in variables:
                    sx = x8ToNum(getReg(variables[sx][1:]))
                if sy in variables:
                    sy = x8ToNum(getReg(variables[sy][1:]))
                origin = int(sx) + (150 * (int(sy))) - 1
                for x in range(int(imgData[0])):
                    for y in range(int(imgData[1])):
                        pos += 1
                        offset += 1
                        Col1 = x8(*[int(i) for i in imgData[-1+pos*3]])
                        Col2 = x8(*[int(i) for i in imgData[pos*3]])
                        Col3 = x8(*[int(i) for i in imgData[1+pos*3]])
                        if (len(disp) > origin+offset) and (x8ToNum(Col1) + x8ToNum(Col2) + x8ToNum(Col3)) > 3:
                            disp[offset+origin] = (Col1, Col2, Col3)
                    offset += 150 - y - 1
    except Exception as e:
        print(f"\033[91;1mAssembly error: {e}\033[0m")

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
                    setReg(variables[line[1]][1:], x8(*[str(i) for i in indexBin]))
    #START
    if startSec:
        
        start = startSec.split("\n")
        for i in start:
            if i != "":
                line = i.split(" ")
                sec(line)
    differences = []
    temp = 0
    if updateSec:
        running = True
        while running:
            start_time_update = time.time()
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
            dif = time.time() - start_time_update
            differences.append(dif)
        #print(f"Calculated frequency (+time: +accuracy): {1/(sum(iter(differences))/len(differences))}")
    else:
        pygame.quit()

def cleanup(reduced_debug=True) -> None:
    global variables, functions, memory, binaryMem
    if not reduced_debug:
        print("=" * 64)
        print("Clearing variables")
    s = time.time()
    variables.clear()
    if not reduced_debug:
        print(f"\033[32;1mDone ({time.time() - s}s)\033[0m")
    if not reduced_debug:
        print("Clearing functions")
    s = time.time()
    functions.clear()
    if not reduced_debug:
        print(f"\033[32;1mDone ({time.time() - s}s)\033[0m")
    if not reduced_debug:
        print("Clearing memory")
    s = time.time()
    try:
        memory.clear()
        memory = [x8(0,0,0,0,0,0,0,0) for i in range(memLen)]
        if not reduced_debug:
            print(f"\033[32;1mDone ({time.time() - s}s)\033[0m")
    except Exception as e:
        if not reduced_debug:
            print(f"\033[91;1mFailed to clear memory {e}\033[0m")
    if not reduced_debug:
        print("Clearing binary memory")
    s = time.time()
    try:
        binaryMem.clear()
        binaryMem = [0 for i in range(binMemLen)]
        if not reduced_debug:
            print(f"\033[32;1mDone ({time.time() - s}s)\033[0m")
    except Exception as e:
        if not reduced_debug:
            print(f"\033[91;1mFailed to clear binary memory: {e}\033[0m")

if __name__ == "__main__":
    BIOS()
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    with open(dir_path + "\\ROM.pb8") as f:
        run(f"\n{f.read()}\n")
    cleanup(reduced_debug=False)