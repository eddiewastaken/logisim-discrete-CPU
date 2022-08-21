#Define microinstruction values
micro = {
    "HLT" : "0b1000000000000000", #Halt clock
    "MI"  : "0b0100000000000000", #Memory address register in
    "RI"  : "0b0010000000000000", #RAM data in
    "RO"  : "0b0001000000000000", #RAM data out
    "IO"  : "0b0000100000000000", #Instruction register out
    "II"  : "0b0000010000000000", #Instruction register in
    "AI"  : "0b0000001000000000", #A register in
    "AO"  : "0b0000000100000000", #A register out
    "EO"  : "0b0000000010000000", #ALU out
    "SU"  : "0b0000000001000000", #ALU subtract
    "BI"  : "0b0000000000100000", #B register in
    "OI"  : "0b0000000000010000", #Output register in
    "CE"  : "0b0000000000001000", #Program counter enable
    "CO"  : "0b0000000000000100", #Program counter out
    "J"   : "0b0000000000000010", #Jump (program counter in)
    "FI"  : "0b0000000000000001"  #Flag register in
} 

#2D array of opcodes and microinstructions in each
ops = [
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #0000 - NOP (No operation)
    ["MI|CO",  "RO|II|CE",  "IO|MI",  "RO|AI",  "0",           "0", "0", "0"],   #0001 - LDA (Load A reg with contents of given address)
    ["MI|CO",  "RO|II|CE",  "IO|MI",  "RO|BI",  "EO|AI|FI",    "0", "0", "0"],   #0010 - ADD (Add contents of given address to A reg)
    ["MI|CO",  "RO|II|CE",  "IO|MI",  "RO|BI",  "EO|AI|SU|FI", "0", "0", "0"],   #0011 - SUB (Subtract contents of given address from A reg)
    ["MI|CO",  "RO|II|CE",  "IO|MI",  "AO|RI",  "0",           "0", "0", "0"],   #0100 - STA (Store contents of A reg at given address)
    ["MI|CO",  "RO|II|CE",  "IO|AI",  "0",      "0",           "0", "0", "0"],   #0101 - LDI (Load A reg with given value)
    ["MI|CO",  "RO|II|CE",  "IO|J",   "0",      "0",           "0", "0", "0"],   #0110 - JMP (Jump to given address)
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #0111 - JC (Jump to given address if carry flag is set)
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #1000 - JZ (Jump to given address if zero flag is set)
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #1001
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #1010
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #1011
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #1100
    ["MI|CO",  "RO|II|CE",  "0",      "0",      "0",           "0", "0", "0"],   #1101
    ["MI|CO",  "RO|II|CE",  "AO|OI",  "0",      "0",           "0", "0", "0"],   #1110 - OUT (Load Out reg with contents of A reg)
    ["MI|CO",  "RO|II|CE",  "HLT",    "0",      "0",           "0", "0", "0"]    #1111 - HLT (Halt the clock)
]

JMP = ["MI|CO",  "RO|II|CE",  "IO|J",   "0",      "0",           "0", "0", "0"]

#Parse each opcode step into int values
def parseExp(exp):
    #Replace microcode label(s) with binary value(s)
    for code, val in micro.items():
        exp = exp.replace(code, val)
    #Evaluate bitwise operation expression as int
    return eval(exp)

#Parse entire 2d array, return 2d array of same dimensions containing computed values
def parse2D(array):
    #Create result array
    rows = len(array)
    cols = len(array[0])
    result = [[0 for x in range(cols)] for y in range(rows)]
    #Map function
    for i in range(0, rows):
        for j in range(0, cols):
            result[i][j] = parseExp(array[i][j])
    return result

def toHex(array):
    return [[("%0.4x" % i) for i in j] for j in array]

def toBin(array):
    return [[(format(i, "016b")) for i in j] for j in array]

def toFiles(array, header):
    with open("ROM_LOW_FLAGS.ROM", mode='a', encoding='utf-8') as rL, open("ROM_HIGH_FLAGS.ROM", mode='a', encoding='utf-8') as rH:
        if header:
            #Write headers for Logisim ROM file
            rL.write("v2.0 raw")
            rL.write("\n")
            rH.write("v2.0 raw")
            rH.write("\n")
        #Write upper and lower bytes of hex values to each file, seperated by whitespace
        rows = len(array)
        cols = len(array[0])
        for i in range(0, rows):
            for j in range(0, cols):
                val = array[i][j]
                rL.write(val[2:])
                rL.write(' ')
                rH.write(val[:2])
                rH.write(' ')
        #Close files
        rL.close()
        rH.close()

#Neither
out = parse2D(ops)
outBin = toBin(out)
outHex = toHex(out)
toFiles(outHex, True)

#JC
JC = ops.copy()
JC[7] = JMP
out = parse2D(JC)
outBin = toBin(out)
outHex = toHex(out)
toFiles(outHex, False)

#JZ
JZ = ops.copy()
JZ[8] = JMP
out = parse2D(JZ)
outBin = toBin(out)
outHex = toHex(out)
toFiles(outHex, False)

#Both
BOTH = ops.copy()
BOTH[7] = JMP
BOTH[8] = JMP

#Main
out = parse2D(BOTH)
outBin = toBin(out)
outHex = toHex(out)
toFiles(outHex, False)