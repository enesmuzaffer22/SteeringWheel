"""
vJoy Device Configuration Checker
Verifies that vJoy Device 1 has the correct axes configured
"""

import sys

try:
    import pyvjoy
    from pyvjoy import _sdk
except ImportError:
    print("❌ pyvjoy not installed!")
    sys.exit(1)

print("=" * 70)
print("🔍 vJoy Device Configuration Checker")
print("=" * 70)
print()

device_id = 1

# Check device status
try:
    status = _sdk.GetVJDStatus(device_id)
    status_names = {
        0: "VJD_STAT_OWN (Owned)",
        1: "VJD_STAT_FREE (Available)",
        2: "VJD_STAT_BUSY (Busy)",
        3: "VJD_STAT_MISS (Not Configured)",
        4: "VJD_STAT_UNKN (Unknown)"
    }
    
    print(f"Device Status: {status_names.get(status, 'Unknown')}")
    
    if status == 3:
        print()
        print("❌ ERROR: vJoy Device 1 is NOT configured!")
        print()
        print("🔧 SOLUTION:")
        print("1. Search 'Configure vJoy' in Start Menu")
        print("2. Select Device 1")
        print("3. Check these boxes:")
        print("   ✅ Enable vJoy")
        print("   ✅ X-Axis")
        print("   ✅ Y-Axis")
        print("   ✅ Z-Axis")
        print("4. Click 'Apply'")
        sys.exit(1)
except AttributeError:
    print("⚠️  Cannot check status (older pyvjoy)")

print()

# Try to get axis info
print("Checking available axes...")
print()

# Try to initialize device
try:
    # Release if busy
    try:
        _sdk.RelinquishVJD(device_id)
    except:
        pass
    
    j = pyvjoy.VJoyDevice(device_id)
    print("✅ vJoy Device 1 initialized successfully")
    print()
    
    # Test each axis
    axes_to_test = [
        (pyvjoy.HID_USAGE_X, "X-Axis (Steering)"),
        (pyvjoy.HID_USAGE_Y, "Y-Axis (Gas)"),
        (pyvjoy.HID_USAGE_Z, "Z-Axis (Brake)"),
        (pyvjoy.HID_USAGE_RX, "RX-Axis"),
        (pyvjoy.HID_USAGE_RY, "RY-Axis"),
        (pyvjoy.HID_USAGE_RZ, "RZ-Axis"),
        (pyvjoy.HID_USAGE_SL0, "Slider 0"),
        (pyvjoy.HID_USAGE_SL1, "Slider 1"),
    ]
    
    print("Testing axes:")
    available_axes = []
    
    for axis_id, axis_name in axes_to_test:
        try:
            j.set_axis(axis_id, 0x4000)
            print(f"   ✅ {axis_name}")
            available_axes.append(axis_name)
        except Exception as e:
            print(f"   ❌ {axis_name} - Not available")
    
    print()
    
    if len(available_axes) < 3:
        print("❌ ERROR: Not enough axes configured!")
        print()
        print("Required axes:")
        print("   • X-Axis (for steering)")
        print("   • Y-Axis (for gas)")
        print("   • Z-Axis (for brake)")
        print()
        print("🔧 SOLUTION:")
        print("1. Open 'Configure vJoy' from Start Menu")
        print("2. Select Device 1")
        print("3. Enable X, Y, Z axes")
        print("4. Click 'Apply'")
        sys.exit(1)
    
    # Test buttons
    print("Testing buttons:")
    button_count = 0
    for btn in range(1, 33):  # Test first 32 buttons
        try:
            j.set_button(btn, 1)
            j.set_button(btn, 0)
            button_count += 1
        except:
            break
    
    if button_count > 0:
        print(f"   ✅ {button_count} buttons available")
    else:
        print(f"   ⚠️  No buttons configured (not required for steering wheel)")
    
    print()
    print("=" * 70)
    print("✅ CONFIGURATION OK!")
    print("=" * 70)
    print()
    print("Your vJoy Device 1 is properly configured with:")
    for axis in available_axes[:3]:
        print(f"   ✅ {axis}")
    
    print()
    print("🎮 Next steps:")
    print("1. Open joy.cpl (Game Controllers)")
    print("2. Select 'vJoy Device'")
    print("3. Click 'Properties'")
    print("4. Run: python main.py")
    print("5. Tilt phone and watch axes move")
    print()
    print("🎯 For games:")
    print("• Most modern games auto-detect vJoy as 'vJoy Device'")
    print("• In game settings, select 'Steering Wheel' or 'Custom Controller'")
    print("• Map controls:")
    print("  - Steering → X-Axis")
    print("  - Throttle → Y-Axis")
    print("  - Brake → Z-Axis")
    
    # Reset axes
    j.set_axis(pyvjoy.HID_USAGE_X, 0x4000)
    j.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
    j.set_axis(pyvjoy.HID_USAGE_Z, 0x1)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("🔧 Common solutions:")
    print("1. Make sure vJoy driver is installed")
    print("2. Configure Device 1 in 'Configure vJoy'")
    print("3. Restart computer")
    sys.exit(1)
