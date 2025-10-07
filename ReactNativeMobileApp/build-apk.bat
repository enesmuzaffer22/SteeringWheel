@echo off
echo ========================================
echo   Steering Wheel App - APK Builder
echo ========================================
echo.
echo This script will help you build the Android APK.
echo.
echo Prerequisites:
echo   1. Node.js installed
echo   2. Expo account (free at expo.dev)
echo.
pause

echo.
echo Step 1: Checking if EAS CLI is installed...
where eas >nul 2>nul
if %errorlevel% neq 0 (
    echo EAS CLI not found. Installing...
    call npm install -g eas-cli
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install EAS CLI
        pause
        exit /b 1
    )
) else (
    echo EAS CLI is already installed!
)

echo.
echo Step 2: Checking if you're logged in...
call eas whoami
if %errorlevel% neq 0 (
    echo.
    echo You're not logged in. Please login now...
    echo If you don't have an account, create one at: https://expo.dev/signup
    echo.
    call eas login
    if %errorlevel% neq 0 (
        echo ERROR: Login failed
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo   Ready to Build APK!
echo ========================================
echo.
echo This will build your APK in the cloud.
echo Build time: approximately 10-15 minutes
echo.
echo The APK will be available for download when complete.
echo.
pause

echo.
echo Starting build...
call eas build -p android --profile preview

echo.
echo ========================================
echo   Build Process Complete!
echo ========================================
echo.
echo If the build was successful, you can:
echo   1. Download APK from the link shown above
echo   2. Or visit: https://expo.dev
echo   3. Transfer APK to your Android phone
echo   4. Install and enjoy!
echo.
pause
