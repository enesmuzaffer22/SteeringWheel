# 🏎️ vJoy Steering Wheel Test Guide

## 📋 Prerequisites

Before testing, ensure:

1. ✅ vJoy driver installed (see VJOY_INSTALLATION.md)
2. ✅ Python packages installed: `pip install -r requirements.txt`
3. ✅ vJoy Device 1 configured with X, Y, Z axes enabled
4. ✅ React Native mobile app ready on your phone

---

## 🔍 Step 1: Verify vJoy Installation

### Check vJoy Driver:

1. Press **Windows + R**
2. Type: `joy.cpl`
3. Press Enter
4. You should see **"vJoy Device"** in the list

### Configure vJoy Device:

1. Open **"Configure vJoy"** from Start Menu
2. Select **Device 1**
3. Ensure these are checked:
   - ✅ **Enable vJoy Device**
   - ✅ **X-Axis**
   - ✅ **Y-Axis**
   - ✅ **Z-Axis**
4. Click **Apply**

---

## 🚀 Step 2: Start Python Server

### Run the Server:

```bash
cd PythonDesktopApp
python main.py
```

### Expected Output:

```
======================================================================
🏎️  VIRTUAL STEERING WHEEL SERVER (vJoy)
======================================================================
🌐 Server: 0.0.0.0:5000
🎮 Device: vJoy Device #1

🎮 Steering Wheel Mapping:
   • Y-axis (tilt L/R) → X-AXIS (steering)
   • Gas button       → Y-AXIS (throttle)
   • Brake button     → Z-AXIS (brake)

🎯 Precision:
   • 16-bit resolution (0-32768)
   • Analog steering: -100% to +100%
   • Digital gas/brake: 0% or 100%

📱 Phone Setup:
   1. Open React Native app
   2. Enter: ws://YOUR_PC_IP:5000
   3. Hold phone HORIZONTAL (landscape)

🔧 Verify vJoy:
   Windows + R → joy.cpl → 'vJoy Device' should be listed

======================================================================
⏳ Waiting for connection...
```

---

## 📱 Step 3: Connect Mobile App

### On Your Phone:

1. Open the React Native app
2. Enter WebSocket URL: `ws://YOUR_PC_IP:5000`
   - Replace `YOUR_PC_IP` with your PC's local IP (e.g., `192.168.1.100`)
3. Tap **"Connect"**
4. Phone should automatically rotate to **landscape mode**

### Expected Server Output:

```
✅ [CONNECTED] Client at 192.168.1.XXX
```

---

## 🎮 Step 4: Test Steering Controls

### Test Steering (Y-Axis Tilt):

1. Hold phone **horizontally** (landscape)
2. **Tilt LEFT** → Should see: `[WHEEL] y=-0.XX (-XX%) → LEFT ⬅️`
3. **Tilt RIGHT** → Should see: `[WHEEL] y=+0.XX (+XX%) → RIGHT ➡️`
4. **Center** → Should see: `[WHEEL] y=+0.0X (+X%) → CENTER ⬆️`

### Test Gas Button:

1. Press **GAS** (right side button on screen)
2. Should see: `[WHEEL] y=+0.XX (+XX%) → CENTER ⬆️ 🟢 GAS`

### Test Brake Button:

1. Press **BRAKE** (left side button on screen)
2. Should see: `[WHEEL] y=+0.XX (+XX%) → CENTER ⬆️ 🔴 BRAKE`

### Test Combined Input:

1. Tilt phone **LEFT** while pressing **GAS**
2. Should see: `[WHEEL] y=-0.XX (-XX%) → LEFT ⬅️ 🟢 GAS`

---

## 🕹️ Step 5: Verify in Windows Game Controllers

### Open Game Controllers Panel:

1. Press **Windows + R**
2. Type: `joy.cpl`
3. Press Enter
4. Select **"vJoy Device"**
5. Click **"Properties"**

### Test Axes:

- **X-Axis (Steering)**: Tilt phone LEFT/RIGHT → Slider should move
- **Y-Axis (Gas)**: Press GAS button → Slider should jump to max
- **Z-Axis (Brake)**: Press BRAKE button → Slider should jump to max

### Visual Confirmation:

- Crosshair should move as you tilt phone
- Sliders should respond to button presses

---

## 🏁 Step 6: Test in a Racing Game

