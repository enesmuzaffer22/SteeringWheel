# vJoy Sorun Giderme Kılavuzu

## 🎯 Sorun: Telefon sunucuya veri gönderiyor ama oyun/joy.cpl hareket algılamıyor

Bu sorun genellikle vJoy cihazının düzgün yapılandırılmadığında veya aktif olmadığında ortaya çıkar.

---

## 📋 ADIM 1: vJoy Tanılama Testi

Önce vJoy'un düzgün çalışıp çalışmadığını kontrol edelim:

```powershell
cd PythonDesktopApp
python diagnose_vjoy.py
```

### ✅ Tüm testler geçerse:

- "✅ TÜM TESTLER BAŞARILI!" mesajını göreceksiniz
- Adım 3'e geçin

### ❌ Hata alırsanız:

- Script size tam olarak ne yapmanız gerektiğini söyleyecek
- Önerileri uygulayın ve tekrar çalıştırın

---

## 📋 ADIM 2: Configure vJoy Kontrolü

1. **Başlat menüsünde "Configure vJoy" arayın ve açın**

2. **Sol tarafta "Device 1" seçin**

3. **Şu ayarların işaretli olduğunu kontrol edin:**

   - ✅ Enable vJoy
   - ✅ X-Axis (Direksiyon için)
   - ✅ Y-Axis (Gaz için)
   - ✅ Z-Axis (Fren için)

4. **"Apply" butonuna tıklayın**

5. **Bilgisayarı YENIDEN BAŞLATIN** (önemli!)

---

## 📋 ADIM 3: Hızlı Canlı Test

vJoy'un gerçekten çalıştığını görmek için:

```powershell
python quick_vjoy_test.py
```

### Test sırasında:

1. Script başladığında **Windows + R** → **joy.cpl** yazın
2. **vJoy Device** seçin
3. **Properties** tıklayın
4. Script'e dönüp **Enter** basın
5. **Eksenlerin hareket ettiğini izleyin!**

### ✅ Eksenler hareket ederse:

- vJoy çalışıyor! Adım 4'e geçin

### ❌ Eksenler hareket etmezse:

- joy.cpl'yi kapatıp tekrar açın
- Configure vJoy'da ayarları tekrar kontrol edin
- Bilgisayarı yeniden başlatın
- `python diagnose_vjoy.py` tekrar çalıştırın

---

## 📋 ADIM 4: Sunucuyu Başlatın

```powershell
python main.py
```

### Görmeli olduğunuz mesajlar:

```
✅ Device 1 başarıyla alındı
🎮 vJoy Device #1 başlatıldı!
🔍 Eksenler test ediliyor...
✅ Tüm eksenler çalışıyor!
⏳ Waiting for connection...
```

### ❌ Hata alırsanız:

- Script size tam çözümü gösterecek
- `python diagnose_vjoy.py` çalıştırın
- Configure vJoy ayarlarını kontrol edin

---

## 📋 ADIM 5: Telefonu Bağlayın ve Test Edin

### A) joy.cpl ile Test:

1. **joy.cpl'yi açık tutun:**

   - Windows + R → joy.cpl
   - vJoy Device → Properties

2. **Telefonu bağlayın:**

   - React Native uygulamasını açın
   - Sunucu IP'sini girin (örn: ws://192.168.1.251:5000)
   - Connect

3. **Telefonu YATAY tutun (landscape)**

4. **Telefonu sağa-sola eğin:**

   - joy.cpl'de **X-Axis** hareket etmeli
   - Sunucu konsolunda **[WHEEL]** mesajları görmeli

5. **Gas ve Brake butonlarına basın:**
   - joy.cpl'de **Y-Axis** (gas) ve **Z-Axis** (brake) hareket etmeli

### ✅ joy.cpl'de hareket görüyorsanız:

**vJoy TAM ÇALIŞIYOR!** Oyunda kullanmaya hazırsınız.

### ❌ Hareket görmüyorsanız:

**Sunucu konsolunu kontrol edin:**

- `[WHEEL]` mesajları var mı?
  - **VARSA:** vJoy sorunu var, Adım 2'ye dönün
  - **YOKSA:** Telefon-sunucu bağlantı sorunu

**Telefon bağlantısı sorunları için:**

