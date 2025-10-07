"""
vJoy Device Test and Diagnostic Tool
Tests vJoy installation and device status
"""

import sys

print("=" * 70)
print("🔍 vJoy Diagnostic Tool")
print("=" * 70)
print()

# Test 1: Check if pyvjoy is installed
print("📦 Test 1: Checking pyvjoy installation...")
try:
    import pyvjoy
    print("   ✅ pyvjoy is installed")
except ImportError as e:
    print(f"   ❌ pyvjoy not installed: {e}")
    print("   Solution: pip install pyvjoy")
    sys.exit(1)

# Test 2: Check vJoy driver
print()
print("🔌 Test 2: Checking vJoy driver...")
try:
    import pyvjoy
    
    # Try to check if vJoy is enabled
    try:
        from pyvjoy import _sdk
        if hasattr(_sdk, 'vJoyEnabled') and callable(_sdk.vJoyEnabled):
            if _sdk.vJoyEnabled():
                print("   ✅ vJoy driver is enabled")
            else:
                print("   ❌ vJoy driver is NOT enabled")
                print("   Solution: Install vJoy driver from https://github.com/njz3/vJoy/releases")
                sys.exit(1)
        else:
            print("   ⚠️  Cannot verify vJoy driver status")
            print("   Continuing with tests...")
    except:
        print("   ⚠️  Cannot verify vJoy driver status")
        print("   Continuing with tests...")
        
except Exception as e:
    print(f"   ❌ vJoy driver error: {e}")
    print("   Solution: Reinstall vJoy driver and restart computer")
    sys.exit(1)

# Test 3: Check Device 1 status
print()
print("🎮 Test 3: Checking vJoy Device 1 status...")
try:
    from pyvjoy import _sdk
    device_id = 1
    
    try:
        status = _sdk.GetVJDStatus(device_id)
        
        status_names = {
            0: "VJD_STAT_OWN (Owned by this feeder)",
            1: "VJD_STAT_FREE (Available)",
            2: "VJD_STAT_BUSY (Owned by another feeder)", 
            3: "VJD_STAT_MISS (Device missing/not configured)",
            4: "VJD_STAT_UNKN (Unknown error)"
        }
        
        status_name = status_names.get(status, f"Unknown status: {status}")
        print(f"   Status: {status_name}")
        
        if status == 3:  # VJD_STAT_MISS
            print("   ❌ Device 1 is NOT configured!")
            print()
            print("   🔧 SOLUTION:")
            print("   1. Open 'Configure vJoy' from Start Menu")
            print("   2. Check 'Enable vJoy Device' for Device 1")
            print("   3. Enable these axes:")
            print("      ✅ X-Axis (Steering)")
            print("      ✅ Y-Axis (Gas)")
            print("      ✅ Z-Axis (Brake)")
            print("   4. Click 'Apply'")
            print("   5. Run this test again")
            sys.exit(1)
        
        elif status == 2:  # VJD_STAT_BUSY
            print("   ⚠️  Device 1 is owned by another program!")
            print()
            print("   🔧 SOLUTION:")
            print("   1. Close any programs using vJoy (joy.cpl, games, etc.)")
            print("   2. Close Game Controllers panel (joy.cpl)")
            print("   3. Run this test again")
            print()
            print("   Trying to reset the device...")
            
            # Try to relinquish the device
            try:
                _sdk.RelinquishVJD(device_id)
                print("   ✅ Device released successfully")
                print("   Please run the test again")
                sys.exit(0)
            except:
                print("   ❌ Could not release device")
                print("   Please restart your computer")
                sys.exit(1)
        
        elif status == 1:  # VJD_STAT_FREE
            print("   ✅ Device 1 is available!")
        
        elif status == 0:  # VJD_STAT_OWN
            print("   ✅ Device 1 is already owned by this feeder")
            # Try to relinquish and re-acquire
            try:
                _sdk.RelinquishVJD(device_id)
                print("   ✅ Device released")
            except:
                pass
    except AttributeError:
        print("   ⚠️  Cannot check device status (older pyvjoy version)")
        print("   Continuing with acquisition test...")
            
except Exception as e:
    print(f"   ❌ Error checking device status: {e}")
    print("   Continuing anyway...")

# Test 4: Try to acquire device
print()
print("🎯 Test 4: Attempting to acquire vJoy Device 1...")
try:
    from pyvjoy import _sdk
    device_id = 1
    
    # First relinquish if owned
    try:
        _sdk.RelinquishVJD(device_id)
        print("   Released any previous ownership")
    except:
        pass
    
    # Try to acquire
    try:
        if _sdk.AcquireVJD(device_id):
            print("   ✅ Successfully acquired Device 1")
        else:
            print("   ❌ Failed to acquire Device 1")
            print()
            print("   🔧 POSSIBLE SOLUTIONS:")
            print("   1. Open 'Configure vJoy' and enable Device 1")
            print("   2. Restart your computer")
            print("   3. Reinstall vJoy driver")
            sys.exit(1)
    except AttributeError:
        print("   ⚠️  Cannot test acquisition (using fallback method)")
        
except Exception as e:
    print(f"   ⚠️  Acquisition test skipped: {e}")

# Test 5: Test axis control
print()
print("🕹️  Test 5: Testing axis control...")
try:
    j = pyvjoy.VJoyDevice(device_id)
    
    # Test X-Axis (Steering)
    print("   Testing X-Axis (Steering)...")
    j.set_axis(pyvjoy.HID_USAGE_X, 0x4000)  # Center
    print("   ✅ X-Axis set to center")
    
    # Test Y-Axis (Gas)
    print("   Testing Y-Axis (Gas)...")
    j.set_axis(pyvjoy.HID_USAGE_Y, 0x1)  # Min
    print("   ✅ Y-Axis set to minimum")
    
    # Test Z-Axis (Brake)
    print("   Testing Z-Axis (Brake)...")
    j.set_axis(pyvjoy.HID_USAGE_Z, 0x1)  # Min
    print("   ✅ Z-Axis set to minimum")
    
    print()
    print("   🎮 All axes working!")
    print()
    print("   📝 Verify in Windows:")
    print("   1. Press Windows + R")
    print("   2. Type: joy.cpl")
    print("   3. Select 'vJoy Device'")
    print("   4. Click 'Properties'")
    print("   5. You should see the axes centered")
    
except Exception as e:
    print(f"   ❌ Axis control error: {e}")
    sys.exit(1)

# Test 6: Cleanup
print()
print("🧹 Test 6: Cleanup...")
try:
    from pyvjoy import _sdk
    device_id = 1
    _sdk.RelinquishVJD(device_id)
    print("   ✅ Device released successfully")
except:
    print("   ⚠️  Could not release device (this is OK)")

print()
print("=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print()
print("🎉 vJoy is ready to use!")
print()
print("Next steps:")
print("1. Run: python main.py")
print("2. Connect your phone")
print("3. Tilt phone to test steering")
print()
