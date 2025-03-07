@echo off
REM Get Batchfields from chart recorder over modbus.

for /f "delims=" %%a in ('pyModbusTCP_cli.exe 100.100.100.52 read 42367M 60') do set "bf1=%%a"
for /f "delims=" %%a in ('pyModbusTCP_cli.exe 100.100.100.52 read 42427M 60') do set "bf2=%%a"
for /f "delims=" %%a in ('pyModbusTCP_cli.exe 100.100.100.52 read 42487M 60') do set "bf3=%%a"
for /f "delims=" %%a in ('pyModbusTCP_cli.exe 100.100.100.52 read 42547M 60') do set "bf4=%%a"
for /f "delims=" %%a in ('pyModbusTCP_cli.exe 100.100.100.52 read 42607M 60') do set "bf5=%%a"
for /f "delims=" %%a in ('pyModbusTCP_cli.exe 100.100.100.52 read 42667M 60') do set "bf6=%%a"

echo %bf1%
echo %bf2%
echo %bf3%
echo %bf4%
echo %bf5%
echo %bf6%
