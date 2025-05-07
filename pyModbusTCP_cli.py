
'''
The pyModbusTCP_cli application is intended to encaspulate the pyModbusTCP 
commands into a single directly executable program.  Using pyinstaller,
pyModbusTCP_cli can be packaged into an .exe file that can be run on any Windows
computer without the need for installing Python.

Execution of the application will take the form of a single command or a shell
console application allowing multiple commands to be executed.

Single command syntax:
pyModbusTCP_cli 192.168.1.10 read_holding_register 23496
15

Console app example:
pyModbusTCP_cli 192.168.1.10
> read_holding_registers 23496
15
> quit

- or -

pyModbusTCP_cli
> Read read_holding_registers 23466
ERROR - No IPAddress specified.  Use IPAddress command.
> IPAddress 192.168.1.10
> read_holding_registers 23496
15
> quit

'''

import sys
import datetime
import time
import struct

from pyModbusTCP.client import ModbusClient
from pathlib import Path
from struct import *
version = "0.1.0"
comm = None # Global variable for ModbusClient
output_format = "raw"
output_formats = ["raw", "readable", "minimal"]
show_timing = False

# CONSTANTS
NOTFOUND = -1


#region HELPER FUNCTIONS
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getNumber(s):
    assert isNumber(s), "Expected a number, got {0}".format(s)
    if isinstance(s, str):
        if s.isnumeric():
            return int(s)
        else: 
            return float(s)
    else:
        return s
        
#endregion HELPER FUNCTIONS

#region DATA HELPER FUNCTIONS
def getTagValues(tags):
    outData = []
    for tag in tags:
        if len(tag) > 0:
            try:
                result = read(tag, mode="silent")
            except Exception as error:
                #print("Error reading: " + tag + " - " + str(error))
                outData += [tag + "=!ERROR!"]
                continue
            outData += [tag + "=" + str(result)]
    return outData

def getTagValuesFromFile(filename):
    tags = []
    try:
        tags = Path(filename).read_text().split("\n")
    except Exception as error:
        print("ERROR - Error opening the file {0}. {1}".format(filename, str(error)))
        return []
    outData = getTagValues(tags)
    return outData

#endregion DATA HELPER FUNCTIONS

#region CONSOLE COMMAND DEFINITIONS
def ipAddress(args):
    global comm
    comm = ModbusClient(host=args, auto_open=True, auto_close=True)
    comm.open()

#region WRITE FUNCTIONS
def write(args):
    if (comm == None):
        print("ERROR - No IPAddress specified.  Use IPAddress command.")
        return
    words = args.split()
    if len(words) < 2:
        print("ERROR - Invalid number of arguments.  See help for more info.")
        return
    # See if the last character is a data formatter:
    # I=Integer (Default)
    # F=Float
    # M=String
    formatTypes = ["I", "S", "F", "M"]
    formatReq = words[0][-1]
    try: # Catch any formatting errors.
        if formatReq in formatTypes:
            startingRegister = int(words[0][:-1])
        else:
            startingRegister = int(words[0])
            formatReq = "I"
        # Concatenate the remaining arguments into a single argument.
        values = " ".join(words[1:])
        # Remove the brackets.
        values = values.replace("[", "").replace("]","")
        # Convert the register values to an array of integers.
        if (formatReq == "M"):
            registerValues = convertStringToInts(values)
        elif (formatReq == "F"):
            registerValues = [float(item.strip()) for item in values.split(",") if item.strip()]
            registerValues = convertFloatsToInts(registerValues)
        elif ((formatReq == "I") or (formatReq == "S")):
            registerValues = [int(item.strip()) for item in values.split(",") if item.strip()]
            registerValues = convertSIntsToInts(registerValues)
    except Exception as error:
        print("ERROR - {0}".format(str(error)))
        return
    # Write the values.
    start_time = time.time()
    try:
        ret = comm.write_multiple_registers(startingRegister, registerValues)
    except Exception as error:
        print("ERROR - {0}".format(str(error)))
    exec_time = time.time() - start_time
    if (ret):
        print("Success")
    if (show_timing):
        print("Executed in {0:7.3f} seconds.".format(exec_time))
    return

def write_multiple_registers(args):
    if (comm == None):
        print("ERROR - No IPAddress specified.  Use IPAddress command.")
        return
    words = args.split()
    if len(words) != 2:
        print("ERROR - Invalid number of arguments.  See help for more info.")
        return
    startingRegister = int(words[0])
    words[1] = words[1].replace("[", "").replace("]","")
    registerValues = [int(item.strip()) for item in words[1].split(",") if item.strip()]
    start_time = time.time()
    try:
        ret = comm.write_multiple_registers(startingRegister, registerValues)
    except Exception as error:
        print("ERROR - {0}".format(str(error)))
    exec_time = time.time() - start_time
    if (ret):
        print("Success")
    if (show_timing):
        print("Executed in {0:7.3f} seconds.".format(exec_time))
    return

