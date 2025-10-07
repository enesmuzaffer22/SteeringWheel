# 🧪 Test Rehberi - Direksiyon Uygulaması

## ✅ Yapılan Düzeltmeler

### 1. **Buton Durumları Artık Sunucuya İletiliyor**

- ✅ `isGasPressedRef` ve `isBrakePressedRef` eklendi
- ✅ `sendGyroData()` fonksiyonu ref'leri kullanıyor
- ✅ Her buton press/release anında ref güncellenıyor
- ✅ WebSocket payload'ına `gas` ve `brake` boolean değerleri eklendi

### 2. **Otomatik Ekran Yönlendirmesi**

- ✅ `expo-screen-orientation` paketi yüklendi
- ✅ Bağlanınca **LANDSCAPE** (yatay) moduna kilitlenir
- ✅ Disconnect olunca **PORTRAIT** (dikey) moduna döner
- ✅ useEffect ile otomatik yönetiliyor

## 🚀 Test Adımları

### 1. Python Desktop App'i Başlat

```powershell
cd PythonDesktopApp
python main.py
```

**Beklenen Çıktı:**

```
============================================================
🎮 Accelerometer to Keyboard Bridge Server
============================================================
🌐 Starting server on 0.0.0.0:5000
📊 Steering threshold: ±0.3
⌨️  Key mapping:
   • y < -0.3 = LEFT arrow
   • y > 0.3 = RIGHT arrow
   • Gas button = UP arrow
   • Brake button = DOWN arrow
🏎️  Hold phone HORIZONTAL like a steering wheel
============================================================
⏳ Waiting for client connection...
```

### 2. React Native App'i Aç

- Telefondan uygulamayı aç
- **Portrait (dikey)** modda açılmalı
- IP adresini gir
- "Connect" butonuna bas

### 3. Otomatik Landscape'e Geçiş

- Connect butonuna bastıktan sonra...
- ✅ Ekran **otomatik olarak YATAY** dönmeli
- ✅ Tam ekran direksiyon modu açılmalı
- ✅ Sol ve sağda butonlar görünmeli

### 4. Buton Testleri

#### Test 1: GAZ Butonu (Yeşil - Sağda)

1. Yeşil butona BAS ve TUT
2. **Python Console'da şunu görmelisiniz:**
   ```
   [18:45:13] 🟢 GAS pressed (UP arrow)
   [18:45:13] [DATA] y=+0.12 → CENTER ⬆️ 🟢 GAS
   ```
3. Butonu BIRAK
4. **Python Console'da şunu görmelisiniz:**
   ```
   [18:45:15] ⚪ GAS released
   ```

#### Test 2: FREN Butonu (Kırmızı - Solda)

1. Kırmızı butona BAS ve TUT
2. **Python Console'da şunu görmelisiniz:**
   ```
   [18:45:20] 🔴 BRAKE pressed (DOWN arrow)
   [18:45:20] [DATA] y=+0.08 → CENTER ⬆️ 🔴 BRAKE
   ```
3. Butonu BIRAK
4. **Python Console'da şunu görmelisiniz:**
   ```
   [18:45:22] ⚪ BRAKE released
   ```

#### Test 3: Direksiyon + Gaz

1. Telefonu SOLA çevir
2. Aynı anda GAZ butonuna bas
3. **Python Console'da şunu görmelisiniz:**
   ```
   [18:45:25] [DATA] y=-0.45 → TURN LEFT ⬅️
   [18:45:25] 🟢 GAS pressed (UP arrow)
   [18:45:26] [DATA] y=-0.52 → TURN LEFT ⬅️ 🟢 GAS
   ```

#### Test 4: Tüm Kontroller Birlikte

1. Telefonu SAĞA çevir
2. FREN butonuna bas
3. **Python Console'da şunu görmelisiniz:**
   ```
   [18:45:30] [DATA] y=+0.51 → TURN RIGHT ➡️
   [18:45:30] 🔴 BRAKE pressed (DOWN arrow)
   [18:45:31] [DATA] y=+0.48 → TURN RIGHT ➡️ 🔴 BRAKE
   ```

### 5. Disconnect Testi

1. Sol üst köşedeki "✕ Disconnect" butonuna bas
2. ✅ WebSocket bağlantısı kesilmeli
3. ✅ Ekran **otomatik olarak DİKEY** dönmeli
4. ✅ Bağlantı ekranına dönmeli
5. **Python Console'da şunu görmelisiniz:**
   ```
   [18:45:35] ❌ [DISCONNECTED] Client at 192.168.1.123
   [18:45:35] 🔓 Released LEFT arrow
   [18:45:35] 🔓 Released RIGHT arrow
   [18:45:35] 🔓 Released UP arrow (gas)
   [18:45:35] 🔓 Released DOWN arrow (brake)
   [18:45:35] 🛑 [CLEANUP] Released all keys for 192.168.1.123
   ```

## 📊 WebSocket Payload Formatı

```json
{
  "x": 0.123,
  "y": -0.456,
  "z": 0.012,
  "gas": true, // ← GAZ butonu durumu
  "brake": false // ← FREN butonu durumu
}
```

