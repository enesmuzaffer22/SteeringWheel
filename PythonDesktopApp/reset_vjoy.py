"""
vJoy Device Reset Tool
Forces release of vJoy Device 1
"""

import sys

try:
    import pyvjoy
    from pyvjoy import _sdk
except ImportError:
    print("❌ pyvjoy not installed!")
    print("Run: pip install pyvjoy")
    sys.exit(1)

print("=" * 70)
print("🔄 vJoy Device Reset Tool")
print("=" * 70)
print()

device_id = 1

print(f"Checking Device {device_id} status...")
try:
    status = _sdk.GetVJDStatus(device_id)
    
    status_names = {
        0: "VJD_STAT_OWN",
        1: "VJD_STAT_FREE",
        2: "VJD_STAT_BUSY",
        3: "VJD_STAT_MISS",
        4: "VJD_STAT_UNKN"
    }
    
    print(f"Current status: {status_names.get(status, 'Unknown')}")
    print()
    
    if status == 1:
        print("✅ Device is already free!")
        sys.exit(0)
    
    print(f"Attempting to release Device {device_id}...")
    
    # Try multiple times
    for attempt in range(3):
        try:
            _sdk.RelinquishVJD(device_id)
            print(f"   Attempt {attempt + 1}: Released")
            
            # Check status again
            new_status = _sdk.GetVJDStatus(device_id)
            if new_status == 1:
                print()
                print("✅ Device successfully released!")
                print()
                print("You can now run: python main.py")
                sys.exit(0)
        except Exception as e:
            print(f"   Attempt {attempt + 1}: Failed - {e}")
    
    print()
    print("❌ Could not release device automatically")
    print()
    print("🔧 MANUAL STEPS:")
    print("1. Close Game Controllers panel (joy.cpl) if open")
    print("2. Close any games or programs using vJoy")
    print("3. Restart your computer")
    print("4. Run this script again")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("🔧 SOLUTION:")
    print("Restart your computer and try again")
    sys.exit(1)
