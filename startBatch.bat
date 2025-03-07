REM startBatch.bat batchField1 batchField2 batchField3 batchField4 batchField5 batchField6
REM Each argument will be accessible as %1 through %6

pyModbusTCP_cli.exe 100.100.100.52 write 42367M %1
pyModbusTCP_cli.exe 100.100.100.52 write 42427M %2
pyModbusTCP_cli.exe 100.100.100.52 write 42487M %3
pyModbusTCP_cli.exe 100.100.100.52 write 42547M %4
pyModbusTCP_cli.exe 100.100.100.52 write 42607M %5
pyModbusTCP_cli.exe 100.100.100.52 write 42667M %6
pyModbusTCP_cli.exe 100.100.100.52 write 42364 1
