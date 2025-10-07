@echo off
echo ===============================================
echo vJoy Quick Test
echo ===============================================
echo.
echo Opening Game Controllers panel...
start joy.cpl
echo.
echo INSTRUCTIONS:
echo 1. In the window that opened, select "vJoy Device"
echo 2. Click "Properties"
echo 3. Watch the axes as this test runs
echo.
pause
echo.
echo Starting axis test...
echo You should see the crosshair and sliders moving!
echo.
python c:\Users\Muzaffer\Documents\GitHub\SteeringWheel\PythonDesktopApp\test_axes.py
