# 🏎️ Steering Wheel Controller - Transform Your Phone into a Racing Wheel

A comprehensive cross-platform solution that converts your smartphone into a fully functional virtual steering wheel for PC racing games using accelerometer sensors and WebSocket communication.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation Guide](#-installation-guide)
- [How It Works](#-how-it-works)
- [Usage Instructions](#-usage-instructions)
- [Technical Documentation](#-technical-documentation)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Development & Building](#-development--building)
- [License](#-license)

---

## 🎯 Overview

This project consists of two main components working together to create a wireless steering wheel controller:

1. **Mobile Application (React Native)** - Captures real-time accelerometer data from your smartphone and transmits it wirelessly
2. **PC Server Application (Python)** - Receives sensor data and translates it into virtual joystick inputs for racing games

The system provides low-latency (<50ms) control with smooth steering response, making it suitable for casual racing game play over a local Wi-Fi network.

### 🎮 What It Does

- **Steering Control**: Tilt your phone left/right to steer the vehicle
- **Throttle/Gas**: Press the right button on screen to accelerate
- **Brake**: Press the left button on screen to brake
- **Real-time Feedback**: Visual indicators show current steering position and button states
- **Auto-orientation**: Screen automatically locks to landscape mode when connected

---

## 🏗️ System Architecture

```
┌─────────────────────────┐
│   Android/iOS Phone     │
│                         │
│  ┌──────────────────┐  │
│  │ React Native App │  │
│  │   (Expo)         │  │
│  ├──────────────────┤  │
│  │ Accelerometer    │  │
│  │ Sensor (50Hz)    │  │
│  └──────────────────┘  │
│          │              │
│    WebSocket (JSON)     │
│          ▼              │
└──────────│──────────────┘
           │
    Wi-Fi Network
    (Local LAN)
           │
           ▼
┌──────────────────────────┐
│      Windows PC          │
│                          │
│  ┌───────────────────┐  │
│  │ Python Server     │  │
│  │ (WebSocket)       │  │
│  ├───────────────────┤  │
│  │ pyvjoy Library    │  │
│  └───────────────────┘  │
│          │               │
│          ▼               │
│  ┌───────────────────┐  │
│  │ vJoy Driver       │  │
│  │ (Virtual Joystick)│  │
│  └───────────────────┘  │
│          │               │
│          ▼               │
│  ┌───────────────────┐  │
│  │  Racing Game      │  │
│  │  (DirectInput)    │  │
│  └───────────────────┘  │
└──────────────────────────┘
```

### Data Flow

1. **Sensor Reading**: Accelerometer captures phone orientation at 20Hz
2. **Data Packaging**: X, Y, Z axes + button states packed into JSON format
3. **Transmission**: WebSocket sends data every 50ms to PC server
4. **Processing**: Python server maps accelerometer values to joystick axes
5. **Virtual Input**: vJoy driver creates virtual gamepad recognized by Windows
6. **Game Control**: Racing game reads DirectInput from virtual controller

---

## ✨ Features

### Mobile App Features

- 📱 **Cross-platform**: Works on Android (via Expo/React Native)
- 🎯 **Real-time Sensor Data**: 20 updates per second for responsive control
- 🔄 **Auto-Reconnect**: Attempts to reconnect if connection drops
- 🌐 **Visual Feedback**: Live display of connection status and sensor values
- 📐 **Auto-Orientation**: Locks to landscape when connected for comfortable steering
- 🎨 **Intuitive UI**: Large, easy-to-press gas and brake buttons
- 🔒 **Stable Connection**: WebSocket protocol ensures reliable data transmission

### PC Server Features

- 🖥️ **Windows Compatible**: Runs on Windows 7/8/10/11
- ⚡ **Low Latency**: <50ms response time on local network
- 🎮 **vJoy Integration**: Creates virtual DirectInput-compatible joystick
- 🔧 **Auto-Configuration**: Detects and configures vJoy device automatically
- 📊 **Detailed Logging**: Real-time console output for debugging
- 🛡️ **Error Handling**: Comprehensive error checking and user guidance
- 🔒 **Admin Privilege Check**: Ensures proper permissions for driver access
- 🧪 **Built-in Testing**: Independent vJoy test mode for verification

### Control Mapping

- **X-Axis (vJoy)**: Steering (left/right tilt) - Full 16-bit range (32,767 steps)
- **Y-Axis (vJoy)**: Brake pedal (on-screen button) - Binary on/off
- **Z-Axis (vJoy)**: Gas/Throttle (on-screen button) - Binary on/off

---

## 📋 Prerequisites

### For PC (Windows)

1. **Operating System**

   - Windows 7 or later (64-bit recommended)
   - Administrator privileges required

2. **vJoy Virtual Joystick Driver**

   - Version 2.1.9 or later
   - Download: [https://sourceforge.net/projects/vjoystick/](https://sourceforge.net/projects/vjoystick/)

3. **Python 3.7+** (if running from source)

   - Not required if using pre-built `.exe` file

4. **Network**
   - Wi-Fi adapter or Ethernet connection
   - Firewall configured to allow port 5000

### For Mobile Device

1. **Android Device**

   - Android 6.0 or later
   - Accelerometer sensor (standard on all modern phones)
   - Wi-Fi capability

2. **Development Mode (Optional)**

   - Expo Go app from Google Play Store
   - For testing without building APK

3. **Network**
   - Must be on the same Wi-Fi network as PC

---

## 🚀 Installation Guide

### Step 1: PC Server Setup

#### Install vJoy Driver

1. Download vJoy installer from [GitHub Releases](https://github.com/njz3/vJoy/releases)
2. Run `vJoySetup.exe` **as Administrator**
3. Follow installation wizard
4. **Restart your computer** after installation

#### Configure vJoy Device

1. Open Start Menu → Search "Configure vJoy"
2. Select **Device 1**
3. Enable the following axes:
   - ✅ X-Axis (Steering)
   - ✅ Y-Axis (Brake)
   - ✅ Z-Axis (Gas)
4. Click **"Apply"** then **"OK"**

#### Verify vJoy Installation

1. Press `Win + R`
2. Type `joy.cpl` and press Enter
3. You should see "vJoy Device" in the list
4. Select it and click "Properties" to test

#### Run the Server

**Option A: Pre-built Executable (Recommended)**

```bash
cd PythonDesktopApp\dist
SteeringWheelServer.exe
```

**Option B: From Source**

```bash
cd PythonDesktopApp
pip install -r requirements.txt
python main.py
```

The server will start and display:

```
============================================================
🏎️  VIRTUAL STEERING WHEEL SERVER (vJoy)
============================================================
🌐 Server: 0.0.0.0:5000
🎮 Device: vJoy Device #1
⏳ Waiting for connection...
```

### Step 2: Mobile App Setup

#### Option 1: Quick Build with Expo (Production APK)

1. **Install Expo CLI globally**

   ```bash
   npm install -g eas-cli
   ```

2. **Navigate to mobile app folder**

   ```bash
   cd ReactNativeMobileApp
   ```

3. **Install dependencies**

   ```bash
   npm install
   ```

4. **Login to Expo** (create free account at expo.dev)

   ```bash
   eas login
   ```

5. **Build APK for Android**

   ```bash
   eas build -p android --profile preview
   ```

   - Build takes 10-15 minutes
   - Download link will be provided in terminal
   - Or visit [expo.dev](https://expo.dev) → Your account → Builds

6. **Install APK on Phone**
   - Transfer APK file to your phone
   - Enable "Install from unknown sources" in Android Settings
   - Open APK and install

#### Option 2: Development Mode (Instant Testing)

1. **Install Expo Go** from Google Play Store on your phone

2. **Install dependencies**

   ```bash
   cd ReactNativeMobileApp
   npm install
   ```

3. **Start development server**

   ```bash
   npx expo start
   ```

4. **Connect your phone**
   - Scan QR code with Expo Go app
   - App loads instantly (no build needed)

---

## 🔍 How It Works

### Mobile App Internals

**Sensor Management**

```javascript
// Accelerometer updates at 50ms intervals (20Hz)
Accelerometer.setUpdateInterval(50);

// Listener captures X, Y, Z acceleration
Accelerometer.addListener((data) => {
  const sensorData = {
    x: data.x, // Up/Down tilt
    y: data.y, // Left/Right tilt (STEERING)
    z: data.z, // Forward/Backward tilt
  };
});
```

**WebSocket Communication**

```javascript
// JSON payload sent every 50ms
{
  "x": -0.15,        // X-axis acceleration
  "y": 0.42,         // Y-axis acceleration (steering)
  "z": 0.87,         // Z-axis acceleration
  "gas": true,       // Gas button state
  "brake": false     // Brake button state
}
```

### PC Server Internals

**Data Processing Pipeline**

1. **Receive JSON data** via WebSocket
2. **Parse accelerometer values** (x, y, z)
3. **Map Y-axis to steering range**
   - Input: -1.0 (left) to +1.0 (right)
   - Output: 0x1 to 0x7FFF (vJoy 16-bit range)
4. **Apply button states**
   - Gas button → Z-Axis = 0x7FFF (max) or 0x1 (min)
   - Brake button → Y-Axis = 0x7FFF (max) or 0x1 (min)
5. **Send to vJoy driver** via pyvjoy library

**Axis Mapping Math**

```python
def map_to_axis(value, min_val=-1.0, max_val=1.0):
    # Clamp input
    value = max(min_val, min(max_val, value))

    # Normalize to 0.0-1.0
    normalized = (value - min_val) / (max_val - min_val)

    # Map to vJoy 16-bit range (1 to 32767)
    axis_value = int(0x1 + (normalized * (0x7FFF - 0x1)))

    return axis_value
```

**vJoy Axis Assignment**

- **X-Axis**: Steering wheel (left/right)
- **Y-Axis**: Brake pedal (binary on/off)
- **Z-Axis**: Gas/Throttle pedal (binary on/off)

---

## 📱 Usage Instructions

### 1. Start PC Server

1. Ensure vJoy is installed and configured
2. Run `SteeringWheelServer.exe` (or `python main.py`)
3. Note the IP address displayed or find it manually:
   - Open PowerShell: `ipconfig`
   - Look for "IPv4 Address" under your active network
   - Example: `192.168.1.251`

### 2. Connect Mobile App

1. Open the Steering Wheel app on your phone
2. Enter server URL: `ws://YOUR_PC_IP:5000`
   - Example: `ws://192.168.1.251:5000`
3. Tap **"Connect"**
4. Wait for "Connected" status (green indicator)

### 3. Calibrate and Test

1. **Hold phone horizontally** (landscape orientation)
2. Phone should auto-rotate to landscape mode
3. Test steering:
   - Tilt left → Steering goes left
   - Tilt right → Steering goes right
   - Center position → Wheels straight
4. Test buttons:
   - Press **RIGHT (green)** → Gas pedal
   - Press **LEFT (red)** → Brake pedal

### 4. Configure Racing Game

1. Open your racing game's controller settings
2. Look for "vJoy Device" in controller list
3. Assign controls:
   - **Steering** → X-Axis
   - **Throttle/Gas** → Z-Axis (or Z-Rotation)
   - **Brake** → Y-Axis (or Y-Rotation)
4. Test in-game to verify functionality

### 5. Start Racing!

- Hold phone like a steering wheel (landscape orientation)
- Tilt left/right to steer
- Use on-screen buttons for gas and brake
- To disconnect: Tap **"✕ Disconnect"** button at top

---

## 📊 Technical Documentation

### Communication Protocol

**WebSocket Connection**

- Protocol: `ws://` (WebSocket)
- Port: `5000` (default, configurable)
- Format: JSON
- Update Rate: 20 messages/second (50ms interval)

**Message Structure**

```json
{
  "x": <float>,      // X-axis acceleration (-1.0 to 1.0)
  "y": <float>,      // Y-axis acceleration (-1.0 to 1.0) - STEERING
  "z": <float>,      // Z-axis acceleration (-1.0 to 1.0)
  "gas": <boolean>,  // Gas button pressed (true/false)
  "brake": <boolean> // Brake button pressed (true/false)
}
```

### Performance Metrics

| Metric              | Value         | Notes                               |
| ------------------- | ------------- | ----------------------------------- |
| Update Rate         | 20 Hz         | Configurable in app (50ms interval) |
| Network Latency     | 5-20ms        | On local Wi-Fi                      |
| Processing Delay    | <5ms          | Server-side processing              |
| Total Latency       | <50ms         | End-to-end (sensor to game)         |
| Steering Resolution | 16-bit        | 32,767 discrete positions           |
| Axis Range          | 0x1 to 0x7FFF | vJoy standard range                 |

### Technology Stack

**Mobile Application**

- **Framework**: React Native 0.74.0
- **Runtime**: Expo SDK 51.0.0
- **Sensors**: expo-sensors 13.0.0
- **Orientation**: expo-screen-orientation
- **Language**: JavaScript (ES6+)

**PC Server**

- **Language**: Python 3.7+
- **Async I/O**: asyncio, websockets
- **Virtual Driver**: pyvjoy (vJoy wrapper)
- **Platform**: Windows (vJoy dependency)

**Dependencies**

```python
# Python (requirements.txt)
websockets>=10.0
pyvjoy>=1.0.3
```

```json
// React Native (package.json)
{
  "expo": "~51.0.0",
  "expo-sensors": "~13.0.0",
  "expo-screen-orientation": "~7.0.0",
  "react": "18.2.0",
  "react-native": "0.74.0"
}
```

---

## 📁 Project Structure

```
SteeringWheel/
│
├── README.md                           # This file
│
├── PythonDesktopApp/                   # PC Server Application
│   ├── main.py                         # Main server script
│   ├── requirements.txt                # Python dependencies
│   ├── SteeringWheelServer.spec        # PyInstaller spec file
│   ├── build_exe.bat                   # Build script for executable
│   ├── check_firewall.bat              # Firewall configuration helper
│   ├── test_server.py                  # Server testing utilities
│   │
│   ├── build/                          # Build artifacts (intermediate)
│   │   └── SteeringWheelServer/
│   │       ├── Analysis-00.toc
│   │       ├── base_library.zip
│   │       ├── EXE-00.toc
│   │       └── ...
│   │
│   └── dist/                           # Compiled executable
│       └── SteeringWheelServer.exe     # ⭐ Run this on PC!
│
└── ReactNativeMobileApp/               # Mobile Application
    ├── App.js                          # Main React Native component
    ├── package.json                    # npm dependencies
    ├── app.json                        # Expo configuration
    ├── babel.config.js                 # Babel transpiler config
    ├── eas.json                        # EAS Build configuration
    ├── build-apk.bat                   # Quick build script
    │
    └── server/                         # Test server examples
        ├── server.py                   # Basic WebSocket test server
        ├── server_advanced.py          # Advanced testing server
        └── requirements.txt            # Python dependencies for test server
```

### Key Files Explained

**`PythonDesktopApp/main.py`**

- Main server application (850+ lines)
- WebSocket server implementation
- vJoy device management
- Accelerometer data processing
- Error handling and logging
- Admin privilege checking
- Built-in diagnostics

**`ReactNativeMobileApp/App.js`**

- Complete mobile app (700+ lines)
- WebSocket client
- Accelerometer sensor management
- UI components (connection, steering)
- State management
- Auto-orientation control

**`PythonDesktopApp/dist/SteeringWheelServer.exe`**

- Standalone executable (no Python installation needed)
- Built with PyInstaller
- Includes all dependencies
- Ready to run on any Windows PC

---

## 🔧 Troubleshooting

### Connection Issues

#### ❌ "Connection Failed" on Mobile App

**Symptoms**: App shows "Connection Failed" or "Disconnected"

**Solutions**:

1. ✅ Verify PC server is running (green text in console)
2. ✅ Check both devices on **same Wi-Fi network**
   - PC: Settings → Network → Wi-Fi
   - Phone: Settings → Wi-Fi
3. ✅ Verify correct IP address
   - PC: Run `ipconfig` in PowerShell
   - Use format: `ws://192.168.x.x:5000` (not https://)
4. ✅ Check Windows Firewall
   ```powershell
   # Run as Administrator
   cd PythonDesktopApp
   check_firewall.bat
   ```
5. ✅ Try disabling firewall temporarily to test
6. ✅ Ensure port 5000 is not used by another application

#### ❌ Server Won't Start

**Error**: "vJoy driver is not enabled!"

**Solutions**:

1. Install vJoy from [GitHub](https://github.com/njz3/vJoy/releases)
2. Restart computer after installation
3. Open "Configure vJoy" → Enable Device 1
4. Run server as Administrator

**Error**: "Port 5000 already in use"

**Solutions**:

1. Close other applications using port 5000
2. Check for other running instances:
   ```powershell
   netstat -ano | findstr :5000
   ```
3. Kill process if found:
   ```powershell
   taskkill /PID <process_id> /F
   ```

### vJoy Issues

#### ❌ "Device is busy" or "Cannot acquire device"

**Solutions**:

1. Close "Game Controllers" (joy.cpl) if open
2. Close other applications using vJoy
3. Restart the server application
4. Worst case: Restart Windows

#### ❌ Steering Not Working in Game

**Solutions**:

1. Open `joy.cpl` (Win+R → joy.cpl)
2. Select "vJoy Device" → Properties
3. Verify axes move when tilting phone
4. In game settings:
   - Select "vJoy Device" as controller
   - Map steering to X-Axis
   - Map throttle to Z-Axis
   - Map brake to Y-Axis
5. Some games require:
   - Controller calibration in-game
   - Deadzone adjustment
   - Sensitivity tweaking

#### ❌ Axes Not Available

**Error**: "X-Axis not available"

**Solutions**:

1. Open "Configure vJoy"
2. Select Device 1
3. Check these axes:
   - ✅ X-Axis
   - ✅ Y-Axis
   - ✅ Z-Axis
4. Click "Apply" → "OK"
5. Restart server

### Mobile App Issues

#### ❌ Accelerometer Not Responding

**Solutions**:

1. Ensure phone has accelerometer (all modern phones do)
2. Grant sensor permissions if prompted
3. Restart the app
4. Test with phone's built-in level/compass app

#### ❌ Screen Won't Rotate

**Solutions**:

1. Enable auto-rotate in phone settings
2. Unlock screen orientation
3. Reconnect to server (triggers orientation lock)

#### ❌ Buttons Not Working

**Solutions**:

1. Make sure you're pressing within button area
2. Check server console for "GAS" or "BRAKE" messages
3. Verify in joy.cpl that buttons/axes respond

### Network Debugging

#### Find PC IP Address

**Windows (PowerShell)**:

```powershell
ipconfig
```

Look for "IPv4 Address" under your active adapter (Wi-Fi or Ethernet)

#### Find Phone IP Address

**Android**:

1. Settings → Wi-Fi
2. Tap on connected network
3. Look for "IP address"

#### Verify Connectivity

```powershell
# On PC, ping phone (if you know phone's IP)
ping <phone_ip>

# Check if server is listening
netstat -an | findstr :5000
```

### Performance Issues

#### Laggy or Delayed Response

**Solutions**:

1. Ensure strong Wi-Fi signal (both devices near router)
2. Close background apps on phone
3. Close unnecessary programs on PC
4. Check server console for error messages
5. Reduce update rate in App.js if needed:
   ```javascript
   // Change from 50ms to 100ms
   Accelerometer.setUpdateInterval(100);
   ```

---

## 🛠️ Development & Building

### Building PC Server Executable

**Requirements**:

- Python 3.7+
- PyInstaller

**Steps**:

```bash
cd PythonDesktopApp
pip install -r requirements.txt
pip install pyinstaller

# Build with batch file (Windows)
build_exe.bat

# Or manually with PyInstaller
pyinstaller --onefile --console --name "SteeringWheelServer" main.py
```

**Output**: `dist/SteeringWheelServer.exe`

### Building Mobile APK

**Method 1: EAS Build (Cloud)**

```bash
cd ReactNativeMobileApp
npm install
eas login
eas build -p android --profile preview
```

**Method 2: Local Build (Advanced)**

```bash
cd ReactNativeMobileApp
npm install
npx expo prebuild
cd android
./gradlew assembleRelease
```

**Output**: APK file in `android/app/build/outputs/apk/`

### Running Development Server

**PC Server**:

```bash
cd PythonDesktopApp
python main.py
```

**Mobile App**:

```bash
cd ReactNativeMobileApp
npm install
npx expo start
```

Then scan QR code with Expo Go app

### Testing

**Test vJoy Independently**:

```bash
cd PythonDesktopApp
python main.py
# Select option 2 when prompted
```

**Test WebSocket Server**:

```bash
cd ReactNativeMobileApp/server
pip install websockets
python server.py
```

### Customization

**Change Server Port**:

```python
# In main.py
bridge = SteeringWheelBridge(
    host='0.0.0.0',
    port=8080,  # Change this
    vjoy_device_id=1
)
```

**Adjust Steering Sensitivity**:

```python
# In main.py, modify map_to_axis function
# Or apply multiplier to Y-axis value
y_adjusted = y * 1.5  # Increase sensitivity
```

**Change Update Rate**:

```javascript
// In App.js
Accelerometer.setUpdateInterval(100); // Slower (10 Hz)
// Or
Accelerometer.setUpdateInterval(20); // Faster (50 Hz)
```

---

## 📜 License

**MIT License**

Copyright (c) 2025 Steering Wheel Controller Project

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 🙋 Support & FAQ

**Q: Does this work with all racing games?**
A: It works with games that support DirectInput controllers (most PC racing games). Games using XInput may require additional mapping software like x360ce.

**Q: Can I use this wirelessly?**
A: Yes! It uses Wi-Fi for wireless communication. Both devices must be on the same network.

**Q: What's the input lag?**
A: Typically <50ms on a good local Wi-Fi connection, which is acceptable for casual racing.

**Q: Can I use multiple phones?**
A: Current version supports one phone at a time. Multiple connections would require server modifications.

**Q: Does it work on iOS?**
A: The React Native app can be built for iOS with minor modifications, but it's primarily tested on Android.

**Q: Do I need to keep the server window open?**
A: Yes, the server console must remain running while playing.

**Q: Can I customize button mappings?**
A: Yes, modify the axis assignments in `main.py` (vJoy axes) and configure game controller settings accordingly.

---

## 📞 Contact & Links

- **GitHub Repository**: [SteeringWheel](https://github.com/enesmuzaffer22/SteeringWheel)
- **vJoy Driver**: [https://sourceforge.net/projects/vjoystick/](https://sourceforge.net/projects/vjoystick/)
- **Expo Documentation**: [https://docs.expo.dev](https://docs.expo.dev)
- **React Native**: [https://reactnative.dev](https://reactnative.dev)

---

**Made with ❤️ for racing game enthusiasts! 🏎️💨**

_Transform your smartphone into a racing wheel and enjoy the thrill of mobile-controlled PC gaming!_