def write_single_register(args):
    if (comm == None):
        print("ERROR - No IPAddress specified.  Use IPAddress command.")
        return
    words = args.split()
    if len(words) != 2:
        print("ERROR - Invalid number of arguments.  See help for more info.")
        return
    startingRegister = int(words[0])
    registerValue = int(words[1])
    start_time = time.time()
    try:
        ret = comm.write_single_register(startingRegister, registerValue)
    except Exception as error:
        print("ERROR - {0}".format(str(error)))
    exec_time = time.time() - start_time
    if (ret):
        print("Success")
    if (show_timing):
        print("Executed in {0:7.3f} seconds.".format(exec_time))
    return

#endregion WRITE FUNCTIONS

#region READ FUNCTIONS
def read(args, mode="print"):
    if (comm == None):
        print("ERROR - No IPAddress specified.  Use IPAddress command.")
        return "ERROR"
    words = args.split()
    if len(words) > 2 or len(words) == 0:
        print("ERROR - Invalid number of arguments.  See help for more info.")
        return "ERROR"
    # See if the last character is a data formatter:
    # I=Integer (Default)
    # S=Signed Integer
    # F=Float
    # M=String
    formatTypes = ["I", "S", "F", "M"]
    formatReq = words[0][-1]
    try: # Catch any formatting errors.
        if formatReq in formatTypes:
            startingRegister = int(words[0][:-1])
        else:
            startingRegister = int(words[0])
            formatReq = "I"
        numRegisters = 1
        if formatReq == "F":
            numRegisters = 2
        if len(words) > 1:
            numRegisters = int(words[1])
            if formatReq == "F":
                numRegisters = numRegisters * 2
            elif formatReq == "M":
                numRegisters = int(numRegisters / 2)
                if numRegisters < 1:
                    numRegisters = 1
    except Exception as error:
        print("ERROR - {0}".format(str(error)))
        return "ERROR"
    start_time = time.time()
    try:
        ret = comm.read_holding_registers(startingRegister, numRegisters)
    except Exception as error:
        print("ERROR - {0}".format(str(error)))
    exec_time = time.time() - start_time
    # Format output
    retFormatted = []
    # Format as unsigned integer (Default)
    if formatReq == "I":
        retFormatted = ret
    # Format as signed integer
    if formatReq == "S":
        for i in range(0, len(ret)):
            if (ret[i] > 32767):
                retFormatted.append(ret[i] - 65536)
            else:
                retFormatted.append(ret[i])
    # Format as floats
    if formatReq == "F":
        for i in range(0,len(ret)-1, 2):
            # print(ret)
            mypack=pack('>HH', ret[i], ret[i+1])
            retFormatted.append(unpack('>f', mypack)[0])
    # Format as string
    if formatReq == "M":
        retFormatted = ""
        for regVal in ret:
            bytesVal = regVal.to_bytes(2, "big")
            if bytesVal[0] == 0:
                break
            if bytesVal[1] == 0:
                retFormatted += chr(bytesVal[0])
                break
            retFormatted += chr(bytesVal[0]) + chr(bytesVal[1])
    if (mode=="print"):
        print(retFormatted)
    if (show_timing):
        print("Executed in {0:7.3f} seconds.".format(exec_time))
    return retFormatted

def read_holding_registers(args):
    if (comm == None):
        print("ERROR - No IPAddress specified.  Use IPAddress command.")
        return "ERROR"
    words = args.split()
    if len(words) > 2 or len(words) == 0:
        print("ERROR - Invalid number of arguments.  See help for more info.")
        return "ERROR"
    startingRegister = int(words[0])
    numRegisters = 1
    if len(words) > 1:
        numRegisters = int(words[1])
    start_time = time.time()
    try:
        ret = comm.read_holding_registers(startingRegister, numRegisters)
    except Exception as error:
        print("ERROR - {0}".format(str(error)))
    exec_time = time.time() - start_time
    # Format output
    retFormatted = []
    retFormatted = ret
    print(retFormatted)
    if (show_timing):
        print("Executed in {0:7.3f} seconds.".format(exec_time))
    return

