# 🎮 vJoy Kurulum Rehberi

## 📥 1. vJoy Driver'ı İndirin

### **İndirme Linki:**

https://github.com/njz3/vJoy/releases/latest

**Hangi dosyayı indireceğim?**

- `vJoySetup.exe` (Windows 10/11 için)

### **Kurulum Adımları:**

1. `vJoySetup.exe` dosyasını indirin
2. **Sağ tık** → **"Yönetici olarak çalıştır"**
3. Kurulum sihirbazını takip edin
4. "Install" butonuna tıklayın
5. Windows bir güvenlik uyarısı gösterebilir - "Yine de yükle" deyin
6. Kurulum tamamlandıktan sonra bilgisayarı **yeniden başlatın**

## ⚙️ 2. vJoy'u Yapılandırın

### **vJoy Configure Programını Açın:**

```
Başlat Menüsü → "vJoy" ara → "Configure vJoy"
```

### **Ayarlar:**

1. **Device seçin**: vJoy Device 1
2. **Axis (Eksenler)**:

   - ✅ X Axis (Direksiyon için)
   - ✅ Y Axis (Gaz/Fren için - opsiyonel)
   - ✅ Z Axis (Ek kontrol için - opsiyonel)
   - ❌ Diğer eksenler (kapalı)

3. **Buttons (Butonlar)**:

   - Number of Buttons: 8 (yeterli)

4. **POV Hat Switch**:

   - Discrete POVs: 0 (kapalı)

5. **Apply** butonuna tıklayın
6. **Enable vJoy** kutusunu işaretleyin

## 🐍 3. Python Paketi Kurun

```powershell
cd PythonDesktopApp
pip install pyvjoy
```

## ✅ 4. Test Edin

### **Windows Joystick Test:**

```
Windows + R → joy.cpl
```

Listede **"vJoy Device"** görünmeli.

### **Properties → Test:**

- X-axis'i hareket ettirmeyi test edin
- Joystick merkez pozisyonda olmalı

## 🎮 vJoy vs vgamepad vs Keyboard

| Özellik            | Klavye         | vgamepad        | vJoy                  |
| ------------------ | -------------- | --------------- | --------------------- |
| **Hassasiyet**     | Düşük (on/off) | Yüksek (analog) | Çok Yüksek (analog)   |
| **Oyun Desteği**   | Basit oyunlar  | Xbox oyunları   | TÜM oyunlar           |
| **Algılanma**      | Klavye         | Xbox 360 Pad    | Racing Wheel 🏎️       |
| **Force Feedback** | ❌             | ❌              | ✅ (opsiyonel)        |
| **Kurulum**        | Kolay          | Kolay           | Orta (driver gerekli) |
| **Uyumluluk**      | Orta           | İyi             | Mükemmel              |
| **Profesyonellik** | Düşük          | Orta            | Yüksek                |

## 🏁 vJoy Avantajları:

1. **Gerçek Direksiyon Olarak Algılanır**

   - Oyunlar bunu "Racing Wheel" olarak görür
   - Logitech G29, Thrustmaster gibi görünür

2. **Daha Fazla Özelleştirme**

   - Force feedback desteği
   - Birden fazla eksen
   - Butonlar, POV switch vb.

3. **Evrensel Uyumluluk**

   - DirectInput destekleyen TÜM oyunlar
   - Simülasyon oyunları (iRacing, rFactor)
   - Flight simülatörleri bile!

4. **Anti-Cheat Güvenli**
   - Gerçek donanım olarak algılanır
   - Hiçbir oyun engellemez

## ⚠️ Dikkat Edilmesi Gerekenler:

1. **Driver Kurulumu Zorunlu**

   - Windows driver yükleme izni gerekli
   - Yönetici hakları şart

2. **Yeniden Başlatma**

   - Kurulumdan sonra bilgisayarı restart edin

3. **Yapılandırma**
   - vJoy Configure ile device'ı aktif edin
   - Eksen sayısını ayarlayın

## 🚀 Kurulum Sonrası:

1. ✅ Driver kuruldu
2. ✅ vJoy Configure'da device aktif edildi
3. ✅ joy.cpl'de vJoy Device görünüyor
4. ✅ `pip install pyvjoy` çalıştırıldı

**Şimdi Python kodunu güncelleyebiliriz!**

## 📝 Notlar:

- vJoy en profesyonel çözümdür
- Simracing topluluğu tarafından yaygın kullanılır
- FFB wheel'ler ile birlikte kullanılabilir
- 16 bit hassasiyet (0-32768 değer aralığı)

## 🔗 Kaynaklar:

- vJoy GitHub: https://github.com/njz3/vJoy
- pyvjoy Dokümantasyon: https://github.com/tidzo/pyvjoy
- vJoy Forum: http://vjoystick.sourceforge.net/

---

**Kurulum tamamlandıktan sonra Python kodunu güncelleyeceğiz!**
