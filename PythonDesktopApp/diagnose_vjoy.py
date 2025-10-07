"""
vJoy Tam Tanılama ve Test Aracı
Tüm vJoy sorunlarını tespit eder ve çözer
"""

import sys
import time

print("=" * 80)
print("🔍 vJoy TAM TANIMLAMA ARACI")
print("=" * 80)
print()

# Test 1: pyvjoy kurulumu
print("📦 Test 1: pyvjoy kontrolü...")
try:
    import pyvjoy
    print("   ✅ pyvjoy kurulu")
except ImportError:
    print("   ❌ pyvjoy kurulu değil!")
    print("   Çözüm: pip install pyvjoy")
    sys.exit(1)

# Test 2: vJoy driver kontrolü
print()
print("🔌 Test 2: vJoy driver kontrolü...")
try:
    from pyvjoy import _sdk
    
    # vJoy etkin mi kontrol et
    try:
        if hasattr(_sdk, 'vJoyEnabled') and callable(_sdk.vJoyEnabled):
            enabled = _sdk.vJoyEnabled()
            if enabled:
                print("   ✅ vJoy driver etkin")
            else:
                print("   ❌ vJoy driver etkin DEĞİL!")
                print("   Çözüm: https://github.com/njz3/vJoy/releases adresinden vJoy'u yükleyin")
                sys.exit(1)
        else:
            print("   ⚠️  vJoyEnabled fonksiyonu bulunamadı, devam ediliyor...")
    except Exception as e:
        print(f"   ⚠️  Driver kontrol hatası: {e}")
        print("   Devam ediliyor...")
        
except Exception as e:
    print(f"   ❌ vJoy SDK yükleme hatası: {e}")
    sys.exit(1)

# Test 3: Device 1 durumu
print()
print("🎮 Test 3: vJoy Device 1 durumu...")
device_id = 1

try:
    status = _sdk.GetVJDStatus(device_id)
    
    status_map = {
        0: ("VJD_STAT_OWN", "Bu program tarafından kullanılıyor", "✅"),
        1: ("VJD_STAT_FREE", "Kullanılabilir", "✅"),
        2: ("VJD_STAT_BUSY", "Başka bir program kullanıyor", "⚠️"),
        3: ("VJD_STAT_MISS", "Ayarlanmamış/Eksik", "❌"),
        4: ("VJD_STAT_UNKN", "Bilinmeyen hata", "❌")
    }
    
    code, desc, icon = status_map.get(status, ("UNKNOWN", "Bilinmeyen durum", "❓"))
    print(f"   {icon} Durum: {code}")
    print(f"   Açıklama: {desc}")
    
    if status == 3:  # Missing
        print()
        print("   ❌ CİHAZ AYARLANMAMIŞ!")
        print()
        print("   🔧 ÇÖZÜM ADIMLARı:")
        print("   1. Başlat menüsünde 'Configure vJoy' arayın")
        print("   2. Device 1'i seçin")
        print("   3. 'Enable vJoy' kutusunu işaretleyin")
        print("   4. Şu eksenleri etkinleştirin:")
        print("      ✅ X-Axis (Direksiyon)")
        print("      ✅ Y-Axis (Gaz)")
        print("      ✅ Z-Axis (Fren)")
        print("   5. 'Apply' tıklayın")
        print("   6. Bu scripti tekrar çalıştırın")
        sys.exit(1)
    
    elif status == 2:  # Busy
        print()
        print("   ⚠️  Cihaz başka bir program tarafından kullanılıyor!")
        print()
        print("   Serbest bırakılmaya çalışılıyor...")
        
        try:
            _sdk.RelinquishVJD(device_id)
            time.sleep(0.5)
            
            new_status = _sdk.GetVJDStatus(device_id)
            if new_status == 1:
                print("   ✅ Cihaz başarıyla serbest bırakıldı!")
            else:
                print("   ❌ Serbest bırakılamadı")
                print()
                print("   🔧 MANUEL ADIMLAR:")
                print("   1. joy.cpl panelini kapatın (Game Controllers)")
                print("   2. vJoy kullanan tüm programları kapatın")
                print("   3. Bilgisayarı yeniden başlatın")
                sys.exit(1)
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            sys.exit(1)

except Exception as e:
    print(f"   ❌ Durum kontrolü hatası: {e}")
    sys.exit(1)

# Test 4: Cihazı al
print()
print("🎯 Test 4: vJoy Device 1 bağlanıyor...")

try:
    # Önce serbest bırak
    try:
        _sdk.RelinquishVJD(device_id)
        time.sleep(0.2)
    except:
        pass
    
    # Şimdi al
    joystick = pyvjoy.VJoyDevice(device_id)
    print("   ✅ Device 1 başarıyla bağlandı!")
    
except Exception as e:
    print(f"   ❌ Bağlanma hatası: {e}")
    print()
    print("   🔧 ÇÖZÜM:")
    print("   1. 'Configure vJoy' açın")
    print("   2. Device 1'i etkinleştirin")
    print("   3. X, Y, Z eksenlerini etkinleştirin")
    print("   4. Apply tıklayın")
    print("   5. Bilgisayarı yeniden başlatın")
    sys.exit(1)

# Test 5: Eksenleri test et
print()
print("🕹️  Test 5: Eksenleri test ediliyor...")

axes_to_test = [
    (pyvjoy.HID_USAGE_X, "X-Axis (Direksiyon)", 0x4000, "Merkez"),
    (pyvjoy.HID_USAGE_Y, "Y-Axis (Gaz)", 0x1, "Minimum"),
    (pyvjoy.HID_USAGE_Z, "Z-Axis (Fren)", 0x1, "Minimum"),
]

