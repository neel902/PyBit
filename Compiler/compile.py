import prnExtra
from prnExtra import Flags
import time
import grammars
import win32clipboard

def setClipboard(text : str) -> None:
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

import sys

#prnExtra.clearConsole()
#prnExtra.prnExtra("Compiling code...", Flags.ConsoleFonts.BOLD)
#prnExtra.prnExtra("Tokenising - 5%", Flags.ConsoleColours.GREEN, Flags.ConsoleFonts.BOLD)

def Tokens(text : str):
    lines = []
    line = ""
    inString = False
    for char in text:
        if char in grammars.QUOTES:
            inString = not inString
            line += "'"
            continue
        if inString:
            line += char
        else:
            if char in grammars.WHITE:
                continue
            if char in grammars.EOL:
                if line.strip() == "":
                    continue
                lines.append(line)
                line = ""
            else:
                line += char
    if line != "":
        prnExtra.prnExtra("Tokenisation failed: EOL Error (Are you missing a semicolon?)", Flags.ConsoleColours.RED, Flags.ConsoleFonts.BOLD)
        sys.exit()
    if inString:
        prnExtra.prnExtra("Tokenisation failed: EOF Error (Are you missing a quotation mark?)", Flags.ConsoleColours.RED, Flags.ConsoleFonts.BOLD)
        sys.exit()
    return lines

def Parse(tokens):
    finalParsed = []
    parsed = []
    currentToken = ""
    inString = False
    ENDS = f"{grammars.PAREN_START}{grammars.PAREN_END}{grammars.COMMA}{grammars.PAREN_START_CURLY}{grammars.PAREN_END_CURLY}"
    OPS = "=+-*"

    for line in tokens:
        for char in line:
            if char in grammars.QUOTES:
                inString = not inString
                if currentToken.strip() != "":
                    parsed.append(currentToken)
                currentToken = ""
                continue
            if inString:
                currentToken += char
                continue
            else:
                if char in grammars.WHITE:
                    continue
                else:
                    currentToken += char
            if char in ENDS:
                if currentToken.strip() != "":
                    parsed.append(currentToken)
                currentToken = ""
                continue
            if char in OPS:
                parsed.append(currentToken[:-1])
                parsed.append(char)
                currentToken = ""
                continue
        if currentToken.strip() != "":
            parsed.append(currentToken)
        finalParsed.append(parsed)
        
        parsed = []
        currentToken = ""
    for _ in range(finalParsed.count("")):
        finalParsed.remove("")
    for _ in range(finalParsed.count(" ")):
        finalParsed.remove(" ")
    #print(finalParsed)
    return finalParsed

import random

def genHash(seed):
    CHARS = "qwertyuiopasdfghjklzxcvbnm"
    _hash = ""
    for i in range(8):
        random.seed(str(seed)+str(i))
        _hash += CHARS[random.randint(0, len(CHARS)-1)]
    return _hash

