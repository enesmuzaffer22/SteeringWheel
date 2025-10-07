# 🎮 Steering Wheel Controller - React Native App

A React Native (Expo) mobile app that turns your phone into a steering wheel controller for racing games using the gyroscope sensor.

## 🚀 Features

- **Real-time Gyroscope Data**: Continuously reads x, y, z rotation values from your phone's gyroscope
- **WebSocket Communication**: Sends motion data to a PC server every ~50ms
- **Auto-Reconnect**: Automatically attempts to reconnect if connection drops
- **Live Feedback**: Displays connection status and current gyroscope values
- **Clean UI**: Simple, dark-themed interface optimized for mobile

## 📋 Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI
- Expo Go app on your phone (iOS/Android)

## 🛠️ Installation

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Start the Expo development server**:

   ```bash
   npx expo start
   ```

3. **Run on your device**:
   - Scan the QR code with Expo Go (Android) or Camera app (iOS)
   - Make sure your phone and PC are on the same Wi-Fi network

## 📱 Usage

1. **Enter WebSocket Server URL**:

   - Format: `ws://YOUR_PC_IP:PORT`
   - Example: `ws://192.168.1.42:5000`

2. **Press Connect**: The app will establish a WebSocket connection

3. **When Connected**:

   - Gyroscope starts reading motion data
   - Data is sent to the server every ~50ms
   - You'll see live x, y, z values on screen

4. **Control Your Game**: Tilt your phone to steer!

## 📊 Data Format

The app sends JSON data in this format:

```json
{
  "x": -0.34,
  "y": 0.08,
  "z": 0.55
}
```

## 🔧 Configuration

- **Update Interval**: Currently set to 50ms (20 updates/sec)
- **Server URL**: Configurable via the UI
- **Auto-reconnect**: Enabled by default with 2-second delay

## 🖥️ WebSocket Server Example

You'll need a WebSocket server running on your PC. Here's a simple Python example:

```python
import asyncio
import websockets
import json

async def handle_client(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Gyro data - X: {data['x']}, Y: {data['y']}, Z: {data['z']}")
            # Use this data to control your game
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 5000):
        print("WebSocket server started on ws://0.0.0.0:5000")
        await asyncio.Future()

asyncio.run(main())
```

## 📂 Project Structure

```
.
├── App.js              # Main application component
├── package.json        # Dependencies and scripts
├── app.json           # Expo configuration
├── babel.config.js    # Babel configuration
└── README.md          # This file
```

## 🎯 Key Components

- **WebSocket Management**: Handles connection, reconnection, and data transmission
- **Gyroscope Sensor**: Uses `expo-sensors` to read device motion
- **UI Components**: Status indicators, data display, and connection controls

## 🐛 Troubleshooting

- **Connection Failed**: Ensure both devices are on the same Wi-Fi network
- **No Gyroscope Data**: Check if your device has a gyroscope sensor
- **Reconnection Issues**: Verify the WebSocket server is running and accessible

## 📦 Dependencies

- `expo`: ~51.0.0
- `expo-sensors`: ~13.0.0
- `react`: 18.2.0
- `react-native`: 0.74.0

## 📝 License

MIT

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