- Telefon ve PC aynı Wi-Fi'de mi?
- IP adresi doğru mu? (PowerShell → `ipconfig`)
- Firewall vJoy'u engelliyor olabilir (Windows Defender kapatmayı deneyin)

---

## 📋 ADIM 6: Oyunda Kullanın

### Oyunu Başlatmadan Önce:

1. ✅ `python main.py` çalışıyor
2. ✅ Telefon bağlı
3. ✅ joy.cpl'de hareket görüyorsunuz

### Oyun Ayarları:

1. **Settings/Options → Controls/Input**
2. **Controller/Gamepad seçeneğine gidin**
3. **vJoy Device'ı seçin**
4. **Kontrolleri ayarlayın:**
   - **Steering (Direksiyon)** → X-Axis
   - **Throttle/Accelerate (Gaz)** → Y-Axis
   - **Brake (Fren)** → Z-Axis

### Popüler Oyun Örnekleri:

#### BeamNG.drive:

- Settings → Controls → Steering Wheel
- Device: vJoy Device
- Steering: X Axis
- Throttle: Y Axis
- Brake: Z Axis

#### Assetto Corsa:

- Options → Controls → Configure Controllers
- Select: vJoy Device
- Steering Axis: X
- Gas Axis: Y
- Brake Axis: Z

#### Euro Truck Simulator 2:

- Options → Controls → Edit Controls
- Steering Device: vJoy Device
- Steering: Axis X
- Throttle: Axis Y
- Brake: Axis Z

---

## 🆘 Hala Çalışmıyor mu?

### Kontrol Listesi:

**1. vJoy Driver Kurulu mu?**

```powershell
python diagnose_vjoy.py
```

**2. Configure vJoy Doğru mu?**

- Başlat → Configure vJoy
- Device 1: ✅ Enable, X, Y, Z

**3. Cihaz Meşgul mü?**

```powershell
python reset_vjoy.py
```

**4. joy.cpl'de Görünüyor mu?**

- Windows + R → joy.cpl
- "vJoy Device" listede var mı?

**5. Bilgisayar Yeniden Başlatıldı mı?**

- Ciddi değil gibi görünse de, genellikle çözüm budur!

---

## 🔧 Yaygın Sorunlar ve Çözümleri

### Sorun: "Device is BUSY"

**Çözüm:**

```powershell
python reset_vjoy.py
```

Veya joy.cpl'yi kapatın ve tekrar deneyin.

### Sorun: "Device is MISSING"

**Çözüm:**

1. Configure vJoy açın
2. Device 1'i etkinleştirin
3. Apply → Bilgisayarı yeniden başlatın

### Sorun: "Eksen hatası"

**Çözüm:**
Configure vJoy'da X, Y, Z eksenlerinin HEPSİNİN etkin olduğundan emin olun.

### Sorun: "Oyun vJoy'u görmüyor"

**Çözüm:**

1. Oyunu yeniden başlatın
2. Oyun ayarlarında "Refresh" veya "Detect" yapın
3. DirectInput desteği olan oyunlar vJoy'u görebilir
4. XInput-only oyunlar göremeyebilir (ViGEm gerektirir)

---

## 📞 Destek

Tüm adımları denediyseniz ve hala sorun yaşıyorsanız:

1. **Log dosyalarını toplayın:**

   - `python diagnose_vjoy.py > vjoy_log.txt`
   - `python main.py > server_log.txt`

2. **joy.cpl ekran görüntüsü:**

   - Windows + R → joy.cpl
   - vJoy Device Properties ekranı

3. **Configure vJoy ekran görüntüsü:**
   - Device 1 ayarları

Bu bilgilerle yardım isteyebilirsiniz.

---

## ✅ Başarı Kriteri

**Herşey çalışıyorsa şunları göreceksiniz:**

1. ✅ `python diagnose_vjoy.py` → Tüm testler başarılı
2. ✅ `python quick_vjoy_test.py` → joy.cpl'de eksenler hareket ediyor
3. ✅ `python main.py` → Telefon bağlanıyor
4. ✅ joy.cpl → Telefonu eğdiğinizde eksenler hareket ediyor
5. ✅ Oyun → Kontroller çalışıyor

**Hepsini gördüyseniz: TEBRIKLER! 🎉**
