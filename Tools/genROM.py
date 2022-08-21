import csv, sys, os, argparse

###CLI Usage: python genROM.py "CSVFile.csv" "Address Width" "Data Width"

def createParser():
    parser = argparse.ArgumentParser(description='Generates a Logisim ROM file given a CSV of desired memory contents.')
    parser.add_argument('CSV', help='Path to input CSV file (without headers)')
    parser.add_argument('ADDR', help='Amount of ROM address lines (note - not total cells)', type=int)
    parser.add_argument('WIDTH', help='Bit width of each ROM cell', type=int)
    return parser

def readCSV(path):
    datafile = open(path, 'r')
    datareader = csv.reader(datafile, delimiter=',')
    data = []
    for row in datareader:
        data.append(row)
    return data

def ceil(a, b):
    return -(-a // b)

def toHex(array, addr, width):
    hexArray = [[('%0*X' % (ceil(width,4), int(i, base=2))) for i in j] for j in array]
    addresses = (2**addr)
    csvSize = sum(len(row) for row in hexArray)
    if csvSize > addresses:
        print("\n")
        print("Error - too many cells in CSV to fit in ROM!")
        print("Available ROM locations: " + str(addresses))
        print("Supplied cells: " + str(csvSize))
        print("Please edit, then run me again!")
        print("\n")
        exit()
    rows = len(array)
    cols = len(array[0])
    for i in range(0, rows):
        for j in range(0, cols):
            #Checks width of data in each CSV cell
            actualWidth = len(str(bin(int(hexArray[i][j], base=16)))[2:])
            if actualWidth > width:
                print("\n")
                print("Error - value in cell too large for ROM's bit width!")
                print("Problem value:  " + str(bin(int(hexArray[i][j], base=16)))[2:] + " at cell (" + str(i) + ", " + str(j) + ")")
                print("Please edit, then run me again!")
                print("\n")
                exit()
    return hexArray

def confirm(addr, width):
    response = ""
    addresses = (2**addr)
    print("\n")
    print("Writing for a ROM of " + str(addresses) + " locations * " + str(width) + " bit values.")
    print("\n")
    while response != "Y" and response != "N":
        response = input("Correct? Enter Y to proceed, or N to exit: ")
    return response

#def toBin(array):
#    return [[(format(i, "016b")) for i in j] for j in array]

def toFile(array):
    with open("out.ROM", mode='w', encoding='utf-8') as out:
        #Write headers for Logisim ROM file
        out.write("v2.0 raw")
        out.write("\n")
        #Write hex values to file, seperated by whitespace
        rows = len(array)
        cols = len(array[0])
        for i in range(0, rows):
            for j in range(0, cols):
                val = array[i][j]
                out.write(val)
                out.write(' ')
        #Close file
        out.close()
        print("\n")
        print("ROM file successfully created!")
        print("\n")
                
if __name__ == "__main__":
    argParser = createParser()
    args = argParser.parse_args(sys.argv[1:])
    proceed = confirm(args.ADDR,args.WIDTH)
    if proceed == "N":
        print("\n")
        exit()
    else:
        exists = os.path.exists(args.CSV)
        if exists:
            toFile(toHex(readCSV(args.CSV), args.ADDR, args.WIDTH))
        else:
            print("\n")
            print("Error - supplied CSV path doesn't exist!")
            print("\n")
