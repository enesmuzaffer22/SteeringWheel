@echo off
echo ================================================================================
echo vJoy HIZLI KONTROL - joy.cpl ile Test
echo ================================================================================
echo.
echo 1. ONCE joy.cpl ACIN:
echo    - Windows + R tusuna basin
echo    - "joy.cpl" yazin ve Enter
echo    - "vJoy Device" secin
echo    - "Properties" tiklayin
echo    - Bu pencereyi ACIK TUTUN
echo.
echo 2. Bu script eksenleri hareket ettirecek
echo    joy.cpl penceresinde hareketleri IZLEYIN!
echo.
pause

python quick_vjoy_test.py

pause
