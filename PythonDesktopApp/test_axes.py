"""
Test vJoy axes in real-time
Shows current axis values and updates them continuously
"""

import pyvjoy
import time
import sys

print("=" * 70)
print("🎮 vJoy Real-Time Axis Monitor")
print("=" * 70)
print()

try:
    j = pyvjoy.VJoyDevice(1)
    print("✅ vJoy Device 1 connected")
    print()
    print("Testing axes with different values...")
    print("Watch these values in joy.cpl (Game Controllers panel)")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Test sequence
    positions = [
        ("CENTER", 0x4000, 0x1, 0x1),
        ("LEFT MAX", 0x1, 0x1, 0x1),
        ("RIGHT MAX", 0x8000, 0x1, 0x1),
        ("CENTER + GAS", 0x4000, 0x8000, 0x1),
        ("CENTER + BRAKE", 0x4000, 0x1, 0x8000),
        ("CENTER + BOTH", 0x4000, 0x8000, 0x8000),
        ("LEFT + GAS", 0x1, 0x8000, 0x1),
        ("RIGHT + BRAKE", 0x8000, 0x1, 0x8000),
    ]
    
    cycle = 0
    while True:
        for name, x, y, z in positions:
            cycle += 1
            
            # Set axes
            j.set_axis(pyvjoy.HID_USAGE_X, x)
            j.set_axis(pyvjoy.HID_USAGE_Y, y)
            j.set_axis(pyvjoy.HID_USAGE_Z, z)
            
            # Convert to percentage
            x_pct = int((x / 0x8000) * 100)
            y_pct = int((y / 0x8000) * 100)
            z_pct = int((z / 0x8000) * 100)
            
            print(f"[{cycle:04d}] {name:20s} | X:{x_pct:3d}% | Y:{y_pct:3d}% | Z:{z_pct:3d}%")
            
            time.sleep(1.5)
        
        print("-" * 70)

except KeyboardInterrupt:
    print("\n")
    print("Resetting axes to neutral...")
    j.set_axis(pyvjoy.HID_USAGE_X, 0x4000)
    j.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
    j.set_axis(pyvjoy.HID_USAGE_Z, 0x1)
    print("✅ Done!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