REGLIST = [f"{i1}{i2}{i3}{i4}" for i1 in range(0,2) for i2 in range(0,2) for i3 in range(0,2) for i4 in range(0,2)]
REGLIST.append("rax")
REGLIST.append("rdi")
def compile(parsed):
    data_section = ""
    start_section = ""
    func_section = ""
    used_registries = []
    inFunc = False
    func = []
    funcName = ""
    tick_section = False
    for line in parsed:
        # Deal with making functions
        if line[0][-1] == grammars.PAREN_START_CURLY:
            inFunc = True
            funcName = line[0][:-1]
            func.append(line[1:])
            continue
        if line[0] == grammars.PAREN_END_CURLY:
            fData, fCode, _, __ = (compile(func))
            fData = fData.split("\n")
            if funcName == "tick":
                tick_section = True
            for i in fData:
                if i in data_section:
                    pass
                else:
                    data_section += "\n"+i
            func_section += f"\n.{funcName}{fCode}"
            inFunc = False
            func = ""
            continue
        if inFunc:
            func.append(line)
            continue
        # Deal with calling functions
        
        ibFuncs = ["syscall", "print"]
        #print(line)
        if len(line) >= 2:
            
           
            if line[0][-1] == grammars.PAREN_START and line[-1][-1] == grammars.PAREN_END:
                # In built
                funct = line[0][:-1]
                if funct in ibFuncs:
                    if funct == "syscall":
                        start_section += "\nSYSCALL"
                    if funct == "print":
                        reg = line[1][:-1]
                        if reg[1:] not in used_registries:
                            used_registries.append(reg)
                            data_section += f"\nREG {genHash(reg)} {reg}"
                        start_section += f"\nOUT {genHash(reg)}"
                    continue
                    
                # Custom functions
                start_section += f"\nCALL {funct}"
                continue
        
        # Deal with operators
        if line[0][1:] in REGLIST:
            if line[0] not in used_registries:
                used_registries.append(line[0])
                data_section += f"\nREG {genHash(line[0])} {line[0]}"
            if len(line) < 4:
                if line[2][0] == grammars.REGISTRY_PREFIX:
                    if line[2] not in used_registries:
                        used_registries.append(line[2])
                        data_section += f"\nREG {genHash(line[2])} {line[2]}"
                    start_section += f"\nMOV {genHash(line[2])} {genHash(line[0])}"
                else:
                    if line[2][0] in "01":
                        start_section += f"\nSET {genHash(line[0])} {line[2]}"
                    else:
                        start_section += f"\nSSET {genHash(line[0])} {line[2]}"
                continue
            if line[2] not in used_registries:
                used_registries.append(line[0])
                data_section += f"\nREG {genHash(line[0])} {line[0]}"
            if line[4] not in used_registries:
                used_registries.append(line[0])
                data_section += f"\nREG {genHash(line[0])} {line[0]}"
            operand = line[3]
            operation = {"+":"ADD","-":"SUB","*":"MUL"}[operand]
            start_section += f"\n{operation} {genHash(line[2])} {genHash(line[4])} {genHash(line[0])}"
    return data_section, start_section, func_section, tick_section
    

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage (With Compiler as current directory): python3 compile.py <file_name>")
    else:
        file_name = sys.argv[1]
        prnExtra.clearConsole()
        prnExtra.prnExtra("Compiling code...", Flags.ConsoleFonts.BOLD)
        prnExtra.prnExtra("Tokenising", Flags.ConsoleColours.BLUE, Flags.ConsoleFonts.BOLD)
        code = ""
        try:
            f = open(file_name, "r")
            start_time = time.time()
            code = f.read()           
        except:
            pass
        finally:
            f.close()
        tokens = Tokens(code)
        prnExtra.prnExtra(f"Done in {time.time() - start_time}", Flags.ConsoleColours.GREEN, Flags.ConsoleFonts.BOLD)

        prnExtra.prnExtra("Parsing", Flags.ConsoleColours.BLUE, Flags.ConsoleFonts.BOLD)

        start_time = time.time()
        parsed = Parse(tokens)

        prnExtra.prnExtra(f"Done in {time.time() - start_time}", Flags.ConsoleColours.GREEN, Flags.ConsoleFonts.BOLD)

        prnExtra.prnExtra("Compiling", Flags.ConsoleColours.YELLOW, Flags.ConsoleFonts.BOLD)

        start_time = time.time()
        try:
            compiled = compile(parsed)
            code = f"\n{compiled[2]}\n_data{compiled[0]}"
            if compiled[1].strip() != "":
                code += f"\n_start{compiled[1]}"
            if compiled[3]:
                code += f"\n_tick\nCALL tick"
        except Exception as e:
            prnExtra.prnExtra(f"Compilation error: {e}", Flags.ConsoleColours.RED, Flags.ConsoleFonts.BOLD)
            sys.exit()
        prnExtra.prnExtra(f"Done in {time.time() - start_time}", Flags.ConsoleColours.GREEN, Flags.ConsoleFonts.BOLD)

        print(code)
        setClipboard(code)


if __name__ == "__main__":
    main()