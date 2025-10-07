# 🎮 Oyunlarda vJoy Algılanma Sorunu - Çözüm Rehberi

## ❓ Sorun

vJoy cihazı Windows'ta (joy.cpl) görünüyor ve eksenler hareket ediyor, **FAKAT** oyunlar vJoy'u algılamıyor veya tuşlara/eksenlere tepki vermiyor.

---

## ✅ ÇÖZÜM 1: Oyunu Yeniden Başlat (EN YAYGINI!)

**%90 durumda bu çözüm işe yarar!**

### Adımlar:

1. **Oyunu TAMAMEN kapat** (sadece menüye dönmek yetmez)
2. vJoy'un çalıştığını doğrula:
   - Windows + R → `joy.cpl`
   - vJoy Device → Properties
   - Eksenler hareket ediyor mu kontrol et
3. **Oyunu tekrar başlat**
4. Oyun ayarlarına git → Controls/Input

### Neden Bu Gerekli?

Çoğu oyun, kontrol cihazlarını **sadece başlangıçta** tarar. vJoy oyun açıldıktan sonra başlatılırsa, oyun onu göremez.

---

## ✅ ÇÖZÜM 2: Doğru Kontrol Modunu Seç

Oyun ayarlarında **yanlış mod** seçilmiş olabilir.

### Kontrol Et:

```
Oyun Ayarları → Input/Controls → Device Type
```

### ❌ Yanlış Seçimler:

- ❌ **Keyboard** modu
- ❌ **Gamepad** modu
- ❌ **Xbox Controller** modu

### ✅ Doğru Seçimler:

- ✅ **Steering Wheel** modu
- ✅ **Custom Controller** modu
- ✅ **Direct Input** modu
- ✅ **Wheel** modu

---

## ✅ ÇÖZÜM 3: Manuel Tuş Ataması Yap

Bazı oyunlar otomatik algılamaz, **manuel bind** gerektirir.

### Adımlar (Örnek: Forza Horizon 5):

1. Ayarlar → **Controls**
2. **Steering** seçeneğine tıkla
3. Telefonu **sağa-sola eğ** → Oyun algılamalı
4. **Throttle** seçeneğine tıkla
5. **GAS butonuna bas** → Oyun algılamalı
6. **Brake** seçeneğine tıkla
7. **BRAKE butonuna bas** → Oyun algılamalı

### Test İçin:

```
python main.py
```

Sonra telefonu bağla ve manuel binding sırasında:

- Steering için → Telefonu eğ
- Throttle için → GAS butonuna bas (ekranda loglarda göreceksin)
- Brake için → BRAKE butonuna bas

---

## ✅ ÇÖZÜM 4: Deadzone Ayarları

Oyun **deadzone** çok yüksek olabilir.

### Kontrol Et:

```
Oyun Ayarları → Controls → Advanced → Deadzone
```

### Önerilen Değerler:

- **Steering Deadzone:** 0-5%
- **Throttle Deadzone:** 0-3%
- **Brake Deadzone:** 0-3%

Eğer deadzone %20+ ise, küçük hareketler algılanmayacaktır!

---

## ✅ ÇÖZÜM 5: Oyun-Spesifik Ayarlar

### 🎮 Forza Horizon 5:

```
Settings → Controls & Vibration
1. Steering Axis → REVERSE (eğer ters gidiyorsa)
2. Steering Sensitivity → 50-70%
3. Steering Linearity → 50%
4. Force Feedback Scale → 0% (telefonda FF yok)
```

### 🎮 Assetto Corsa:

```
Options → Controls
1. Device → vJoy Device
2. Steering → Axis X
3. Throttle → Axis Y
4. Brake → Axis Z
5. Invert → Check if needed
```

### 🎮 BeamNG.drive:

```
Options → Controls → Bindings
1. Select 'vJoy Device'
2. Steering → X-Axis
3. Throttle → Y-Axis
4. Brake → Z-Axis
5. Test in Free Roam mode first
```

### 🎮 Euro Truck Simulator 2:

```
Options → Controls
1. Device → Wheel (vJoy Device)
2. Steering → Axis X
3. Accelerate → Axis Y
4. Brake → Axis Z
5. Combined pedals → OFF
```

---

## ✅ ÇÖZÜM 6: Steam Input Devre Dışı Bırak

**Eğer oyun Steam'den çalışıyorsa:**

