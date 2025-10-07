"""
Advanced WebSocket Server with Game Control Integration
Demonstrates how to use gyroscope data to simulate keyboard/gamepad input
"""

import asyncio
import websockets
import json
from datetime import datetime

# Optional: For keyboard simulation (requires pynput)
# Uncomment if you want to control games with keyboard inputs
# pip install pynput
try:
    from pynput.keyboard import Key, Controller
    keyboard = Controller()
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Note: pynput not installed. Keyboard control disabled.")
    print("Install with: pip install pynput")

class GyroController:
    """Process gyroscope data and control game"""
    
    def __init__(self):
        self.steering_threshold = 0.3  # Sensitivity for steering
        self.last_direction = None
        
    def process_gyro_data(self, x, y, z):
        """
        Process gyroscope data and generate control commands
        
        Typical gyro values when holding phone vertically:
        - y: Tilting left/right (steering)
        - x: Tilting forward/backward (acceleration/brake)
        - z: Rolling the phone
        """
        
        # Steering based on Y-axis (left/right tilt)
        if y < -self.steering_threshold:
            direction = "LEFT"
        elif y > self.steering_threshold:
            direction = "RIGHT"
        else:
            direction = "CENTER"
        
        # Acceleration based on X-axis (forward/backward tilt)
        if x > 0.3:
            acceleration = "ACCELERATE"
        elif x < -0.3:
            acceleration = "BRAKE"
        else:
            acceleration = "COAST"
        
        return {
            "steering": direction,
            "acceleration": acceleration,
            "steering_value": y,
            "acceleration_value": x
        }
    
    def simulate_keyboard(self, controls):
        """Simulate keyboard input for game control (if pynput is installed)"""
        if not KEYBOARD_AVAILABLE:
            return
        
        # Example keyboard mapping:
        # - Left Arrow: Steer left
        # - Right Arrow: Steer right
        # - Up Arrow: Accelerate
        # - Down Arrow: Brake
        
        steering = controls["steering"]
        acceleration = controls["acceleration"]
        
        # Release previous keys if direction changed
        if steering != self.last_direction:
            # This is a simplified example
            # In a real implementation, you'd need to track and release keys properly
            pass
        
        self.last_direction = steering

async def handle_client(websocket, path):
    """Handle incoming WebSocket connections"""
    controller = GyroController()
    client_address = websocket.remote_address
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📱 Client connected: {client_address}")
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                x = data.get('x', 0)
                y = data.get('y', 0)
                z = data.get('z', 0)
                
                # Process the gyroscope data
                controls = controller.process_gyro_data(x, y, z)
                
                # Print formatted output
                print(f"🎮 Steering: {controls['steering']:>8} ({controls['steering_value']:6.3f}) | "
                      f"Speed: {controls['acceleration']:>10} ({controls['acceleration_value']:6.3f})")
                
                # Optional: Simulate keyboard input
                # controller.simulate_keyboard(controls)
                
                # Send feedback to client (optional)
                response = {
                    "status": "ok",
                    "controls": controls
                }
                await websocket.send(json.dumps(response))
                
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON: {message}")
            except Exception as e:
                print(f"❌ Error processing message: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 👋 Client disconnected: {client_address}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Start the WebSocket server"""
    host = "0.0.0.0"
    port = 5000
    
    print("\n" + "=" * 70)
    print("🎮 ADVANCED STEERING WHEEL WEBSOCKET SERVER")
    print("=" * 70)
    print(f"🌐 Server: ws://{host}:{port}")
    print(f"⌨️  Keyboard control: {'✅ Enabled' if KEYBOARD_AVAILABLE else '❌ Disabled'}")
    print("\n📋 Gyroscope Mapping:")
    print("   • Y-axis (left/right tilt) → Steering")
    print("   • X-axis (forward/back tilt) → Acceleration/Brake")
    print("   • Z-axis (rotation) → Reserved")
    print("\n🎯 Sensitivity Settings:")
    print("   • Steering threshold: ±0.3")
    print("   • Acceleration threshold: ±0.3")
    print("\n⌨️  Press Ctrl+C to stop")
    print("=" * 70 + "\n")
    
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped gracefully\n")
