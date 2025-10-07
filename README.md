# 🎮 Steering Wheel Controller - Quick Start Guide

A mobile app that turns your phone into a virtual steering wheel for PC racing games.

## 📱 Getting the App on Your Phone

### Option 1: Quick Build with Expo (Recommended)

1. **Install EAS CLI:**

   ```bash
   npm install -g eas-cli
   ```

2. **Login to Expo** (create free account at expo.dev if needed):

   ```bash
   cd ReactNativeMobileApp
   eas login
   ```

3. **Build APK:**

   ```bash
   eas build -p android --profile preview
   ```

   ⏱️ Wait 10-15 minutes for cloud build to complete

   📥 Download APK from the link provided or from expo.dev

4. **Install APK:**
   - Transfer APK to your phone
   - Enable "Install from unknown sources" in Android settings
   - Open APK file and install

### Option 2: Development Mode (No Build Needed)

1. **Install Expo Go** from Google Play Store

2. **Start development server:**

   ```bash
   cd ReactNativeMobileApp
   npx expo start
   ```

3. **Scan QR code** with Expo Go app

4. **App runs instantly!**

## 🖥️ PC Setup

1. **Install vJoy Driver:**

   - Download from: https://github.com/njz3/vJoy/releases
   - Run vJoySetup.exe as Administrator
   - Restart computer
   - Open "Configure vJoy" from Start menu
   - Enable Device 1
   - Enable X-Axis, Y-Axis, Z-Axis
   - Click "Apply"

2. **Run Server:**
   - Navigate to `PythonDesktopApp/dist/`
   - Double-click `SteeringWheelServer.exe`
   - Follow on-screen instructions

## 🎯 How to Use

1. **Start the server** on your PC (SteeringWheelServer.exe)

2. **Find your PC's IP address:**

   - Open PowerShell on PC
   - Type: `ipconfig`
   - Look for "IPv4 Address" (e.g., 192.168.1.251)

3. **Connect from phone:**

   - Open the app
   - Enter: `ws://YOUR_PC_IP:5000`
   - Click "Connect"

4. **Start driving:**
   - Hold phone horizontally like a steering wheel
   - Tilt left/right to steer
   - Use LEFT button for BRAKE
   - Use RIGHT button for GAS

## ⚠️ Important Notes

- Both devices must be on the same Wi-Fi network
- PC server must be running before connecting
- Hold phone in landscape orientation when connected
- Server runs on port 5000 by default

## 🔧 Troubleshooting

**"Connection Failed"**

- Make sure server is running on PC
- Check both devices are on same Wi-Fi
- Verify IP address is correct
- Try disabling Windows Firewall temporarily

**"vJoy not working"**

- Make sure vJoy driver is installed
- Enable X, Y, Z axes in Configure vJoy
- Restart computer after installation
- Run server as Administrator

**"App won't install"**

- Enable "Install from unknown sources" in Android settings
- Make sure APK download is complete
- Try different file transfer method

## 📁 Project Structure

```
SteeringWheel/
├── PythonDesktopApp/          # PC Server
│   ├── dist/
│   │   └── SteeringWheelServer.exe  # Run this!
│   └── main.py                # Source code
│
└── ReactNativeMobileApp/      # Mobile App
    ├── App.js                 # Main app code
    ├── eas.json              # Build configuration
    └── BUILD_APK_INSTRUCTIONS.md  # Detailed build guide
```

## 🎮 Controls

| Action       | Control                          |
| ------------ | -------------------------------- |
| Steering     | Tilt phone left/right            |
| Gas/Throttle | Press RIGHT button               |
| Brake        | Press LEFT button                |
| Disconnect   | Press "Disconnect" button at top |

## 📊 Technical Details

- **Server:** Python WebSocket (port 5000)
- **Mobile:** React Native + Expo
- **Virtual Controller:** vJoy (Windows driver)
- **Data Rate:** ~20 updates per second
- **Latency:** <50ms on local Wi-Fi

## 🚀 Building from Source

See detailed instructions in:

- PC Server: Run `pyinstaller --onefile --console --name "SteeringWheelServer" main.py`
- Mobile App: See `BUILD_APK_INSTRUCTIONS.md`

## 📝 License

MIT License - Feel free to use and modify!

## 🙋 Support

For issues or questions:

1. Check troubleshooting section above
2. Make sure all prerequisites are installed
3. Verify network connectivity
4. Check Windows Firewall settings

---

**Made with ❤️ for racing game enthusiasts! 🏎️**
