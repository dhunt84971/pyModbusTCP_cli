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
pyModbusTCP_cli 192.168.1.10 read 23496
[15]
```

Console app example:
```
pyModbusTCP_cli 192.168.1.10
pyModbusTCP_cli> read 23496
[15]
pyModbusTCP_cli> quit
```

OR
```
pyModbusTCP_cli
pyModbusTCP_cli> read 3080
ERROR - No IPAddress specified.  Use IPAddress command.
pyModbusTCP_cli> IPAddress 192.168.1.10
pyModbusTCP_cli> read 23496
[15]
pyModbusTCP_cli> quit
```

Read an array:
```
pyModbusTCP_cli 192.168.1.10 read 23496 5
[15, 2, 3, 4, 5]
```

Read a floating point value:
```
pyModbusTCP_cli 192.168.1.10 read 23502F
[3.141962368934]
```
**Note: Floating points take 2 registers for each value.  Specify the count in the number of floating point values to be returned.**

Read a string value:
```
pyModbusTCP_cli 192.168.1.10 read 23502M 30
Test
```
**Note: Two characters are returned for each register.  Specify the count in the maximum number of characters to be returned. String values returned will be null terminated.**

Write a value:
```
pyModbusTCP_cli 192.168.1.10 write 23496 0
Success
```

## Commands
The following commands are not case-sensitive.
+ ```Help```                        - Displays this list of commands.
+ ```IPAddress <ip address>```      - Sets the IP address for the target device.
+ ```Quit```                        - Leave console application.
+ ```Read <register>[format] [count]```                  - Returns the specified register values from the target device.
    + ```format``` - Can be:
        + 'I' for Integer (default)
        + 'S' for Signed Integer
        + 'F' for Floating point
        + 'M' for String
    + ```count``` - Specify the number of elements to return.  (default is 1)
+ ```Read_Holding_Registers <register> [count]```   - Returns the specified register values as unformatted integers from the target device.
+ ```Write <starting register>[format] <comma separated list of values>```  - Writes the value(s) using the format to the starting register.
+ ```Write_Single_Register <register> <value>```    - Writes the integer value to the specified register.
+ ```Write_Multiple_registers <starting register> <comma separated list of values>```   - Writes the integer values starting at the specified register.
+ ```ShowTiming (On | Off)```      - Turns on or off the time to execute feedback.
+ ```Version``` - Displays the version.

## Multi-Tag Commands:
Filenames are case sensitive.
+ ```ReadTagFile <filename> [<outfile>]```
    - Returns the values of the tags from the file.

## The pyModbusTCP Project
This application is a command line wrapper to ease the use of the many functions of the pyModbusTCP library.  The pyinstaller program is used to create an executable package on Windows that does not require the installation of Python.

For more information and documentation:
https://github.com/sourceperl/pyModbusTCP

**Special thanks to all the contributors that make pyModbusTCP possible.**

## Development Environment
In order to build the executable using pyinstaller, first clone this repository and then install both pyModbusTCP and pyinstaller using pip.

```
git clone https://github.com/dhunt84971/pyModbusTCP_cli.git
cd pyModbusTCP_cli
pip install pyModbusTCP
pip install pyinstaller
```

### Building the Executable
In order to build the executable for the Windows platform it is necessary to run pyinstaller on a Windows computer.  Keep in mind that Python 3.9+ cannot run on Windows 7.  For this reason it is recommended that a Windows 7 system with Python installed be used to create the executable in order to ensure compatability with Windows 7 and newer versions of Windows.
 
```
pyinstaller -F pyModbusTCP_cli.py
```

## License

This project is licensed under the MIT License.
