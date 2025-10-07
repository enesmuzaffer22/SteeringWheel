@echo off
echo ================================================
echo vJoy Process Checker
echo ================================================
echo.
echo Checking for programs using vJoy...
echo.

tasklist | findstr /I "joy.cpl"
if %errorlevel% == 0 (
    echo [FOUND] Game Controllers panel is open
    echo Solution: Close joy.cpl window
    echo.
)

tasklist | findstr /I "vJoyConf"
if %errorlevel% == 0 (
    echo [FOUND] Configure vJoy is open
    echo Solution: Close Configure vJoy window
    echo.
)

tasklist | findstr /I "python"
if %errorlevel% == 0 (
    echo [FOUND] Python processes running
    echo One of them might be using vJoy
    echo.
)

echo.
echo ================================================
echo Manual steps:
echo 1. Close all game controllers windows
echo 2. Close Configure vJoy if open
echo 3. Kill any old Python processes
echo 4. Run: python main.py
echo ================================================
pause
