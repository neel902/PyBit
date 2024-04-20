import disks

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

memory = [x8(0,0,0,0,0,0,0,0) for i in range(2**4 - 1)]
disp = [(x8(0,0,0,0,0,0,0,0), x8(0,0,0,0,0,0,0,0), x8(0,0,0,0,0,0,0,0)) for i in range(100 * 150)]
binaryMem = [0 for i in range(2**8 - 1)]

clock = x8(0,0,0,0,0,0,0,0)
carry = 0

rax = x8(0,0,0,0,0,0,0,0)
rdi = ""

CHARS = ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"£$%^&*()-+#~:;{}[]<>,./?\|`¬¦'

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
    by2Neg = by2
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

def getReg(id : str):
    global rax, rdi
    if id == "Clock":
        return clock
    elif id == "Carry":
        return carry
    elif id == "rax":
        return rax
    elif id == "rdi":
        return rdi
    else:
        return memory[x4to10(id)]
    
def setReg(id : str, val):
    global rax, rdi
    if id == "rax":
        rax = val
    elif id == "rdi":
        rdi = val
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

def x8ToNum(CODE):
    return CODE.b1 * 2**7 + CODE.b2 * 2**6 + CODE.b3 * 2**5 + CODE.b4 * 2**4 + CODE.b5 * 2**3 + CODE.b6 * 2**2 + CODE.b7 * 2 + CODE.b8

file_descriptor = ""

def sysCall():
    global rax, rdi, file_descriptor
    if rax == x8(0,0,0,0,0,0,0,1):
        file_descriptor = rdi
    if rax == x8(0,0,0,0,0,0,1,0):
        disks.setFile(file_descriptor, rdi)
    if rax == x8(0,0,0,0,0,0,1,1):
        file_descriptor = ""