all_ok = True
for axis_id, axis_name, test_value, position in axes_to_test:
    try:
        joystick.set_axis(axis_id, test_value)
        print(f"   ✅ {axis_name} → {position} (0x{test_value:X})")
        time.sleep(0.1)
    except Exception as e:
        print(f"   ❌ {axis_name} → HATA: {e}")
        all_ok = False

if not all_ok:
    print()
    print("   ❌ Bazı eksenler çalışmıyor!")
    print()
    print("   🔧 ÇÖZÜM:")
    print("   Configure vJoy'da X, Y, Z eksenlerinin hepsini etkinleştirin")
    sys.exit(1)

# Test 6: Dinamik test
print()
print("🎮 Test 6: Dinamik eksen hareketi testi...")
print("   Aşağıdaki hareketleri yapacağım:")
print("   • Direksiyon: Sol → Merkez → Sağ → Merkez")
print("   • Gaz: 0% → 100% → 0%")
print("   • Fren: 0% → 100% → 0%")
print()
print("   📝 Windows'ta kontrol için:")
print("   1. Windows + R tuşlarına basın")
print("   2. 'joy.cpl' yazın ve Enter")
print("   3. 'vJoy Device' seçin")
print("   4. 'Properties' tıklayın")
print("   5. Eksenlerin hareket ettiğini görmelisiniz!")
print()
input("   Enter tuşuna basarak teste başlayın...")

try:
    print()
    print("   🚗 Direksiyon testi...")
    
    # Sol
    joystick.set_axis(pyvjoy.HID_USAGE_X, 0x1)
    print("      ⬅️  TAM SOL")
    time.sleep(1)
    
    # Merkez
    joystick.set_axis(pyvjoy.HID_USAGE_X, 0x4000)
    print("      ⬆️  MERKEZ")
    time.sleep(1)
    
    # Sağ
    joystick.set_axis(pyvjoy.HID_USAGE_X, 0x8000)
    print("      ➡️  TAM SAĞ")
    time.sleep(1)
    
    # Merkez
    joystick.set_axis(pyvjoy.HID_USAGE_X, 0x4000)
    print("      ⬆️  MERKEZ")
    time.sleep(1)
    
    print()
    print("   ⛽ Gaz testi...")
    
    # 0%
    joystick.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
    print("      🔴 0%")
    time.sleep(1)
    
    # 50%
    joystick.set_axis(pyvjoy.HID_USAGE_Y, 0x4000)
    print("      🟡 50%")
    time.sleep(1)
    
    # 100%
    joystick.set_axis(pyvjoy.HID_USAGE_Y, 0x8000)
    print("      🟢 100%")
    time.sleep(1)
    
    # 0%
    joystick.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
    print("      🔴 0%")
    time.sleep(1)
    
    print()
    print("   🛑 Fren testi...")
    
    # 0%
    joystick.set_axis(pyvjoy.HID_USAGE_Z, 0x1)
    print("      ⚪ 0%")
    time.sleep(1)
    
    # 100%
    joystick.set_axis(pyvjoy.HID_USAGE_Z, 0x8000)
    print("      🔴 100%")
    time.sleep(1)
    
    # 0%
    joystick.set_axis(pyvjoy.HID_USAGE_Z, 0x1)
    print("      ⚪ 0%")
    time.sleep(1)
    
    print()
    print("   ✅ Tüm hareketler başarılı!")
    
except Exception as e:
    print(f"   ❌ Hareket testi hatası: {e}")
    sys.exit(1)

# Test 7: Sıfırlama
print()
print("🔄 Test 7: Cihaz sıfırlanıyor...")
try:
    joystick.set_axis(pyvjoy.HID_USAGE_X, 0x4000)  # Merkez
    joystick.set_axis(pyvjoy.HID_USAGE_Y, 0x1)     # Min
    joystick.set_axis(pyvjoy.HID_USAGE_Z, 0x1)     # Min
    print("   ✅ Tüm eksenler nötr konuma getirildi")
except Exception as e:
    print(f"   ⚠️  Sıfırlama hatası: {e}")

# Test 8: Oyunlarda kullanım
print()
print("=" * 80)
print("✅ TÜM TESTLER BAŞARILI!")
print("=" * 80)
print()
print("🎮 vJoy Device 1 tamamen çalışıyor!")
print()
print("📋 Sonraki Adımlar:")
print()
print("1️⃣  WINDOWS'TA KONTROL ET:")
print("   • Windows + R → joy.cpl")
print("   • 'vJoy Device' seçin → Properties")
print("   • Eksenlerin hareket ettiğini gördünüz mü? ✅")
print()
print("2️⃣  SUNUCUYU BAŞLAT:")
print("   • python main.py")
print("   • Telefonunuzu bağlayın")
print("   • joy.cpl'de hareketleri izleyin")
print()
print("3️⃣  OYUNDA KULLAN:")
print("   • Oyun ayarlarını açın")
print("   • Controller/Gamepad ayarlarına gidin")
print("   • 'vJoy Device' seçin")
print("   • Kontrolleri ayarlayın:")
print("     - Steering/Direksiyon → X-Axis")
print("     - Throttle/Gaz → Y-Axis")
print("     - Brake/Fren → Z-Axis")
print()
print("4️⃣  SORUN YAŞARSAN:")
print("   • Oyunu yeniden başlat")
print("   • vJoy'u yeniden yapılandır (Configure vJoy)")
print("   • Bilgisayarı yeniden başlat")
print()
print("=" * 80)
print()

# Cleanup
try:
    _sdk.RelinquishVJD(device_id)
except:
    pass
