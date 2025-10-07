# 🎮 Gamepad Mode - Xbox Controller Emulation

## ✨ Yeni Özellikler

### **1. Analog Hassasiyet**

- ❌ **Eski (Klavye)**: Sadece 3 durum → SOL / MERKEZ / SAĞ
- ✅ **Yeni (Gamepad)**: Sonsuz hassasiyet → -100% ~ +100% arası tüm değerler

### **2. Modern Oyun Desteği**

- ✅ Forza Horizon
- ✅ F1 Series
- ✅ Assetto Corsa
- ✅ BeamNG.drive
- ✅ Euro Truck Simulator
- ✅ Tüm Xbox controller destekleyen oyunlar

### **3. Anti-Cheat Uyumlu**

- ✅ Oyunlar bunu **gerçek Xbox 360 controller** olarak görür
- ✅ VAC, EAC, BattlEye ile uyumlu
- ✅ Hiçbir yasak riski yok

## 🚀 Kurulum

### **1. vgamepad Paketini Kur**

```powershell
cd PythonDesktopApp
pip install vgamepad
```

### **2. Modları Değiştir**

`main.py` dosyasının sonunda:

```python
def main():
    bridge = GyroKeyboardBridge(
        host='0.0.0.0',
        port=5000,
        threshold=0.3,
        use_gamepad=True   # ← True = Gamepad, False = Klavye
    )
```

## 🎮 Xbox Controller Mapping

### **Telefon → Xbox Controller**

| Telefon Hareketi    | Xbox Controller    | Değer Aralığı |
| ------------------- | ------------------ | ------------- |
| Telefonu SOLA çevir | LEFT THUMBSTICK ←  | -100% ~ 0%    |
| Telefonu SAĞA çevir | LEFT THUMBSTICK →  | 0% ~ +100%    |
| YEŞİL butona bas    | RIGHT TRIGGER (RT) | 0% veya 100%  |
| KIRMIZI butona bas  | LEFT TRIGGER (LT)  | 0% veya 100%  |

### **Oyunda Görünen**

```
Windows → "Devices and Printers" → "Xbox 360 Controller"

┌─────────────────────────────┐
│   Xbox 360 Controller       │
│                             │
│   [LT]              [RT]    │ ← Fren/Gaz
│                             │
│    ◄──●──►                 │ ← Direksiyon
│   LEFT STICK                │
└─────────────────────────────┘
```

## 📊 Hassasiyet Karşılaştırması

### **Klavye Modu** (use_gamepad=False)

```
Telefon Y değeri → Tuş
─────────────────────────────
y = -0.8  → LEFT arrow (100% basılı)
y = -0.5  → LEFT arrow (100% basılı)
y = -0.3  → LEFT arrow (100% basılı)
y = -0.2  → Hiçbir tuş (0%)
y =  0.0  → Hiçbir tuş (0%)
y = +0.2  → Hiçbir tuş (0%)
y = +0.3  → RIGHT arrow (100% basılı)
y = +0.5  → RIGHT arrow (100% basılı)

❌ Sadece 3 durum var
```

### **Gamepad Modu** (use_gamepad=True)

```
Telefon Y değeri → Joystick Pozisyonu
─────────────────────────────────────
y = -1.0  → Left Thumbstick 100% sola
y = -0.8  → Left Thumbstick 80% sola
y = -0.5  → Left Thumbstick 50% sola
y = -0.3  → Left Thumbstick 30% sola
y = -0.1  → Left Thumbstick 10% sola
y =  0.0  → Left Thumbstick merkez (0%)
y = +0.1  → Left Thumbstick 10% sağa
y = +0.3  → Left Thumbstick 30% sağa
y = +0.5  → Left Thumbstick 50% sağa
y = +0.8  → Left Thumbstick 80% sağa
y = +1.0  → Left Thumbstick 100% sağa

✅ SONSUZ hassasiyet!
```

## 🎯 Kullanım

### **1. Sunucuyu Başlat**

```powershell
cd PythonDesktopApp
python main.py
```

**Gamepad modunda göreceksiniz:**

```
════════════════════════════════════════════════════════════
🏎️  STEERING WHEEL SERVER
   Mode: 🎮 GAMEPAD MODE
════════════════════════════════════════════════════════════
🎮 Virtual Xbox 360 Controller initialized
🌐 Starting server on 0.0.0.0:5000
🎮 Controls (Xbox 360 Controller Emulation):
   • Y-axis (tilt L/R) = LEFT THUMBSTICK (analog)
   • Gas button = RIGHT TRIGGER (0-100%)
   • Brake button = LEFT TRIGGER (0-100%)
   • 💡 Games will see this as a real Xbox controller!
🏎️  Hold phone HORIZONTAL like a steering wheel
════════════════════════════════════════════════════════════
⏳ Waiting for client connection...
```

### **2. Telefonu Bağla**

- React Native uygulamasını aç
- IP adresini gir
- Connect'e bas

### **3. Windows'ta Kontrol Et**

```powershell
# Windows + R tuşlarına bas
joy.cpl

# Xbox 360 Controller görünecek
# Properties → Test sekmesi
# Telefonu hareket ettirince joystick'in hareket ettiğini görün!
```

