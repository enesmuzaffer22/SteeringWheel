"""
WebSocket Accelerometer to Keyboard Bridge
A desktop application that receives accelerometer data from mobile devices
and translates it into keyboard inputs for PC racing games.
"""

import asyncio
import json
import websockets
import keyboard
from datetime import datetime


class GyroKeyboardBridge:
    """Manages the WebSocket server and keyboard input translation."""
    
    def __init__(self, host='0.0.0.0', port=5000, threshold=0.3):
        """
        Initialize the bridge server.
        
        Args:
            host: Server host address (0.0.0.0 for all interfaces)
            port: Server port number
            threshold: Accelerometer threshold for triggering key presses
        """
        self.host = host
        self.port = port
        self.threshold = threshold
        
        # Track current key state to avoid repeated key presses
        self.left_pressed = False
        self.right_pressed = False
        self.gas_pressed = False
        self.brake_pressed = False
        
    def log(self, message):
        """Print timestamped log message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def release_all_keys(self):
        """Release all arrow keys if they are pressed."""
        if self.left_pressed:
            keyboard.release('left')
            self.left_pressed = False
            self.log("🔓 Released LEFT arrow")
            
        if self.right_pressed:
            keyboard.release('right')
            self.right_pressed = False
            self.log("🔓 Released RIGHT arrow")
        
        if self.gas_pressed:
            keyboard.release('up')
            self.gas_pressed = False
            self.log("🔓 Released UP arrow (gas)")
        
        if self.brake_pressed:
            keyboard.release('down')
            self.brake_pressed = False
            self.log("🔓 Released DOWN arrow (brake)")
    
    def process_gyro_data(self, x, y, z, gas=False, brake=False):
        """
        Process accelerometer data and button states, trigger appropriate key events.
        
        Accelerometer values when phone is HORIZONTAL (landscape - steering wheel):
        - y: Rotate left/right (STEERING) → negative=left, positive=right
        - x: Tilt up/down (could be used for gas/brake)
        - z: Gravity (should be ~0.0 when flat)
        
        Args:
            x: X-axis accelerometer value (up/down tilt)
            y: Y-axis accelerometer value (STEERING - rotation like a wheel)
            z: Z-axis accelerometer value (gravity direction)
            gas: Boolean - gas button pressed state
            brake: Boolean - brake button pressed state
        """
        direction = "CENTER"
        
        # Turn LEFT if y is below negative threshold (rotating left)
        if y < -self.threshold:
            if not self.left_pressed:
                # Release right if it was pressed
                if self.right_pressed:
                    keyboard.release('right')
                    self.right_pressed = False
                
                # Press left arrow
                keyboard.press('left')
                self.left_pressed = True
            direction = "TURN LEFT ⬅️"
        
        # Turn RIGHT if y exceeds positive threshold (rotating right)
        elif y > self.threshold:
            if not self.right_pressed:
                # Release left if it was pressed
                if self.left_pressed:
                    keyboard.release('left')
                    self.left_pressed = False
                
                # Press right arrow
                keyboard.press('right')
                self.right_pressed = True
            direction = "TURN RIGHT ➡️"
        
        # CENTER - release steering keys
        else:
            if self.left_pressed:
                keyboard.release('left')
                self.left_pressed = False
            if self.right_pressed:
                keyboard.release('right')
                self.right_pressed = False
            direction = "CENTER ⬆️"
        
        # Handle GAS button (UP arrow)
        if gas and not self.gas_pressed:
            keyboard.press('up')
            self.gas_pressed = True
            self.log("🟢 GAS pressed (UP arrow)")
        elif not gas and self.gas_pressed:
            keyboard.release('up')
            self.gas_pressed = False
            self.log("⚪ GAS released")
        
        # Handle BRAKE button (DOWN arrow)
        if brake and not self.brake_pressed:
            keyboard.press('down')
            self.brake_pressed = True
            self.log("🔴 BRAKE pressed (DOWN arrow)")
        elif not brake and self.brake_pressed:
            keyboard.release('down')
            self.brake_pressed = False
            self.log("⚪ BRAKE released")
        
        # Log the data and action
        gas_status = "🟢 GAS" if gas else ""
        brake_status = "🔴 BRAKE" if brake else ""
        extra_status = f" {gas_status} {brake_status}".strip()
        self.log(f"[DATA] y={y:+.2f} → {direction} {extra_status}")
    
    async def handle_client(self, websocket, path):
        """
        Handle individual WebSocket client connection.
        
        Args:
            websocket: WebSocket connection object
            path: Connection path
        """
        # Get client address
        client_address = websocket.remote_address[0] if websocket.remote_address else "Unknown"
        self.log(f"✅ [CONNECTED] Client at {client_address}")
        
        try:
            # Continuously receive messages from client
            async for message in websocket:
                try:
                    # Parse JSON data
                    data = json.loads(message)
                    
                    # Extract accelerometer values
                    x = float(data.get('x', 0))
                    y = float(data.get('y', 0))
                    z = float(data.get('z', 0))
                    
                    # Extract button states
                    gas = bool(data.get('gas', False))
                    brake = bool(data.get('brake', False))
                    
                    # Process the accelerometer data and button states
                    self.process_gyro_data(x, y, z, gas, brake)
                    
                except json.JSONDecodeError:
                    self.log(f"⚠️  [ERROR] Invalid JSON: {message}")
                except (ValueError, KeyError) as e:
                    self.log(f"⚠️  [ERROR] Invalid data format: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            self.log(f"❌ [DISCONNECTED] Client at {client_address}")
        
        finally:
            # Release all keys when client disconnects
            self.release_all_keys()
            self.log(f"🛑 [CLEANUP] Released all keys for {client_address}")
    
    async def start_server(self):
        """Start the WebSocket server."""
        self.log("=" * 60)
        self.log("🎮 Accelerometer to Keyboard Bridge Server")
        self.log("=" * 60)
        self.log(f"🌐 Starting server on {self.host}:{self.port}")
        self.log(f"📊 Steering threshold: ±{self.threshold}")
        self.log(f"⌨️  Key mapping:")
        self.log(f"   • y < -{self.threshold} = LEFT arrow")
        self.log(f"   • y > {self.threshold} = RIGHT arrow")
        self.log(f"   • Gas button = UP arrow")
        self.log(f"   • Brake button = DOWN arrow")
        self.log(f"🏎️  Hold phone HORIZONTAL like a steering wheel")
        self.log("=" * 60)
        self.log("⏳ Waiting for client connection...")
        
        # Start WebSocket server
        async with websockets.serve(self.handle_client, self.host, self.port):
            # Keep server running indefinitely
            await asyncio.Future()  # Run forever


def main():
    """Main entry point for the application."""
    try:
        # Create bridge instance (threshold=0.3 for better control)
        bridge = GyroKeyboardBridge(host='0.0.0.0', port=5000, threshold=0.3)
        
        # Start the server
        asyncio.run(bridge.start_server())
    
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("🛑 Server stopped by user (Ctrl+C)")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ [CRITICAL ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
