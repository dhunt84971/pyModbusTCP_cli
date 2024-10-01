# pyModbusTCP_cli

The pyModbusTCP_cli application is intended to encaspulate the pyModbusTCP 
commands into a single directly executable program.  Using pyinstaller,
pyModbusTCP_cli can be packaged into an .exe file that can be run on any Windows
computer without the need for installing Python.

Execution of the application will take the form of a single command or a shell
console application allowing multiple commands to be executed.

## Examples of Usage
Single command syntax example:
```
pyModbusTCP_cli 192.168.1.10 read_holding_register 23496
15
```

Console app example:
```
pyModbusTCP_cli 192.168.1.10
pyModbusTCP_cli> read_holding_registers 23496
15
pyModbusTCP_cli> quit
```

OR
```
pyModbusTCP_cli
pyModbusTCP_cli> Read read_holding_registers
ERROR - No IPAdress specified.  Use IPAddress command.
pyModbusTCP_cli> IPAddress 192.168.1.10
pyModbusTCP_cli> read_holding_registers 23496
15
pyModbusTCP_cli> quit
```

Read an array:
```
pyModbusTCP_cli 192.168.1.10 read_holding_registers 23496 5
[15, 2, 3, 4, 5]
```

Read a floating point value:
```
pyModbusTCP_cli 192.168.1.10 read_holding_registers 23502F
[3.141962368934]
```
**Note: Floating points take 2 registers for each value.  Specify the count in the number of floating point values to be returned.**

Read a string value:
```
pyModbusTCP_cli 192.168.1.10 read_holding_registers 23502M 30
Test
```
**Note: Two characters are returned for each register.  Specify the count in the maximum number of characters to be returned. String values returned will be null terminated.**

## Commands
The following commands are not case-sensitive.
+ ```Help```                        - Displays this list of commands.
+ ```IPAddress <ip address>```      - Sets the IP address for the target PLC.
+ ```Quit```                        - Leave console application.
+ ```GetPLCTime```                  - Returns the PLC time.
+ ```SetPLCTime```                  - Sets the PLC time to the current time.
+ ```Read <tag>```                  - Returns the specified tag's value from the target PLC.
+ ```Write <tag> <value>```         - Sets the specified tag's value in the target PLC.
+ ```Output (Raw | Readable)```     - Sets the output format.  Raw is the default.
+ ```ShowTiming (On | Off)```      - Turns on or off the time to execute feedback.
          
### Multi-Tag Commands:
Filenames are case sensitive.
+ ```ReadTagFile <filename> [<outfile>]```
    - Returns the values of the tags from the file.
+ ```OptimizeTagFile <filename> [<outfile>]```
    - Returns an optimized tag list from the source file.
+ ```ReadOptimizedTagFile <tagfilename> <optimizedtagfilename> [<outfile>]```
    - Returns the values of the tags from the tagfile using the optimizedtagfile to retrieve the values.

## The pycomm3 Project
This application is a command line wrapper to ease the use of the many functions of the pycomm3 library.  The pyinstaller program is used to create an executable package on Windows that does not require the installation of Python.

For more information and documentation:
https://github.com/ottowayi/pycomm3

**Special thanks to ruscito, ottowayi and all the contributors that make pycomm3 possible.**

## Development Environment
In order to build the executable using pyinstaller, first clone this repository and then install both pylogix and pyinstaller using pip.

```
git clone https://github.com/dhunt84971/pycomm3_slc_cli.git
cd pycomm3_slc_cli
pip install pycomm3
pip install pyinstaller
```

### Building the Executable
In order to build the executable for the Windows platform it is necessary to run pyinstaller on a Windows computer.  Keep in mind that Python 3.9+ cannot run on Windows 7.  For this reason it is recommended that a Windows 7 system with Python installed be used to create the executable in order to ensure compatability with Windows 7 and newer versions of Windows.
 
```
pyinstaller -F pycomm3_slc_cli.py
```

## License

This project is licensed under the MIT License.