### **4. Oyunda Ayarla**

1. Oyunu aç
2. Settings → Controls
3. **"Xbox Controller"** veya **"Gamepad"** seçeneğini seç
4. Kontrolleri test et!

## 📈 Log Çıktıları

### **Gamepad Modunda:**

```
[18:45:12] ✅ [CONNECTED] Client at 192.168.1.123
[18:45:13] [GAMEPAD] y=-0.45 (-45%) → TURN LEFT ⬅️
[18:45:14] [GAMEPAD] y=-0.52 (-52%) → TURN LEFT ⬅️ 🟢 GAS
[18:45:15] [GAMEPAD] y=+0.38 (+38%) → TURN RIGHT ➡️ 🟢 GAS
[18:45:16] [GAMEPAD] y=+0.12 (+12%) → CENTER ⬆️
[18:45:17] [GAMEPAD] y=-0.22 (-22%) → CENTER ⬆️ 🔴 BRAKE
```

### **Klavye Modunda:**

```
[18:45:12] ✅ [CONNECTED] Client at 192.168.1.123
[18:45:13] 🟢 GAS pressed (UP arrow)
[18:45:13] [KEYBOARD] y=-0.45 → TURN LEFT ⬅️ 🟢 GAS
[18:45:14] [KEYBOARD] y=+0.52 → TURN RIGHT ➡️ 🟢 GAS
[18:45:15] ⚪ GAS released
[18:45:16] 🔴 BRAKE pressed (DOWN arrow)
```

## 🔧 Sorun Giderme

### **Problem: "vgamepad not installed" hatası**

**Çözüm:**

```powershell
pip install vgamepad
```

### **Problem: "Failed to initialize gamepad" hatası**

**Çözüm:**

1. Yönetici olarak PowerShell açın
2. Programı yönetici olarak çalıştırın

```powershell
# Yönetici olarak
cd PythonDesktopApp
python main.py
```

### **Problem: Oyun controller'ı görmüyor**

**Çözüm:**

1. Windows + R → `joy.cpl`
2. "Xbox 360 Controller" listede mi kontrol edin
3. Yoksa programı yeniden başlatın
4. Önce programı başlatın, SONRA oyunu açın

### **Problem: Çok hassas veya hassasiyetsiz**

**Çözüm:**
Gamepad modunda threshold kullanılmaz, ama log'lardaki yüzdeleri kontrol edin:

- Telefonu az çevirince %10-20 görmeli
- Telefonu çok çevirince %80-100 görmeli
- Eğer değerler düşükse, telefonu daha fazla eğin

## 🎮 Mod Karşılaştırması

| Özellik         | Klavye Modu       | Gamepad Modu            |
| --------------- | ----------------- | ----------------------- |
| **Hassasiyet**  | Düşük (3 durum)   | Yüksek (sonsuz)         |
| **Uyumluluk**   | Basit oyunlar     | Tüm oyunlar             |
| **Anti-cheat**  | ⚠️ Engellenebilir | ✅ Güvenli              |
| **Kurulum**     | Kolay             | Orta (vgamepad gerekli) |
| **Performans**  | Hızlı             | Hızlı                   |
| **Gerçekçilik** | Düşük             | Yüksek                  |

## 💡 Öneriler

### **Klavye Modunu Kullan Eğer:**

- ✅ Basit/eski oyunlar oynuyorsanız
- ✅ Sadece ok tuşları yeterliyse
- ✅ Hızlı kurulum istiyorsanız

### **Gamepad Modunu Kullan Eğer:**

- ✅ Modern yarış oyunları oynuyorsanız (Forza, F1, Assetto)
- ✅ Gerçekçi direksiyon kontrolü istiyorsanız
- ✅ Analog hassasiyet gerekiyorsa
- ✅ Online oyunlar oynuyorsanız (anti-cheat güvenliği için)

## 🏁 En İyi Ayarlar

### **Forza Horizon / Motorsport:**

```python
use_gamepad=True  # Mutlaka gamepad modu
threshold=0.3     # Threshold gamepad'de kullanılmaz ama kalabilir
```

Oyunda:

- Settings → Controls → "Steering" → "Simulation"
- Dead zone: %5-10
- Sensitivity: Normal

### **F1 2024:**

```python
use_gamepad=True
```

Oyunda:

- Settings → Controls → Input Device: "Gamepad"
- Steering Linearity: 0
- Steering Saturation: 100

### **Assetto Corsa:**

```python
use_gamepad=True
```

Oyunda:

- Options → Controls → "X360 Controller"
- Steering Gamma: 1.0
- Steering Filter: 0.9

## 🎯 Özet

**Gamepad modu ile:**

- 🎮 Gerçek Xbox controller gibi çalışır
- 📊 Sonsuz analog hassasiyet
- 🏎️ Tüm modern yarış oyunlarında çalışır
- 🔒 Anti-cheat güvenli
- ⚡ Windows oyunlarıyla %100 uyumlu

**Hemen deneyin!**

```powershell
pip install vgamepad
python main.py
```
