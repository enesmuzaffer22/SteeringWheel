@echo off
echo ================================================
echo WINDOWS FIREWALL CHECK FOR PORT 5000
echo ================================================
echo.

echo Checking current firewall rules for port 5000...
netsh advfirewall firewall show rule name=all | findstr "5000"

echo.
echo ================================================
echo ADDING FIREWALL RULE (Run as Administrator)
echo ================================================
echo.

REM Add inbound rule for port 5000
netsh advfirewall firewall add rule name="Steering Wheel Server - Port 5000" dir=in action=allow protocol=TCP localport=5000

echo.
if %errorlevel% equ 0 (
    echo SUCCESS: Firewall rule added for port 5000
) else (
    echo ERROR: Failed to add firewall rule
    echo Please run this script AS ADMINISTRATOR
)

echo.
pause
