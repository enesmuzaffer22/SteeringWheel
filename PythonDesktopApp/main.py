"""
WebSocket Accelerometer to vJoy Steering Wheel Bridge
A desktop application that receives accelerometer data from mobile devices
and translates it into vJoy virtual steering wheel inputs for PC racing games.

🔧 FIXES APPLIED:
- Corrected vJoy axis range (0x1 to 0x7FFF instead of 0x8000)
- Fixed center value (0x4001 instead of 0x4000)
- Added admin privilege check
- Added axis availability validation
- Improved error handling and logging
- Added test function to verify vJoy independently
"""

import asyncio
import json
import websockets
from datetime import datetime
import ctypes
import sys
import time

# Try to import pyvjoy for steering wheel emulation
try:
    import pyvjoy
    VJOY_AVAILABLE = True
except ImportError:
    VJOY_AVAILABLE = False
    print("❌ ERROR: pyvjoy not installed!")
    print("")
    print("📥 INSTALLATION STEPS:")
    print("   1. Download vJoy driver: https://github.com/njz3/vJoy/releases")
    print("   2. Install vJoySetup.exe as Administrator")
    print("   3. Restart your computer")
    print("   4. Run: pip install pyvjoy")
    print("")
    exit(1)


def is_admin():
    """Check if script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_admin_privileges():
    """Verify admin privileges and warn user if not running as admin."""
    if not is_admin():
        print("⚠️  WARNING: Not running as Administrator!")
        print("   vJoy may not work correctly without admin privileges.")
        print("")
        print("🔧 TO FIX:")
        print("   1. Close this window")
        print("   2. Right-click on PowerShell/Terminal")
        print("   3. Select 'Run as Administrator'")
        print("   4. Run the script again")
        print("")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            exit(0)
        print("")


class SteeringWheelBridge:
    """Manages the WebSocket server and vJoy steering wheel emulation."""
    
    # vJoy device status constants
    VJD_STAT_OWN = 0    # Device is owned by this process
    VJD_STAT_FREE = 1   # Device is free
    VJD_STAT_BUSY = 2   # Device is owned by another process
    VJD_STAT_MISS = 3   # Device is not installed/configured
    VJD_STAT_UNKN = 4   # Unknown status
    
    def __init__(self, host='0.0.0.0', port=5000, vjoy_device_id=1):
        """
        Initialize the steering wheel bridge server.
        
        Args:
            host: Server host address (0.0.0.0 for all interfaces)
            port: Server port number
            vjoy_device_id: vJoy device ID (1-16, default is 1)
        """
        self.host = host
        self.port = port
        self.vjoy_device_id = vjoy_device_id
        
        # 🔧 FIX #1: Correct vJoy axis range
        # vJoy uses 16-bit values: 0x1 (min) to 0x7FFF (max), NOT 0x8000
        # Center is 0x4001 (16385), not 0x4000
        self.AXIS_MIN = 0x1        # 1 (minimum value)
        self.AXIS_MAX = 0x7FFF     # 32767 (maximum value) - CORRECTED from 0x8000
        self.AXIS_CENTER = 0x4001  # 16385 (center) - CORRECTED from 0x4000
        
        # Initialize vJoy device
        try:
            # First, try to release the device if it's held by another program
            from pyvjoy import _sdk
            
            try:
                # 🔧 FIX #2: Check if vJoy driver is enabled
                if hasattr(_sdk, 'vJoyEnabled') and callable(_sdk.vJoyEnabled):
                    if not _sdk.vJoyEnabled():
                        self.log("❌ vJoy driver etkin değil!")
                        self.log("")
                        self.log("🔧 ÇÖZÜM:")
                        self.log("   1. https://github.com/njz3/vJoy/releases")
                        self.log("   2. vJoySetup.exe'yi Administrator olarak yükleyin")
                        self.log("   3. Bilgisayarı yeniden başlatın")
                        exit(1)
                
                # 🔧 FIX #3: Use constants for device status
                status = _sdk.GetVJDStatus(vjoy_device_id)
                
                if status == self.VJD_STAT_BUSY:
                    self.log(f"⚠️  Device {vjoy_device_id} meşgul, serbest bırakılıyor...")
                    _sdk.RelinquishVJD(vjoy_device_id)
                    time.sleep(0.5)
                    
                    # Tekrar kontrol et
                    status = _sdk.GetVJDStatus(vjoy_device_id)
                    if status == self.VJD_STAT_BUSY:
                        self.log("❌ Device serbest bırakılamadı!")
                        self.log("")
                        self.log("🔧 ÇÖZÜM:")
                        self.log("   1. joy.cpl'yi kapatın (Game Controllers)")
                        self.log("   2. vJoy kullanan programları kapatın")
                        self.log("   3. Bilgisayarı yeniden başlatın")
                        exit(1)
                        
                elif status == self.VJD_STAT_MISS:
                    self.log(f"❌ Device {vjoy_device_id} ayarlanmamış!")
                    self.log("")
                    self.log("🔧 ÇÖZÜM:")
                    self.log("   1. Başlat menüsünde 'Configure vJoy' açın")
                    self.log("   2. Device 1'i etkinleştirin")
                    self.log("   3. X, Y, Z eksenlerini etkinleştirin")
                    self.log("   4. 'Apply' tıklayın")
                    self.log("")
                    self.log("VEYA terminalde çalıştırın:")
                    self.log("   python diagnose_vjoy.py")
                    exit(1)
                    
                elif status == self.VJD_STAT_FREE or status == self.VJD_STAT_OWN:
                    # Önce serbest bırak
                    try:
                        _sdk.RelinquishVJD(vjoy_device_id)
                        time.sleep(0.2)
                    except:
                        pass
                    
                    # Şimdi al
                    if _sdk.AcquireVJD(vjoy_device_id):
                        self.log(f"✅ Device {vjoy_device_id} başarıyla alındı")
                    else:
                        self.log(f"❌ Device {vjoy_device_id} alınamadı!")
                        self.log("   Lütfen diagnose_vjoy.py çalıştırın")
                        exit(1)
                        
            except AttributeError:
                self.log("⚠️  Eski pyvjoy sürümü, temel kontroller yapılamıyor...")
            except Exception as e:
                self.log(f"⚠️  Durum kontrolü hatası: {e}")
                self.log("   Devam ediliyor...")
            
            # Initialize device
            self.joystick = pyvjoy.VJoyDevice(vjoy_device_id)
            self.log(f"🎮 vJoy Device #{vjoy_device_id} başlatıldı!")
            
            # 🔧 FIX #4: Validate that required axes are available
            self.log("🔍 Eksen kullanılabilirliği kontrol ediliyor...")
            axes_available = True
            
            # Check X-axis (steering)
            try:
                self.joystick.set_axis(pyvjoy.HID_USAGE_X, self.AXIS_CENTER)
                self.log("   ✅ X-Axis (Steering) kullanılabilir")
            except Exception as e:
                self.log(f"   ❌ X-Axis kullanılamıyor: {e}")
                axes_available = False
            
            # Check Y-axis (gas/throttle)
            try:
                self.joystick.set_axis(pyvjoy.HID_USAGE_Y, self.AXIS_MIN)
                self.log("   ✅ Y-Axis (Gas) kullanılabilir")
            except Exception as e:
                self.log(f"   ❌ Y-Axis kullanılamıyor: {e}")
                axes_available = False
            
            # Check Z-axis (brake)
            try:
                self.joystick.set_axis(pyvjoy.HID_USAGE_Z, self.AXIS_MIN)
                self.log("   ✅ Z-Axis (Brake) kullanılabilir")
            except Exception as e:
                self.log(f"   ❌ Z-Axis kullanılamıyor: {e}")
                axes_available = False
            
            if not axes_available:
                self.log("")
                self.log("❌ Gerekli eksenler etkin değil!")
                self.log("")
                self.log("🔧 ÇÖZÜM:")
                self.log("   1. Başlat → 'Configure vJoy'")
                self.log("   2. X-Axis, Y-Axis, Z-Axis'i işaretleyin")
                self.log("   3. 'Apply' → 'OK'")
                self.log("   4. Bu programı yeniden başlatın")
                exit(1)
            
            self.log("✅ Tüm eksenler çalışıyor!")
                
        except Exception as e:
            self.log(f"❌ vJoy Device #{vjoy_device_id} başlatılamadı!")
            self.log(f"   Hata: {e}")
            self.log("")
            self.log("🔧 SORUN GİDERME:")
            self.log("   1. Başlat → 'Configure vJoy'")
            self.log("   2. Device 1 etkin")
            self.log("   3. X-Axis, Y-Axis, Z-Axis etkin")
            self.log("   4. 'Apply' tıklayın")
            self.log("")
            self.log("   Veya çalıştırın: python diagnose_vjoy.py")
            exit(1)
        
        # Current values for tracking
        self.current_steering = self.AXIS_CENTER
        self.current_gas = self.AXIS_MIN
        self.current_brake = self.AXIS_MIN
        
        # 🔧 FIX #5: Add rate limiting to prevent flooding vJoy driver
        self.last_update_time = 0
        self.min_update_interval = 0.01  # 10ms minimum between updates (100Hz max)
        
    def log(self, message):
        """Print timestamped log message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def map_to_axis(self, value, min_val=-1.0, max_val=1.0):
        """
        Map a float value to vJoy axis range.
        
        Args:
            value: Input value to map
            min_val: Minimum input value
            max_val: Maximum input value
            
        Returns:
            Integer value in vJoy axis range (0x1 to 0x8000)
        """
        # Clamp input value
        value = max(min_val, min(max_val, value))
        
        # Normalize to 0.0-1.0
        normalized = (value - min_val) / (max_val - min_val)
        
        # Map to vJoy range
        axis_value = int(self.AXIS_MIN + (normalized * (self.AXIS_MAX - self.AXIS_MIN)))
        
        return axis_value
    
    def update_steering_wheel(self, y, gas, brake):
        """
        Update vJoy device with steering wheel data.
        
        Args:
            y: Y-axis value (-1.0 to +1.0) for steering
            gas: Boolean for gas pedal
            brake: Boolean for brake pedal
        """
        # 🔧 FIX #6: Rate limiting to prevent driver flooding
        current_time = time.time()
        if current_time - self.last_update_time < self.min_update_interval:
            return  # Skip this update if too soon
        self.last_update_time = current_time
        
        # MAP Y-AXIS to STEERING (X-AXIS in vJoy)
        # Y: -1.0 (full left) to +1.0 (full right)
        steering_value = self.map_to_axis(y, -1.0, 1.0)
        
        # 🔧 FIX #10: TERS ÇEVRİLDİ - Oyunlar genellikle Z=Gaz, Y=Fren bekler
        # MAP GAS to Z-AXIS in vJoy (DÜZELTME: Önceden Y-Axis'teydi)
        # Gas: False = 0, True = full throttle
        gas_value = self.AXIS_MAX if gas else self.AXIS_MIN
        
        # MAP BRAKE to Y-AXIS in vJoy (DÜZELTME: Önceden Z-Axis'teydi)
        # Brake: False = 0, True = full brake
        brake_value = self.AXIS_MAX if brake else self.AXIS_MIN
        
        # 🔧 FIX #7: Critical error handling - stop execution on axis failure
        try:
            # Send all three axes
            self.joystick.set_axis(pyvjoy.HID_USAGE_X, steering_value)
            self.joystick.set_axis(pyvjoy.HID_USAGE_Z, gas_value)      # Z-Axis = GAS (DEĞİŞTİRİLDİ)
            self.joystick.set_axis(pyvjoy.HID_USAGE_Y, brake_value)    # Y-Axis = BRAKE (DEĞİŞTİRİLDİ)
            
            # Update tracking values
            self.current_steering = steering_value
            self.current_gas = gas_value
            self.current_brake = brake_value
            
            # 🔧 FIX #8: Verbose logging to verify values sent to vJoy
            # Uncomment for detailed debugging:
            # self.log(f"   [VJOY] X={steering_value:5d} Y={gas_value:5d} Z={brake_value:5d}")
            
        except Exception as e:
            self.log(f"❌ CRITICAL: Eksen güncelleme hatası: {e}")
            self.log("   vJoy device artık yanıt vermiyor!")
            self.log("   Programı yeniden başlatın veya diagnose_vjoy.py çalıştırın")
            raise  # Re-raise exception to stop execution
    
    def reset_steering_wheel(self):
        """Reset all axes to neutral/off position."""
        self.joystick.set_axis(pyvjoy.HID_USAGE_X, self.AXIS_CENTER)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Z, self.AXIS_MIN)  # Z = GAS (reset to 0)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Y, self.AXIS_MIN)  # Y = BRAKE (reset to 0)
        
        self.current_steering = self.AXIS_CENTER
        self.current_gas = self.AXIS_MIN
        self.current_brake = self.AXIS_MIN
        
        self.log("🎮 Steering wheel reset to neutral")
    
    def process_sensor_data(self, x, y, z, gas, brake):
        """
        Process accelerometer data and update steering wheel.
        
        Args:
            x: X-axis accelerometer value
            y: Y-axis accelerometer value (STEERING)
            z: Z-axis accelerometer value
            gas: Boolean - gas button pressed
            brake: Boolean - brake button pressed
        """
        # Update vJoy device
        self.update_steering_wheel(y, gas, brake)
        
        # Calculate steering percentage
        steering_percent = int(y * 100)
        
        # Determine direction
        if y < -0.3:
            direction = "LEFT ⬅️"
        elif y > 0.3:
            direction = "RIGHT ➡️"
        else:
            direction = "CENTER ⬆️"
        
        # Build status string
        status_parts = []
        if gas:
            status_parts.append("🟢 GAS")
        if brake:
            status_parts.append("🔴 BRAKE")
        
        status = f" {' '.join(status_parts)}" if status_parts else ""
        
        # Log with details
        self.log(f"[WHEEL] y={y:+.2f} ({steering_percent:+3d}%) → {direction}{status}")
    
    async def handle_client(self, websocket, path):
        """
        Handle individual WebSocket client connection.
        
        Args:
            websocket: WebSocket connection object
            path: Connection path
        """
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
                    
                    # Process the data
                    self.process_sensor_data(x, y, z, gas, brake)
                    
                except json.JSONDecodeError:
                    self.log(f"⚠️  [ERROR] Invalid JSON: {message}")
                except (ValueError, KeyError) as e:
                    self.log(f"⚠️  [ERROR] Invalid data format: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            self.log(f"❌ [DISCONNECTED] Client at {client_address}")
        
        finally:
            # Reset steering wheel when client disconnects
            self.reset_steering_wheel()
            self.log(f"🛑 [CLEANUP] Reset controls for {client_address}")
    
    async def start_server(self):
        """Start the WebSocket server."""
        self.log("=" * 70)
        self.log("🏎️  VIRTUAL STEERING WHEEL SERVER (vJoy)")
        self.log("=" * 70)
        self.log(f"🌐 Server: {self.host}:{self.port}")
        self.log(f"🎮 Device: vJoy Device #{self.vjoy_device_id}")
        self.log("")
        self.log("🎮 Steering Wheel Mapping:")
        self.log("   • Y-axis (tilt L/R) → X-AXIS (steering)")
        self.log("   • Gas button       → Z-AXIS (throttle) ✅ DÜZELTİLDİ")
        self.log("   • Brake button     → Y-AXIS (brake) ✅ DÜZELTİLDİ")
        self.log("")
        self.log("🎯 vJoy Configuration (FIXED):")
        self.log(f"   • Range: {self.AXIS_MIN} (0x{self.AXIS_MIN:04X}) to {self.AXIS_MAX} (0x{self.AXIS_MAX:04X})")
        self.log(f"   • Center: {self.AXIS_CENTER} (0x{self.AXIS_CENTER:04X})")
        self.log("   • Resolution: 16-bit (32767 steps)")
        self.log("")
        self.log("📱 Phone Setup:")
        self.log("   1. Open React Native app")
        self.log("   2. Enter: ws://YOUR_PC_IP:5000")
        self.log("   3. Hold phone HORIZONTAL (landscape)")
        self.log("")
        self.log("🔧 Verify vJoy:")
        self.log("   Windows + R → joy.cpl → 'vJoy Device' should move")
        self.log("")
        self.log("=" * 70)
        self.log("⏳ Waiting for connection...")
        self.log("")
        
        # Start WebSocket server
        async with websockets.serve(self.handle_client, self.host, self.port):
            # Keep server running indefinitely
            await asyncio.Future()


def test_vjoy_movement():
    """
    🧪 INDEPENDENT TEST FUNCTION
    Tests vJoy device movement without WebSocket connection.
    Run this to verify vJoy is working before testing with mobile app.
    """
    print("=" * 70)
    print("🧪 vJoy INDEPENDENT TEST")
    print("=" * 70)
    print("This will move the vJoy device through all positions.")
    print("Open 'joy.cpl' (Game Controllers) to watch the movement.")
    print("")
    input("Press ENTER to start test...")
    print("")
    
    try:
        from pyvjoy import _sdk
        
        # Check driver
        if not _sdk.vJoyEnabled():
            print("❌ vJoy driver not enabled!")
            return
        
        device_id = 1
        status = _sdk.GetVJDStatus(device_id)
        
        if status == 3:  # MISS
            print(f"❌ Device {device_id} not configured!")
            return
        
        # Acquire device
        if status == 2:  # BUSY
            _sdk.RelinquishVJD(device_id)
            time.sleep(0.5)
        
        if not _sdk.AcquireVJD(device_id):
            print(f"❌ Cannot acquire device {device_id}!")
            return
        
        # Initialize
        j = pyvjoy.VJoyDevice(device_id)
        print(f"✅ Device {device_id} acquired")
        print("")
        
        # Corrected axis values
        AXIS_MIN = 0x1
        AXIS_MAX = 0x7FFF
        AXIS_CENTER = 0x4001
        
        # Test sequence
        tests = [
            ("Center position", AXIS_CENTER, AXIS_MIN, AXIS_MIN),
            ("Full LEFT", AXIS_MIN, AXIS_MIN, AXIS_MIN),
            ("Full RIGHT", AXIS_MAX, AXIS_MIN, AXIS_MIN),
            ("Center + GAS", AXIS_CENTER, AXIS_MAX, AXIS_MIN),
            ("Center + BRAKE", AXIS_CENTER, AXIS_MIN, AXIS_MAX),
            ("Center + BOTH", AXIS_CENTER, AXIS_MAX, AXIS_MAX),
            ("Reset to center", AXIS_CENTER, AXIS_MIN, AXIS_MIN),
        ]
        
        for name, x_val, y_val, z_val in tests:
            print(f"🎮 {name}")
            print(f"   X={x_val:5d} (0x{x_val:04X})  Y={y_val:5d} (0x{y_val:04X})  Z={z_val:5d} (0x{z_val:04X})")
            
            j.set_axis(pyvjoy.HID_USAGE_X, x_val)
            j.set_axis(pyvjoy.HID_USAGE_Y, y_val)
            j.set_axis(pyvjoy.HID_USAGE_Z, z_val)
            
            time.sleep(1.5)
        
        print("")
        print("✅ Test completed!")
        print("If you saw movement in joy.cpl, vJoy is working correctly.")
        print("")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point for the application."""
    
    # 🔧 FIX #9: Check admin privileges on startup
    check_admin_privileges()
    
    # Allow user to run independent test
    print("=" * 70)
    print("🏎️  STEERING WHEEL SERVER")
    print("=" * 70)
    print("")
    print("Options:")
    print("  1. Start WebSocket server (normal mode)")
    print("  2. Run vJoy test (verify vJoy works)")
    print("")
    
    choice = input("Enter choice (1 or 2) [default: 1]: ").strip()
    print("")
    
    if choice == "2":
        test_vjoy_movement()
        return
    
    try:
        # Create steering wheel bridge instance
        bridge = SteeringWheelBridge(
            host='0.0.0.0', 
            port=5000,
            vjoy_device_id=1  # vJoy Device 1 (change if using different device)
        )
        
        # Start the server
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