def readTagFile(args):
    if (comm == None):
        print("ERROR - No IPAddress specified.  Use IPAddress command.")
        return
    words = args.split()
    filename = words[0]
    start_time = time.time()
    outData = getTagValuesFromFile(filename)
    if len(outData) > 0:
        outFile = ""
        if len(words) > 1:
            outFile = words[1]
        exec_time = time.time() - start_time
        if len(outFile) > 0:
            Path(outFile).write_text("\n".join(outData))
        else:
            print("\n".join(outData))
        if (show_timing):
            print("executed in {0:7.3f} seconds.".format(exec_time))
    return

#endregion READ FUNCTIONS

def getHelp(args):
    print('''
    Commands: (Not case sensitive.)
        Help                                            
          - Displays this list of commands.
        IPAddress <ip address>                          
          - Sets the IP address for the target device.
        Read <register>[format] [count]
          - Returns the specified register values from the target device.
          - format is:
              + 'I' for Integer (default)
              + 'S' for Signed Integer
              + 'F' for Floating point
              + 'M' for String
          - count is the number of elements to return.  (default is 1)
        Read_Holding_Registers <register> [count]
          - Returns the specified register values as unformatted integers from the target device.
        Write <starting register>[format] <comma separated list of values>
          - Writes the value(s) using the format to the starting register.
        Write_Single_Register <register> <value>
          - Writes the integer value to the specified register.
        Write_Multiple_registers <starting register> <comma separated list of values>
          - Writes the integer values starting at the specified register.
        ShowTiming (On | Off)
          - Turns on or off the time to execute feedback.
        Version
          - Displays the version number for the application.
        Quit                                            
          - Leave console application.
    ''')
    return

def showTiming(args):
    global show_timing
    if (args in ["on", "off"]):
        show_timing = args == "on"
        print("ShowTiming set to " + args + ".")
    else:
        print("Invalid ShowTiming argument.  Valid arguments are 'on' or 'off'.")
    return

#endregion CONSOLE COMMAND DEFINITIONS

#region COMMAND LOOP
def parseCommand(command):
    words = command.casefold().split()
    if (len(words) > 0):
        if (words[0] == "help"):
            getHelp(command)
        elif (words[0] == "ipaddress"):
            ipAddress(words[1])
        elif (words[0] == "read"):
            read(getAdditionalArgs(command))
        elif (words[0] == "read_holding_registers"):
            read_holding_registers(getAdditionalArgs(command))
        elif (words[0] == "readtagfile"):
            readTagFile(getAdditionalArgs(command))
        elif (words[0] == "write"):
            write(getAdditionalArgs(command))
        elif (words[0] == "write_single_register"):
            write_single_register(getAdditionalArgs(command))
        elif (words[0] == "write_multiple_registers"):
            write_multiple_registers(getAdditionalArgs(command))
        elif (words[0] == "showtiming"):
            showTiming(getAdditionalArgs(command))
        elif (words[0] == "version"):
            print(version)
        else:
            print("ERROR - Unrecognized command.  Enter Help for a list of commands.")
    return

def commandLoop():
    command = input("pyModbusTCP_cli> ")
    while (command.casefold() != "quit"):
        parseCommand(command)
        command = input("pyModbusTCP_cli> ")
    return

#endregion COMMAND LOOP

#region HELPER FUNCTIONS
def isIPAddress(value):
    return len(value.split(".")) == 4

def getAdditionalArgs(command):
    words = command.split()
    if (len(words) > 1):
        return " ".join(words[1:])
    else:
        return ""

def convertSIntsToInts(intValues):
    result = []
    for intValue in intValues:
        if (intValue < 0):
            intValue = 65536 + intValue
        result.append(intValue)
    return result

def convertFloatsToInts(floatValues):
    result = []
    for valueFloat in floatValues:
        # Pack the float into 4 bytes using big-endian format.
        packed = struct.pack('!f', valueFloat)
        # Unpack the 4 bytes into two 16-bit unsigned integers.
        high, low = struct.unpack('!HH', packed)
        result.extend([high, low])
    return result

def convertStringToInts(stringValue):
    result = []
    for i in range(0, len(stringValue), 2):
        high = ord(stringValue[i])
        # Check if there's a second character in the pair.
        low = ord(stringValue[i+1]) if i+1 < len(stringValue) else 0
        # Combine the two bytes into one 16-bit integer.
        combined = (high << 8) | low
        result.append(combined)
    return result

#endregion HELPER FUNCTIONS

#region MAIN
def main():
    global comm
    arguments = sys.argv
    if (len(arguments) > 1):
        if (isIPAddress(arguments[1])):
            ipAddress(arguments[1])
            if (len(arguments) > 2):
                parseCommand(" ".join(arguments[2:]))
                comm.close()
            else:
                commandLoop()
                comm.close()
        else:
            parseCommand(" ".join(arguments[1:]))
    else:
        commandLoop()
        comm.close()
    return

#endregion MAIN

main()
