"""
Hızlı vJoy Canlı Test
joy.cpl açıkken bu scripti çalıştırın ve eksenlerin hareket ettiğini görün
"""

import sys
import time

try:
    import pyvjoy
except ImportError:
    print("❌ pyvjoy kurulu değil!")
    print("Çözüm: pip install pyvjoy")
    sys.exit(1)

print("=" * 70)
print("🎮 HIZLI vJoy CANLI TEST")
print("=" * 70)
print()
print("📝 ÖNCE BUNLARI YAPIN:")
print("   1. Windows + R tuşlarına basın")
print("   2. 'joy.cpl' yazın ve Enter")
print("   3. 'vJoy Device' seçin")
print("   4. 'Properties' tıklayın")
print()
print("Bu pencereyi açık tutun ve eksenleri izleyin!")
print()
input("Hazır olduğunuzda Enter'a basın...")

print()
print("Device bağlanıyor...")

try:
    from pyvjoy import _sdk
    
    # Serbest bırak
    try:
        _sdk.RelinquishVJD(1)
        time.sleep(0.2)
    except:
        pass
    
    # Bağlan
    j = pyvjoy.VJoyDevice(1)
    print("✅ Bağlandı!")
    print()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    print()
    print("Configure vJoy'da Device 1'in etkin olduğundan emin olun!")
    sys.exit(1)

print("🎮 EKSEN HAREKETLERİ BAŞLIYOR...")
print("   joy.cpl penceresini izleyin!")
print()

try:
    for round_num in range(3):  # 3 tur
        print(f"📍 TUR {round_num + 1}/3")
        print()
        
        # Direksiyon - SOL
        print("   🚗 Direksiyon: ⬅️  TAM SOL")
        j.set_axis(pyvjoy.HID_USAGE_X, 0x1)
        time.sleep(1.5)
        
        # Direksiyon - MERKEZ
        print("   🚗 Direksiyon: ⬆️  MERKEZ")
        j.set_axis(pyvjoy.HID_USAGE_X, 0x4000)
        time.sleep(1.5)
        
        # Direksiyon - SAĞ
        print("   🚗 Direksiyon: ➡️  TAM SAĞ")
        j.set_axis(pyvjoy.HID_USAGE_X, 0x8000)
        time.sleep(1.5)
        
        # Direksiyon - MERKEZ
        print("   🚗 Direksiyon: ⬆️  MERKEZ")
        j.set_axis(pyvjoy.HID_USAGE_X, 0x4000)
        time.sleep(1)
        
        # Gaz - TAM GAZ
        print("   ⛽ Gaz: 🟢 TAM GAZ")
        j.set_axis(pyvjoy.HID_USAGE_Y, 0x8000)
        time.sleep(1.5)
        
        # Gaz - BIRAK
        print("   ⛽ Gaz: ⚪ BIRAKILD")
        j.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
        time.sleep(1)
        
        # Fren - BAS
        print("   🛑 Fren: 🔴 BASILDI")
        j.set_axis(pyvjoy.HID_USAGE_Z, 0x8000)
        time.sleep(1.5)
        
        # Fren - BIRAK
        print("   🛑 Fren: ⚪ BIRAKILD")
        j.set_axis(pyvjoy.HID_USAGE_Z, 0x1)
        time.sleep(1)
        
        print()
    
    print("=" * 70)
    print("✅ TEST TAMAMLANDI!")
    print("=" * 70)
    print()
    print("❓ Eksenlerin hareket ettiğini GÖRDÜNÜZ MÜ?")
    print()
    print("✅ EVET → vJoy düzgün çalışıyor!")
    print("   Şimdi çalıştırın: python main.py")
    print()
    print("❌ HAYIR → Sorun var:")
    print("   1. joy.cpl'yi kapatın ve tekrar açın")
    print("   2. Configure vJoy'da X, Y, Z eksenlerinin etkin olduğunu kontrol edin")
    print("   3. Bilgisayarı yeniden başlatın")
    print("   4. python diagnose_vjoy.py çalıştırın")
    print()
    
    # Sıfırla
    j.set_axis(pyvjoy.HID_USAGE_X, 0x4000)
    j.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
    j.set_axis(pyvjoy.HID_USAGE_Z, 0x1)
    
except KeyboardInterrupt:
    print("\n\n⏹️  Test durduruldu")
    
except Exception as e:
    print(f"\n❌ Hata: {e}")

# Cleanup
try:
    _sdk.RelinquishVJD(1)
except:
    pass
