
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
> Read read_holding_registers
ERROR - No IPAdress specified.  Use IPAddress command.
> IPAddress 192.168.1.10
> read_holding_registers 23496
15
> quit

'''

import sys
import datetime
import time

from pyModbusTCP.client import ModbusClient
from pathlib import Path
from struct import *
version = "0.0.1"
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
                result = comm.read(tag)
            except Exception as error:
                #print("Error reading: " + tag + " - " + str(error))
                outData += [tag + "=!ERROR!"]
                continue
            outData += [tag + "=" + str(result.value)]
    return outData
#endregion DATA HELPER FUNCTIONS

#region CONSOLE COMMAND DEFINITIONS
def ipAddress(args):
    global comm
    comm = ModbusClient(host=args, auto_open=True, auto_close=True)
    comm.open()

def read_holding_registers(args):
    if (comm == None):
        print("ERROR - No IPAddress specified.  Use IPAddress command.")
        return
    words = args.split()
    if len(words) > 2 or len(words) == 0:
        print("ERROR - Invalid number of arguments.  See help for more info.")
        return
    # See if the last character is a data formatter:
    # I=Integer (Default)
    # F=Float
    # M=String
    formatTypes = ["I", "F", "M"]
    formatReq = words[0][-1]
    if formatReq in formatTypes:
        startingRegister = int(words[0][:-1])
    else:
        startingRegister = int(words[0])
        formatReq = "I"
    # Get the number of registers to read
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
    start_time = time.time()
    ret = comm.read_holding_registers(startingRegister, numRegisters)
    exec_time = time.time() - start_time
    # Format output
    retFormatted = []
    if formatReq == "I":
        retFormatted = ret
    # Format as floats
    if formatReq == "F":
        for i in range(0,len(ret)-1, 2):
            print(ret)
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
    print(retFormatted)
    if (show_timing):
        print("Executed in {0:7.3f} seconds.".format(exec_time))
    return

def getHelp(args):
    print('''
    Commands: (Not case sensitive.)
        Help                                            
          - Displays this list of commands.
        IPAddress <ip address>                          
          - Sets the IP address for the target device.
        Read_Holding_Registers <register>[format] [count]       
          - Read 4x holding register data from the device.
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
        elif (words[0] == "read_holding_registers"):
            read_holding_registers(getAdditionalArgs(command))
        elif (words[0] == "showtiming"):
            showTiming(getAdditionalArgs(command))
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