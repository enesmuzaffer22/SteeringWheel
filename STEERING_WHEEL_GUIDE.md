# 🏎️ Direksiyon Modu Kullanım Kılavuzu

## 📱 Telefonu Nasıl Tutmalısınız?

Telefonu **YATAY (Landscape)** modda, **direksiyon gibi** tutun:

```
        [Üst kısım]
    ┌───────────────┐
    │               │
    │   📱 EKRAN    │  ← Telefonu yatay tut
    │               │
    └───────────────┘
        [Alt kısım]

🔄 Sola çevir  →  SOL ok tuşu basılır  ⬅️
🔄 Sağa çevir  →  SAĞ ok tuşu basılır  ➡️
🔄 Düz tut     →  Hiçbir tuş basılmaz  ⬆️
```

## 🎮 Accelerometer Eksenleri

Telefon **YATAY** tutulduğunda:

- **Y ekseni** = Direksiyon dönüşü (SOL/SAĞ) 🎯

  - `y < -0.3` → SOL DÖNÜŞ ⬅️
  - `y > +0.3` → SAĞ DÖNÜŞ ➡️
  - `-0.3 < y < +0.3` → MERKEZ (düz)

- **X ekseni** = Yukarı/aşağı eğim (ileride gaz/fren için kullanılabilir)
- **Z ekseni** = Yerçekimi (~0.0 olmalı telefon yataydayken)

## ⚙️ Ayarlar

### Python Desktop App:

- **Threshold (Hassasiyet)**: `0.3`
- **Kullanılan Eksen**: Y ekseni (rotation)
- **Tuş Mapping**:
  - Sol ok tuşu: `keyboard.press('left')`
  - Sağ ok tuşu: `keyboard.press('right')`

### React Native Mobile App:

- **Sensör**: Accelerometer (Gyroscope DEĞİL!)
- **Update Rate**: 50ms (~20 Hz)
- **Veri Gönderme**: 50ms interval

## 🚀 Başlatma Adımları

1. **PC'de Python uygulamasını çalıştır:**

   ```powershell
   cd PythonDesktopApp
   python main.py
   ```

2. **Telefondan bağlan:**

   - React Native uygulamasını aç
   - PC'nin IP adresini gir (örn: `ws://192.168.1.251:5000`)
   - "Connect" butonuna bas

3. **Telefonu YATAY tut ve oyna!**
   - Sola çevir → Sol dönüş
   - Sağa çevir → Sağ dönüş

## 🔧 Hassasiyet Ayarlama

Eğer direksiyon çok hassas veya çok az hassassa:

**Python tarafında** (`main.py`):

```python
# Daha az hassas (daha fazla dönüş gerekli)
bridge = GyroKeyboardBridge(threshold=0.5)

# Daha hassas (az dönüşle tepki verir)
bridge = GyroKeyboardBridge(threshold=0.2)

# Varsayılan (dengeli)
bridge = GyroKeyboardBridge(threshold=0.3)
```

## 🎯 İpuçları

1. **Kalibrasyon**: Telefonu düz tuttuğunuzda Y değeri ~0.0 olmalı
2. **Pozisyon**: Telefonu rahat tutabileceğiniz bir pozisyon bulun
3. **Yumuşak Geçişler**: Ani hareketler yerine yumuşak dönüşler yapın
4. **Test**: Önce bir notepad açıp ok tuşlarının basıldığını test edin

## 📊 Beklenen Değerler

```
Düz tuttuğunuzda:
x ≈ 0.0, y ≈ 0.0, z ≈ 0.0

Sola çevirince:
y → -0.5 civarı (negatif)

Sağa çevirince:
y → +0.5 civarı (pozitif)
```

## ⚠️ Sorun Giderme

**Problem**: Veriler gelmiyor (hep 0.0)

- **Çözüm**: App'i tamamen kapatıp yeniden aç (shake → reload yeterli değil)

**Problem**: Ters yönde çalışıyor

- **Çözüm**: Python kodunda threshold işaretlerini değiştir (`y < -threshold` ↔ `y > threshold`)

**Problem**: Çok hassas/hassasiyetsiz

- **Çözüm**: Threshold değerini ayarla (0.2 - 0.5 arası)

**Problem**: Telefonu düz tutunca bile dönüyor

- **Çözüm**: Threshold'u artır (0.4 veya 0.5 yap)
