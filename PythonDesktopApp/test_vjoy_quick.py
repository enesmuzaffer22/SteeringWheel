"""
🧪 Quick vJoy Test Script
Tests vJoy device independently from the main steering wheel application.
Use this to verify vJoy is working before connecting mobile app.

USAGE:
    python test_vjoy_quick.py

REQUIREMENTS:
    - vJoy driver installed
    - Device 1 configured with X, Y, Z axes
    - joy.cpl open to watch movement
"""

import time
import sys

try:
    import pyvjoy
except ImportError:
    print("❌ pyvjoy not installed!")
    print("   Run: pip install pyvjoy")
    exit(1)


def test_vjoy_device():
    """Test vJoy device with corrected values."""
    
    print("=" * 70)
    print("🧪 QUICK vJoy TEST")
    print("=" * 70)
    print("")
    print("This will move vJoy Device 1 through all positions.")
    print("📋 BEFORE RUNNING:")
    print("   1. Press Windows + R")
    print("   2. Type: joy.cpl")
    print("   3. Select 'vJoy Device'")
    print("   4. Click 'Properties'")
    print("   5. Watch the axes move!")
    print("")
    input("Press ENTER when ready...")
    print("")
    
    device_id = 1
    
    # ✅ CORRECTED VALUES
    AXIS_MIN = 0x1        # 1 - Minimum
    AXIS_MAX = 0x7FFF     # 32767 - Maximum (NOT 0x8000!)
    AXIS_CENTER = 0x4001  # 16385 - True center (NOT 0x4000!)
    
    try:
        from pyvjoy import _sdk
        
        # Check driver
        print("🔍 Checking vJoy driver...")
        if not _sdk.vJoyEnabled():
            print("❌ vJoy driver not enabled!")
            print("   Install from: https://github.com/njz3/vJoy/releases")
            return False
        print("✅ Driver is enabled")
        
        # Check device status
        print(f"🔍 Checking Device {device_id} status...")
        status = _sdk.GetVJDStatus(device_id)
        
        status_names = {
            0: "OWN (Owned by this process)",
            1: "FREE (Available)",
            2: "BUSY (Used by another process)",
            3: "MISS (Not configured)",
            4: "UNKN (Unknown)"
        }
        
        print(f"   Status: {status_names.get(status, 'Unknown')}")
        
        if status == 3:  # MISS
            print("❌ Device not configured!")
            print("   1. Start → 'Configure vJoy'")
            print("   2. Enable Device 1")
            print("   3. Check X-Axis, Y-Axis, Z-Axis")
            print("   4. Click Apply")
            return False
        
        # Release if busy
        if status == 2:  # BUSY
            print("⚠️  Device is busy, releasing...")
            _sdk.RelinquishVJD(device_id)
            time.sleep(0.5)
        
        # Acquire device
        print(f"🔍 Acquiring Device {device_id}...")
        if not _sdk.AcquireVJD(device_id):
            print(f"❌ Cannot acquire device {device_id}!")
            print("   Close other programs using vJoy")
            return False
        print(f"✅ Device {device_id} acquired")
        
        # Initialize
        j = pyvjoy.VJoyDevice(device_id)
        
        print("")
        print("=" * 70)
        print("🎮 AXIS CONFIGURATION")
        print("=" * 70)
        print(f"MIN:    {AXIS_MIN:5d} (0x{AXIS_MIN:04X})")
        print(f"CENTER: {AXIS_CENTER:5d} (0x{AXIS_CENTER:04X})")
        print(f"MAX:    {AXIS_MAX:5d} (0x{AXIS_MAX:04X})")
        print("")
        print("=" * 70)
        print("🧪 RUNNING TEST SEQUENCE")
        print("=" * 70)
        print("")
        
        # Test sequence with detailed output
        tests = [
            ("1️⃣  Reset to CENTER", AXIS_CENTER, AXIS_MIN, AXIS_MIN),
            ("2️⃣  Steering FULL LEFT", AXIS_MIN, AXIS_MIN, AXIS_MIN),
            ("3️⃣  Steering FULL RIGHT", AXIS_MAX, AXIS_MIN, AXIS_MIN),
            ("4️⃣  Back to CENTER", AXIS_CENTER, AXIS_MIN, AXIS_MIN),
            ("5️⃣  GAS pressed (Y-axis MAX)", AXIS_CENTER, AXIS_MAX, AXIS_MIN),
            ("6️⃣  GAS released", AXIS_CENTER, AXIS_MIN, AXIS_MIN),
            ("7️⃣  BRAKE pressed (Z-axis MAX)", AXIS_CENTER, AXIS_MIN, AXIS_MAX),
            ("8️⃣  BRAKE released", AXIS_CENTER, AXIS_MIN, AXIS_MIN),
            ("9️⃣  BOTH pedals pressed", AXIS_CENTER, AXIS_MAX, AXIS_MAX),
            ("🔟 Final reset to CENTER", AXIS_CENTER, AXIS_MIN, AXIS_MIN),
        ]
        
        for i, (name, x_val, y_val, z_val) in enumerate(tests, 1):
            print(f"{name}")
            print(f"   X (Steering): {x_val:5d} (0x{x_val:04X})")
            print(f"   Y (Gas):      {y_val:5d} (0x{y_val:04X})")
            print(f"   Z (Brake):    {z_val:5d} (0x{z_val:04X})")
            
            try:
                j.set_axis(pyvjoy.HID_USAGE_X, x_val)
                j.set_axis(pyvjoy.HID_USAGE_Y, y_val)
                j.set_axis(pyvjoy.HID_USAGE_Z, z_val)
                print("   ✅ Sent to vJoy")
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                return False
            
            print("")
            time.sleep(1.8)  # Pause to see movement
        
        print("=" * 70)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("")
        print("If you saw movement in joy.cpl:")
        print("   ✅ vJoy is configured correctly")
        print("   ✅ Axes are responding")
        print("   ✅ You can use the main server")
        print("")
        print("If you did NOT see movement:")
        print("   ❌ Check Configure vJoy settings")
        print("   ❌ Ensure X, Y, Z axes are enabled")
        print("   ❌ Run this script as Administrator")
        print("")
        
        return True
        
    except Exception as e:
        print("")
        print("=" * 70)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    success = test_vjoy_device()
    
    if success:
        print("Next step: Run main.py to start the WebSocket server")
    else:
        print("Fix the issues above before running main.py")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
