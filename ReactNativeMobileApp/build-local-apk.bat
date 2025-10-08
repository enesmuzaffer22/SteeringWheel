@echo off
echo ========================================
echo   Quick Local APK Builder
echo ========================================
echo.
echo This script will build APK locally (NO QUEUE!)
echo.
echo ONE-TIME SETUP REQUIRED:
echo 1. Install Android Studio from: https://developer.android.com/studio
echo 2. During installation, make sure to install:
echo    - Android SDK
echo    - Android SDK Platform
echo    - Android Virtual Device (optional)
echo.
echo After Android Studio installation:
echo 3. Open Android Studio
echo 4. Go to: More Actions ^> SDK Manager
echo 5. Install: Android 13.0 (API 33)
echo.
pause

echo.
echo Checking for Android SDK...
if not exist "%LOCALAPPDATA%\Android\Sdk" (
    echo ERROR: Android SDK not found!
    echo Please install Android Studio first.
    echo Download: https://developer.android.com/studio
    pause
    exit /b 1
)

echo Android SDK found!
echo.

echo Setting environment variables...
set ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk
set PATH=%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%PATH%

echo.
echo Step 1: Generating Android project...
call npx expo prebuild --platform android --clean
if %errorlevel% neq 0 (
    echo ERROR: Prebuild failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Building APK...
cd android
call gradlew.bat assembleRelease
if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD SUCCESSFUL!
echo ========================================
echo.
echo APK Location:
echo android\app\build\outputs\apk\release\app-release.apk
echo.
echo You can now:
echo 1. Copy this APK to your phone
echo 2. Install and test!
echo.
echo Build time: ~2-5 minutes (no queue!)
echo.
pause

:: Open the folder containing the APK
explorer android\app\build\outputs\apk\release

cd ..
