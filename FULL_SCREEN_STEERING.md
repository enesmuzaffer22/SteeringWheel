# 🏎️ Tam Ekran Direksiyon Kontrolü

## 🎮 Yeni Özellikler

### 📱 React Native App

- ✅ Bağlandıktan sonra **TAM EKRAN** direksiyon modu
- ✅ **Landscape (Yatay)** ekran
- ✅ **GAZ Butonu** (Sağda - Yeşil) → Klavyede UP arrow ↑
- ✅ **FREN Butonu** (Solda - Kırmızı) → Klavyede DOWN arrow ↓
- ✅ **Direksiyon** (Ortada) → Y ekseni ile kontrol
- ✅ **Disconnect** butonu (Sol üst köşe)

### 💻 Python Desktop App

- ✅ Gas/Brake buton desteği
- ✅ UP arrow = Gaz pedali
- ✅ DOWN arrow = Fren pedali
- ✅ LEFT/RIGHT arrow = Direksiyon
- ✅ Tüm butonlar bağımsız çalışır

## 🎯 Kullanım

### 1. Bağlantı Ekranı (Portrait Mode)

```
┌─────────────┐
│   BAŞLIK    │
│   IP GİR    │
│  CONNECT    │
└─────────────┘
```

### 2. Direksiyon Ekranı (Landscape Mode - Connect sonrası)

```
Telefonu YATAY tut:

     [Disconnect]

┌──────────────────────────────────────┐
│                                      │
│  [FREN]    🏎️ STEERING    [GAZ]    │
│   🔴       Y: +0.23        🟢       │
│   ↓         CENTER          ↑       │
│  LEFT                      RIGHT    │
│                                      │
└──────────────────────────────────────┘
      📡 Connected • HORIZONTAL 🏎️
```

## ⌨️ Klavye Mapping

| Aksiyon  | Telefon                    | Klavye   |
| -------- | -------------------------- | -------- |
| Sola Dön | Telefonu sola çevir        | ⬅️ LEFT  |
| Sağa Dön | Telefonu sağa çevir        | ➡️ RIGHT |
| Gaz      | Sağdaki yeşil butona bas   | ⬆️ UP    |
| Fren     | Soldaki kırmızı butona bas | ⬇️ DOWN  |

## 🎨 Ekran Özellikleri

### Fren Butonu (Sol)

- **Renk**: Kırmızı (#F44336)
- **İkon**: 🔻
- **Label**: BRAKE
- **Tuş**: ↓
- **Boyut**: Ekranın ~25% genişlik, %70 yükseklik
- **Press Efekti**: Opacity 0.6, scale 0.95

### Gaz Butonu (Sağ)

- **Renk**: Yeşil (#4CAF50)
- **İkon**: 🔺
- **Label**: GAS
- **Tuş**: ↑
- **Boyut**: Ekranın ~25% genişlik, %70 yükseklik
- **Press Efekti**: Opacity 0.6, scale 0.95

### Merkez Bilgi Alanı

- **Başlık**: 🏎️ STEERING (32px)
- **Durum**: LEFT ⬅️ / CENTER / RIGHT ➡️ (28px, turuncu)
- **Y Değeri**: Real-time display
- **Arka Plan**: Siyah (#000)

### Disconnect Butonu

- **Pozisyon**: Sol üst köşe
- **Renk**: Kırmızı (opacity 0.8)
- **Fonksiyon**: Bağlantıyı keser ve bağlantı ekranına döner

## 🔧 Teknik Detaylar

### Data Payload (WebSocket)

```json
{
  "x": 0.123,
  "y": -0.456,
  "z": 0.012,
  "gas": true,
  "brake": false
}
```

### Python Handling

```python
def process_gyro_data(self, x, y, z, gas=False, brake=False):
    # Steering (Y axis)
    if y < -0.3: press LEFT
    elif y > 0.3: press RIGHT
    else: release steering

    # Gas button
    if gas: press UP
    else: release UP

    # Brake button
    if brake: press DOWN
    else: release DOWN
```

## 🚀 Başlatma Sırası

1. **PC'de Python app çalıştır**:

   ```powershell
   cd PythonDesktopApp
   python main.py
   ```

2. **Telefonda React Native app aç**:

   - Portrait modda başlar
   - IP adresini gir
   - "Connect" butonuna bas

3. **Otomatik Landscape'e geçer**:

   - Tam ekran direksiyon modu
   - Telefonu yatay tut
   - Sola/sağa çevir = Direksiyon
   - Sağ butona bas = Gaz
   - Sol butona bas = Fren

4. **Oyun Oyna!** 🏎️

## 📊 Beklenen Log Çıktısı (Python)

```
[18:45:12] ✅ [CONNECTED] Client at 192.168.1.123
[18:45:13] [DATA] y=-0.45 → TURN LEFT ⬅️
[18:45:13] 🟢 GAS pressed (UP arrow)
[18:45:14] [DATA] y=+0.52 → TURN RIGHT ➡️ 🟢 GAS
[18:45:15] ⚪ GAS released
[18:45:15] 🔴 BRAKE pressed (DOWN arrow)
[18:45:16] [DATA] y=+0.12 → CENTER ⬆️ 🔴 BRAKE
```

## 💡 İpuçları

1. **Landscape Zorunlu**: Telefonu mutlaka YATAY tutun
2. **Butonlar Bağımsız**: Gaz+Fren+Direksiyon aynı anda çalışabilir
3. **Yumuşak Geçişler**: Direksiyon için ani değil, yumuşak dönüşler
4. **Test İçin**: Notepad açıp ok tuşlarını test edin
5. **Disconnect**: Sol üst köşeden bağlantıyı kesebilirsiniz

## ⚠️ Sorun Giderme

**Problem**: Connect sonrası ekran değişmiyor

- **Çözüm**: App'i tamamen kapatıp yeniden açın

**Problem**: Butonlar çalışmıyor

- **Çözüm**: Python app'in çalıştığından emin olun

**Problem**: Direksiyon ters çalışıyor

- **Çözüm**: Telefonu 180° döndürün veya threshold'ları tersine çevirin

**Problem**: Ekran portrait'e dönüyor

- **Çözüm**: Telefonun otomatik döndürme ayarını açın

## 🎮 Oyun Ayarları

Çoğu yarış oyununda:

- **↑ UP** = Gaz / İleri
- **↓ DOWN** = Fren / Geri
- **← LEFT** = Sola dön
- **→ RIGHT** = Sağa dön

Oyununuzun ayarlarında bu tuşları kontrol edin!
