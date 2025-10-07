# 🚀 Quick Start Guide

## Step 1: Install Dependencies

Open PowerShell in this directory and run:

```powershell
npm install
```

## Step 2: Start the Mobile App

```powershell
npx expo start
```

This will show a QR code. Scan it with:

- **Android**: Expo Go app
- **iOS**: Camera app (will open in Expo Go)

## Step 3: Start the WebSocket Server

Open a **new** PowerShell window and run:

```powershell
cd server
pip install websockets
python server.py
```

## Step 4: Find Your PC's IP Address

In PowerShell, run:

```powershell
ipconfig
```

Look for "IPv4 Address" (e.g., `192.168.1.42`)

## Step 5: Connect from Your Phone

1. Open the app on your phone
2. Enter: `ws://YOUR_PC_IP:5000` (replace with your actual IP)
3. Press "Connect"
4. Start tilting your phone! 🎮

## 📝 Example

If your PC's IP is `192.168.1.42`, enter:

```
ws://192.168.1.42:5000
```

## 🐛 Troubleshooting

### "Connection Failed"

- ✅ Both devices on same Wi-Fi?
- ✅ Server running on PC?
- ✅ Firewall allowing port 5000?
- ✅ Correct IP address?

### "No Gyroscope Data"

- ✅ Phone has gyroscope sensor?
- ✅ App has sensor permissions?

### Enable Windows Firewall Rule (if needed)

```powershell
New-NetFirewallRule -DisplayName "WebSocket Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

## 📊 What You Should See

**On your phone:**

- Status: "Connected" (green dot)
- Live X, Y, Z values updating
- "📡 Sending data every ~50ms"

**On your PC (server terminal):**

```
Gyro → X:  0.123 | Y: -0.456 | Z:  0.789
Gyro → X:  0.125 | Y: -0.450 | Z:  0.791
...
```

## 🎮 Next Steps

Now you can integrate this data with your racing game! Check out `server_advanced.py` for examples of:

- Processing gyro data for game controls
- Simulating keyboard/gamepad input
- Custom sensitivity settings

Happy racing! 🏎️💨
