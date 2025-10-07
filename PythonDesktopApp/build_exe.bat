@echo off
echo ================================================
echo BUILDING STEERING WHEEL SERVER EXECUTABLE
echo ================================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ERROR: PyInstaller not found!
    echo.
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

REM Clean previous builds
echo Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Build the executable
echo Building executable with PyInstaller...
pyinstaller --clean SteeringWheelServer.spec

echo.
echo ================================================
if exist "dist\SteeringWheelServer.exe" (
    echo SUCCESS: Executable created!
    echo Location: dist\SteeringWheelServer.exe
    echo.
    echo IMPORTANT NOTES:
    echo 1. Run the .exe AS ADMINISTRATOR
    echo 2. Allow Windows Firewall access when prompted
    echo 3. Make sure vJoy is installed and configured
    echo.
) else (
    echo FAILED: Executable not created
    echo Check the errors above
)
echo ================================================
pause
