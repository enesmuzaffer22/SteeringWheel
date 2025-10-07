# 🎮 Gyroscope to Keyboard Bridge

A Python desktop application that receives gyroscope data from a mobile device via WebSocket and translates it into real-time keyboard inputs for PC racing games.

## 🚀 Features

- ✅ WebSocket server listening on all network interfaces
- ✅ Real-time gyroscope data processing (30-50ms response time)
- ✅ Smooth keyboard input simulation (Left/Right arrows)
- ✅ Non-blocking async I/O for low CPU usage
- ✅ Graceful connection handling and cleanup
- ✅ Detailed console logging for debugging
- ✅ State management to avoid key press spam

## 📋 Requirements

- Python 3.7 or higher
- Windows/Linux/macOS
- Administrator/root privileges (required for keyboard control)

## 🛠️ Installation

1. **Clone or download this repository**

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or manually:

   ```bash
   pip install websockets keyboard
   ```

## ▶️ Usage

### Start the Server

**On Windows (run as Administrator):**

```bash
python main.py
```

**On Linux/macOS (run with sudo):**

```bash
sudo python main.py
```

The server will start on `0.0.0.0:5000` and wait for connections.

### Expected Output

```
============================================================
🎮 Gyroscope to Keyboard Bridge Server
============================================================
🌐 Starting server on 0.0.0.0:5000
📊 Steering threshold: ±0.2
⌨️  Key mapping: x > 0.2 = RIGHT, x < -0.2 = LEFT
============================================================
⏳ Waiting for client connection...
```

### When Client Connects

```
[12:34:56] ✅ [CONNECTED] Client at 192.168.1.50
[12:34:56] [DATA] x=-0.34 y=0.05 z=0.72 → TURN LEFT ⬅️
[12:34:57] [DATA] x=+0.45 y=-0.02 z=0.61 → TURN RIGHT ➡️
[12:34:58] [DATA] x=+0.05 y=0.01 z=0.80 → CENTER ⬆️
[12:34:58] 🔓 Released RIGHT arrow
```

## 📡 Mobile Client

Your mobile app should connect to the server's IP address and send JSON messages in this format:

```json
{
  "x": -0.12,
  "y": 0.03,
  "z": 0.78
}
```

**WebSocket URL:** `ws://<SERVER_IP>:5000`

Example: `ws://192.168.1.100:5000`

## ⚙️ Configuration

You can modify these parameters in `main.py`:

```python
bridge = GyroKeyboardBridge(
    host='0.0.0.0',    # Listen on all interfaces
    port=5000,         # Server port
    threshold=0.2      # Steering sensitivity (lower = more sensitive)
)
```

## 🎮 Steering Logic

- **x > +0.2** → Press and hold **Right Arrow** ➡️
- **x < -0.2** → Press and hold **Left Arrow** ⬅️
- **-0.2 ≤ x ≤ +0.2** → Release both keys (center position) ⬆️

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal to gracefully stop the server.

## 🐛 Troubleshooting

### "Permission denied" error

- Run the script with administrator/sudo privileges
- The `keyboard` library requires elevated permissions

### "Connection refused" from mobile

- Check that both devices are on the same network
- Verify the server IP address (`ipconfig` on Windows, `ifconfig` on Linux/macOS)
- Make sure port 5000 is not blocked by firewall

### Keys not responding

- Ensure the racing game window is in focus
- Try adjusting the threshold value for better sensitivity
- Check console logs for data reception

## 📝 License

Free to use and modify for personal projects.

## 🤝 Contributing

Feel free to submit issues or pull requests!