Steam kendi controller layer'ını ekler, bu vJoy'u bozabilir.

### Adımlar:

1. Steam Library → Oyuna sağ tıkla
2. **Properties** → **Controller**
3. **Override for [Game Name]** → **Disable Steam Input**
4. Oyunu kapat ve yeniden başlat

---

## ✅ ÇÖZÜM 7: Administrator Olarak Çalıştır

Bazı anti-cheat sistemleri vJoy'u bloke edebilir.

### Test:

1. `main.py` dosyasına sağ tıkla
2. **Run as Administrator**
3. Oyunu da **Administrator** olarak başlat
4. Test et

---

## ✅ ÇÖZÜM 8: DirectInput vs XInput

vJoy **DirectInput** kullanır, bazı oyunlar **sadece XInput** destekler.

### XInput Gerektiren Oyunlar:

- Forza Horizon 4/5 (genelde)
- Need for Speed (bazı versiyonlar)
- Crew 2

### Çözüm:

**x360ce** kullan (DirectInput → XInput dönüştürücü):

```
1. İndir: https://www.x360ce.com/
2. Oyun klasörüne kopyala
3. vJoy Device'ı Xbox controller olarak map et
4. Oyunu başlat
```

**NOT:** Bu advanced bir yöntemdir, çoğu oyun DirectInput destekler.

---

## 🧪 Test: vJoy Gerçekten Çalışıyor mu?

Basit test için bu scripti çalıştır:

```bash
python test_axes.py
```

Aynı anda:

- Windows + R → `joy.cpl`
- vJoy Device → Properties
- **Eksenler hareket ediyor mu?**

### ✅ Hareket Ediyorsa:

vJoy çalışıyor! Sorun oyun ayarlarında.

### ❌ Hareket Etmiyorsa:

vJoy Python'dan veri almıyor. `main.py` loglarını kontrol et.

---

## 🎯 Önerilen Test Oyunu

**BeamNG.drive** en iyi test oyunudur çünkü:

- ✅ Her türlü controller'ı algılar
- ✅ DirectInput tam desteği
- ✅ Real-time axis görselleştirme
- ✅ Kolay binding menüsü

Eğer BeamNG'de çalışıyorsa, sorun diğer oyunların ayarlarındadır.

---

## 📊 Diagnostic Checklist

Test sırasında kontrol et:

- [ ] joy.cpl'de vJoy Device görünüyor
- [ ] Properties'de eksenler hareket ediyor
- [ ] `python main.py` çalışıyor ve log gösteriyor
- [ ] Telefon bağlandı (✅ CONNECTED mesajı)
- [ ] `[WHEEL] y=...` logları geliyor
- [ ] Oyun TAMAMEN kapatılıp yeniden açıldı
- [ ] Oyun ayarlarında "Steering Wheel" modu seçildi
- [ ] Deadzone değerleri düşük (%0-5)
- [ ] Steam Input disabled (Steam oyunlarında)

---

## 💡 Hızlı Test Komutu

vJoy çalışıp çalışmadığını anında görmek için:

```bash
python check_vjoy_config.py
```

Bu script:

- ✅ vJoy kurulumunu doğrular
- ✅ Axis yapılandırmasını kontrol eder
- ✅ Test verileri gönderir

---

## 🆘 Hala Çalışmıyorsa

### Son Çare Adımlar:

1. **Bilgisayarı yeniden başlat**
2. **vJoy'u kaldır ve tekrar kur:**
   - Settings → Apps → vJoy → Uninstall
   - PC'yi yeniden başlat
   - vJoy'u tekrar kur: https://github.com/njz3/vJoy/releases
   - Configure vJoy → Enable Device 1 → X/Y/Z axes
3. **Python paketlerini yeniden kur:**
   ```bash
   pip uninstall pyvjoy
   pip install pyvjoy
   ```
4. **Farklı bir oyunda test et** (BeamNG öneririm)

---

## 📝 Hangi Oyunu Kullanıyorsun?

Eğer spesifik bir oyunda sorun yaşıyorsan, oyunun adını söyle, o oyun için özel ayarları vereyim!

**Popüler Oyunlar:**

- Forza Horizon 5
- Assetto Corsa
- BeamNG.drive
- Euro Truck Simulator 2
- American Truck Simulator
- Project CARS 2
- F1 2024
- Gran Turismo (PC)
- Need for Speed

---

**Şu anda hangi oyunu test ediyorsun?** 🎮