### Recommended Games:

- **Assetto Corsa**
- **Forza Horizon 5**
- **BeamNG.drive**
- **Project CARS**

### Game Configuration:

1. Open game settings → **Controls**
2. Select **"Steering Wheel"** or **"Custom"**
3. Assign:
   - **Steering** → X-Axis
   - **Throttle** → Y-Axis
   - **Brake** → Z-Axis
4. Set **deadzone** to ~5% (adjust as needed)
5. Disable **steering assist** for better feel

### Test Drive:

1. Start a race or free drive
2. Tilt phone LEFT/RIGHT → Car should steer smoothly
3. Press GAS → Car should accelerate
4. Press BRAKE → Car should slow down
5. Release buttons → Car should coast

---

## 🐛 Troubleshooting

### Problem: Server says "vJoy not installed"

**Solution:**

1. Download vJoy from: https://github.com/njz3/vJoy/releases
2. Install `vJoySetup.exe` as Administrator
3. Restart computer
4. Run: `pip install pyvjoy`

### Problem: "Failed to initialize vJoy Device"

**Solution:**

1. Open **"Configure vJoy"** from Start Menu
2. Enable Device 1
3. Enable X, Y, Z axes
4. Click **Apply**
5. Restart Python server

### Problem: No axes movement in joy.cpl

**Solution:**

1. Check server logs for steering data
2. Verify phone is in **landscape mode**
3. Ensure WebSocket connection is active (green indicator in app)
4. Try tilting phone more aggressively

### Problem: Game doesn't detect steering wheel

**Solution:**

1. Make sure vJoy Device is visible in `joy.cpl`
2. Some games require **restart** to detect new controllers
3. Check game settings for **"Steering Wheel"** input mode
4. Try **calibrating** controller in game settings

### Problem: Steering is inverted

**Solution:**

- In game settings, look for **"Invert Steering"** option
- Or modify `map_to_axis()` in `main.py`:
  ```python
  steering_value = self.map_to_axis(-y, -1.0, 1.0)  # Add minus sign
  ```

### Problem: Steering is too sensitive/not sensitive enough

**Solution:**

1. Adjust **deadzone** in game settings (5-15%)
2. Adjust **sensitivity** in game settings (50-150%)
3. Or modify mapping in `main.py`:

   ```python
   # For less sensitivity:
   y = y * 0.7  # Reduce to 70%

   # For more sensitivity:
   y = y * 1.5  # Increase by 50%
   ```

---

## 📊 Performance Tips

### Reduce Latency:

1. Use **WiFi 5GHz** instead of 2.4GHz (if available)
2. Keep phone **close to router**
3. Close background apps on phone
4. Use **wired connection** for PC (not WiFi)

### Improve Smoothness:

1. Increase accelerometer update rate in React Native app
2. Reduce other network traffic
3. Close unnecessary programs on PC

### Battery Saving:

1. **Plug in phone** during long sessions (screen + WiFi drain battery)
2. Reduce screen brightness
3. Enable **battery saver mode** when not gaming

---

## ✅ Success Checklist

- [ ] vJoy driver installed and Device 1 configured
- [ ] Python server starts without errors
- [ ] Mobile app connects successfully
- [ ] Phone rotates to landscape automatically
- [ ] Server logs show steering data
- [ ] joy.cpl shows vJoy Device with moving axes
- [ ] Game detects steering wheel input
- [ ] Steering, gas, and brake all work in game

---

## 🎯 Next Steps

Once everything works:

1. **Fine-tune** sensitivity in game settings
2. **Calibrate** steering wheel in game
3. **Practice** driving to get used to the feel
4. **Enjoy** your DIY steering wheel!

---

## 📝 Notes

### Axis Mapping:

- **Phone Y-axis** (tilt L/R) → **vJoy X-axis** (steering)
- **Gas button** → **vJoy Y-axis** (throttle)
- **Brake button** → **vJoy Z-axis** (brake)

### Precision:

- vJoy uses **16-bit resolution** (0-32768 values)
- Steering: **analog** (-100% to +100%)
- Gas/Brake: **digital** (0% or 100%)

### Limitations:

- No force feedback (phone can't vibrate based on game)
- No clutch pedal (only 2 buttons available)
- No shifter paddles (could be added with more buttons)

---

**Happy Racing! 🏎️💨**