## 🔍 Beklenen Davranışlar

### Ekran Yönlendirmesi

| Durum         | Ekran Yönü        | Görünüm           |
| ------------- | ----------------- | ----------------- |
| Disconnected  | Portrait (Dikey)  | Bağlantı ekranı   |
| Connecting... | Portrait (Dikey)  | Bağlantı ekranı   |
| Connected     | Landscape (Yatay) | Direksiyon ekranı |

### Buton Durumları

| Aksiyon    | Telefon              | WebSocket        | Python Log        | Klavye     |
| ---------- | -------------------- | ---------------- | ----------------- | ---------- |
| Gaz Bas    | Yeşil butona bas     | `"gas": true`    | 🟢 GAS pressed    | ⬆️ basılı  |
| Gaz Bırak  | Yeşil butonu bırak   | `"gas": false`   | ⚪ GAS released   | ⬆️ serbest |
| Fren Bas   | Kırmızı butona bas   | `"brake": true`  | 🔴 BRAKE pressed  | ⬇️ basılı  |
| Fren Bırak | Kırmızı butonu bırak | `"brake": false` | ⚪ BRAKE released | ⬇️ serbest |

### Direksiyon Durumları

| Aksiyon    | Y Değeri        | Python Log    | Klavye             |
| ---------- | --------------- | ------------- | ------------------ |
| Sola çevir | y < -0.3        | TURN LEFT ⬅️  | ⬅️ basılı          |
| Sağa çevir | y > +0.3        | TURN RIGHT ➡️ | ➡️ basılı          |
| Merkez     | -0.3 < y < +0.3 | CENTER ⬆️     | Tüm tuşlar serbest |

## ⚠️ Olası Sorunlar ve Çözümler

### Sorun 1: Buton durumu görünmüyor

**Belirti:** Python console'da 🟢/🔴 emoji'leri görünmüyor
**Çözüm:**

- React Native uygulamasını tamamen kapatıp yeniden açın
- Shake yapıp "Reload" yeterli DEĞİL, tamamen kapatın

### Sorun 2: Ekran yönü değişmiyor

**Belirti:** Connect sonrası ekran dikey kalıyor
**Çözüm:**

- Telefonun "Otomatik döndürme" ayarını AÇIN
- Uygulamayı yeniden başlatın
- `npm install expo-screen-orientation` komutu çalıştırıldı mı kontrol edin

### Sorun 3: Gas/Brake false olarak görünüyor

**Belirti:** WebSocket payload'da her zaman `"gas": false, "brake": false`
**Çözüm:**

- `isGasPressedRef.current` ve `isBrakePressedRef.current` kullanıldığından emin olun
- App.js'deki değişikliklerin kaydedildiğinden emin olun

### Sorun 4: Klavye tuşları basılmıyor

**Belirti:** Python log'ları doğru ama oyunda tepki yok
**Test:**

1. Notepad açın
2. Uygulamayı çalıştırın
3. Butonlara basın
4. Notepad'de ok tuşlarının çalıştığını görmelisiniz

## 📝 Test Checklist

- [ ] Python server başladı
- [ ] React Native app açıldı (portrait)
- [ ] IP adresi girildi
- [ ] Connect butonuna basıldı
- [ ] Ekran otomatik yatay döndü
- [ ] Tam ekran direksiyon modu açıldı
- [ ] Telefonu sola çevirince Python log'da "TURN LEFT ⬅️" görünüyor
- [ ] Telefonu sağa çevirince Python log'da "TURN RIGHT ➡️" görünüyor
- [ ] Yeşil butona basınca Python log'da "🟢 GAS pressed" görünüyor
- [ ] Kırmızı butona basınca Python log'da "🔴 BRAKE pressed" görünüyor
- [ ] Gaz+Direksiyon aynı anda çalışıyor (log'da 🟢 GAS görünüyor)
- [ ] Fren+Direksiyon aynı anda çalışıyor (log'da 🔴 BRAKE görünüyor)
- [ ] Disconnect butonuna basınca ekran dikey dönüyor
- [ ] Disconnect sonrası bağlantı ekranına dönüyor

## 🎮 Gerçek Oyunda Test

1. Bir yarış oyunu açın (örn: Asphalt, Need for Speed)
2. Oyun ayarlarından kontrol şemasını "Klavye" yapın
3. Tuş atamaları:
   - İleri/Gaz: UP arrow ⬆️
   - Geri/Fren: DOWN arrow ⬇️
   - Sol: LEFT arrow ⬅️
   - Sağ: RIGHT arrow ➡️
4. Uygulamayı bağlayın
5. Oynayın! 🏎️

## 💡 İpuçları

1. **Hassasiyet Ayarı**: Python'da `threshold=0.3` yerine `threshold=0.2` daha hassas
2. **Smooth Steering**: Telefonu yumuşak çevirin, ani hareketler yapmayın
3. **Button Response**: Butonlara basıp çekerken Python log'larını izleyin
4. **Network Delay**: WiFi bağlantısı ~50ms gecikme normal
5. **Battery Saver**: Telefonda pil tasarrufu modunu KAPATIN

Başarılar! 🏁
