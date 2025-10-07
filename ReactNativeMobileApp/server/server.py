"""
Simple WebSocket Server for Steering Wheel Controller
Receives gyroscope data from the React Native mobile app
"""

import asyncio
import websockets
import json
from datetime import datetime

async def handle_client(websocket, path):
    """Handle incoming WebSocket connections"""
    client_address = websocket.remote_address
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Client connected: {client_address}")
    
    try:
        async for message in websocket:
            try:
                # Parse the JSON data
                data = json.loads(message)
                x = data.get('x', 0)
                y = data.get('y', 0)
                z = data.get('z', 0)
                
                # Print the gyroscope data
                print(f"Gyro → X: {x:6.3f} | Y: {y:6.3f} | Z: {z:6.3f}")
                
                # Here you can add your game control logic
                # For example:
                # - Use 'y' for steering left/right
                # - Use 'x' for acceleration/braking
                # - Use 'z' for other controls
                
                # Optional: Send acknowledgment back to client
                # await websocket.send(json.dumps({"status": "received"}))
                
            except json.JSONDecodeError:
                print(f"Invalid JSON received: {message}")
            except Exception as e:
                print(f"Error processing message: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Client disconnected: {client_address}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    """Start the WebSocket server"""
    host = "0.0.0.0"  # Listen on all network interfaces
    port = 5000
    
    print("=" * 60)
    print("🎮 Steering Wheel WebSocket Server")
    print("=" * 60)
    print(f"Server starting on ws://{host}:{port}")
    print("\n📱 To connect from your mobile app:")
    print("   1. Make sure your phone and PC are on the same Wi-Fi")
    print("   2. Find your PC's IP address:")
    print("      - Windows: Run 'ipconfig' in PowerShell")
    print("      - Mac/Linux: Run 'ifconfig' or 'ip addr'")
    print("   3. Enter ws://YOUR_PC_IP:5000 in the mobile app")
    print("\n⌨️  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
