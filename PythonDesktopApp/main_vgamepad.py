"""
🎮 ALTERNATIVE: Xbox Controller Emulation with vgamepad
Use this if vJoy continues to have issues or games don't recognize steering wheels.

ADVANTAGES:
- No vJoy driver needed
- Emulates Xbox 360 controller (wider game compatibility)
- More stable ViGEm driver
- Better support in modern games

INSTALLATION:
    pip install vgamepad

USAGE:
    python main_vgamepad.py
"""

import asyncio
import json
import websockets
from datetime import datetime
import time

try:
    import vgamepad as vg
    VGAMEPAD_AVAILABLE = True
except ImportError:
    VGAMEPAD_AVAILABLE = False
    print("❌ ERROR: vgamepad not installed!")
    print("")
    print("📥 INSTALLATION STEPS:")
    print("   1. Download ViGEmBus: https://github.com/ViGEm/ViGEmBus/releases")
    print("   2. Install ViGEmBus_Setup_x64.msi")
    print("   3. Run: pip install vgamepad")
    print("")
    exit(1)


class SteeringWheelBridgeXbox:
    """
    Manages WebSocket server and Xbox 360 controller emulation.
    
    CONTROLLER MAPPING:
    - Left stick X-axis  → Steering (left/right)
    - Left trigger       → Brake
    - Right trigger      → Gas/Throttle
    """
    
    def __init__(self, host='0.0.0.0', port=5000):
        """
        Initialize the Xbox controller bridge server.
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        
        # Initialize Xbox 360 controller
        try:
            self.gamepad = vg.VX360Gamepad()
            self.log("✅ Xbox 360 Controller emulation initialized!")
        except Exception as e:
            self.log(f"❌ Failed to initialize Xbox controller: {e}")
            self.log("")
            self.log("🔧 SOLUTION:")
            self.log("   1. Install ViGEmBus from:")
            self.log("      https://github.com/ViGEm/ViGEmBus/releases")
            self.log("   2. Restart computer")
            self.log("   3. Run: pip install vgamepad")
            exit(1)
        
        # Rate limiting
        self.last_update_time = 0
        self.min_update_interval = 0.01  # 100Hz max
        
    def log(self, message):
        """Print timestamped log message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def update_controller(self, y, gas, brake):
        """
        Update Xbox controller with steering wheel data.
        
        Args:
            y: Y-axis value (-1.0 to +1.0) for steering
            gas: Boolean for gas pedal (right trigger)
            brake: Boolean for brake pedal (left trigger)
        """
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_update_time < self.min_update_interval:
            return
        self.last_update_time = current_time
        
        # Map steering to left stick X-axis
        # Y: -1.0 (left) to +1.0 (right)
        # vgamepad expects: -1.0 to +1.0 (already correct!)
        self.gamepad.left_joystick_float(x_value_float=y, y_value_float=0.0)
        
        # Map gas to right trigger
        # gas: False = 0.0, True = 1.0
        gas_value = 1.0 if gas else 0.0
        self.gamepad.right_trigger_float(value_float=gas_value)
        
        # Map brake to left trigger
        # brake: False = 0.0, True = 1.0
        brake_value = 1.0 if brake else 0.0
        self.gamepad.left_trigger_float(value_float=brake_value)
        
        # Send update to virtual controller
        self.gamepad.update()
        
        # Log status
        direction = "LEFT ⬅️" if y < -0.1 else ("RIGHT ➡️" if y > 0.1 else "CENTER ⬆️")
        status_parts = []
        if gas:
            status_parts.append("🟢 GAS")
        if brake:
            status_parts.append("🔴 BRAKE")
        status = f" {' '.join(status_parts)}" if status_parts else ""
        
        self.log(f"[XBOX] Steering={y:+.2f} ({int(y*100):+3d}%) → {direction}{status}")
    
    def reset_controller(self):
        """Reset controller to neutral position."""
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        self.gamepad.right_trigger_float(value_float=0.0)
        self.gamepad.left_trigger_float(value_float=0.0)
        self.gamepad.update()
        self.log("🎮 Xbox controller reset to neutral")
    
    def process_sensor_data(self, x, y, z, gas, brake):
        """
        Process accelerometer data and update controller.
        
        Args:
            x: X-axis accelerometer value
            y: Y-axis accelerometer value (STEERING)
            z: Z-axis accelerometer value
            gas: Boolean - gas button pressed
            brake: Boolean - brake button pressed
        """
        self.update_controller(y, gas, brake)
    
    async def handle_client(self, websocket, path):
        """Handle individual WebSocket client connection."""
        client_address = websocket.remote_address[0] if websocket.remote_address else "Unknown"
        self.log(f"✅ [CONNECTED] Client at {client_address}")
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    x = float(data.get('x', 0))
                    y = float(data.get('y', 0))
                    z = float(data.get('z', 0))
                    gas = bool(data.get('gas', False))
                    brake = bool(data.get('brake', False))
                    
                    self.process_sensor_data(x, y, z, gas, brake)
                    
                except json.JSONDecodeError:
                    self.log(f"⚠️  [ERROR] Invalid JSON: {message}")
                except (ValueError, KeyError) as e:
                    self.log(f"⚠️  [ERROR] Invalid data format: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            self.log(f"❌ [DISCONNECTED] Client at {client_address}")
        
        finally:
            self.reset_controller()
            self.log(f"🛑 [CLEANUP] Reset controller for {client_address}")
    
    async def start_server(self):
        """Start the WebSocket server."""
        self.log("=" * 70)
        self.log("🎮 VIRTUAL XBOX CONTROLLER SERVER")
        self.log("=" * 70)
        self.log(f"🌐 Server: {self.host}:{self.port}")
        self.log(f"🎮 Device: Xbox 360 Controller (ViGEm)")
        self.log("")
        self.log("🎮 Controller Mapping:")
        self.log("   • Y-axis (tilt L/R)  → Left Stick X (steering)")
        self.log("   • Gas button         → Right Trigger (throttle)")
        self.log("   • Brake button       → Left Trigger (brake)")
        self.log("")
        self.log("✅ Advantages over vJoy:")
        self.log("   • Works in more games (Xbox controller support)")
        self.log("   • No vJoy driver needed")
        self.log("   • More stable ViGEm driver")
        self.log("")
        self.log("📱 Phone Setup:")
        self.log("   1. Open React Native app")
        self.log("   2. Enter: ws://YOUR_PC_IP:5000")
        self.log("   3. Hold phone HORIZONTAL (landscape)")
        self.log("")
        self.log("🔧 Verify Controller:")
        self.log("   Windows + R → joy.cpl → 'Xbox 360 Controller' should be listed")
        self.log("")
        self.log("=" * 70)
        self.log("⏳ Waiting for connection...")
        self.log("")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()


def test_xbox_controller():
    """Test Xbox controller independently."""
    print("=" * 70)
    print("🧪 XBOX CONTROLLER TEST")
    print("=" * 70)
    print("This will test the virtual Xbox 360 controller.")
    print("Open 'joy.cpl' to watch the movement.")
    print("")
    input("Press ENTER to start test...")
    print("")
    
    try:
        gamepad = vg.VX360Gamepad()
        print("✅ Xbox 360 Controller initialized")
        print("")
        
        tests = [
            ("Center position", 0.0, 0.0, 0.0),
            ("Steering LEFT", -1.0, 0.0, 0.0),
            ("Steering RIGHT", 1.0, 0.0, 0.0),
            ("Center + GAS", 0.0, 1.0, 0.0),
            ("Center + BRAKE", 0.0, 0.0, 1.0),
            ("Center + BOTH", 0.0, 1.0, 1.0),
            ("Reset", 0.0, 0.0, 0.0),
        ]
        
        for name, steering, gas, brake in tests:
            print(f"🎮 {name}")
            print(f"   Steering: {steering:+.2f}  Gas: {gas:.2f}  Brake: {brake:.2f}")
            
            gamepad.left_joystick_float(x_value_float=steering, y_value_float=0.0)
            gamepad.right_trigger_float(value_float=gas)
            gamepad.left_trigger_float(value_float=brake)
            gamepad.update()
            
            time.sleep(1.5)
        
        print("")
        print("✅ Test completed!")
        print("If you saw movement in joy.cpl, Xbox controller is working.")
        print("")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point."""
    print("=" * 70)
    print("🎮 XBOX CONTROLLER SERVER")
    print("=" * 70)
    print("")
    print("Options:")
    print("  1. Start WebSocket server (normal mode)")
    print("  2. Run Xbox controller test")
    print("")
    
    choice = input("Enter choice (1 or 2) [default: 1]: ").strip()
    print("")
    
    if choice == "2":
        test_xbox_controller()
        return
    
    try:
        bridge = SteeringWheelBridgeXbox(host='0.0.0.0', port=5000)
        asyncio.run(bridge.start_server())
    
    except KeyboardInterrupt:
        print("\n")
        print("=" * 70)
        print("🛑 Server stopped by user (Ctrl+C)")
        print("=" * 70)
    
    except Exception as e:
        print(f"\n❌ [CRITICAL ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
