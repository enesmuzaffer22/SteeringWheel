# APK Build Seçenekleri

## ✅ Mevcut Durum
Expo kullanıyorsunuz, bu yüzden APK almak için birkaç seçeneğiniz var:

---

## 🎯 Seçenek 1: EAS Build (Bulut - Kullandığınız)
**Artıları:**
- ✅ En kolay yöntem
- ✅ Hiçbir kurulum gerektirmez
- ✅ Her platformda çalışır

**Eksileri:**
- ❌ İnternet bağlantısı gerekir
- ❌ Build kuyruğu beklemesi olabilir

**Kullanım:**
```bash
eas build -p android --profile preview
```

---

## 🏠 Seçenek 2: Local Build (JDK + Android SDK Gerekli)
**Gereksinimler:**
1. JDK 17 kurulumu
2. Android SDK kurulumu
3. ANDROID_HOME environment variable

**Kurulum Adımları:**

### 1. JDK Kurulumu
- [JDK 17 İndirin](https://www.oracle.com/java/technologies/downloads/#java17)
- Yükleyin ve JAVA_HOME'u ayarlayın

### 2. Android Studio Kurulumu
- [Android Studio İndirin](https://developer.android.com/studio)
- SDK Manager'dan "Android SDK Command-line Tools" kurun

### 3. Environment Variables Ayarlayın
PowerShell'de (Admin olarak):
```powershell
# ANDROID_HOME ayarla
[System.Environment]::SetEnvironmentVariable("ANDROID_HOME", "C:\Users\YourName\AppData\Local\Android\Sdk", "Machine")

# JAVA_HOME ayarla (JDK yolunuza göre)
[System.Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Java\jdk-17", "Machine")

# Path'e ekle
$androidPath = "$env:ANDROID_HOME\platform-tools;$env:ANDROID_HOME\tools;$env:ANDROID_HOME\tools\bin"
[System.Environment]::SetEnvironmentVariable("Path", "$env:Path;$androidPath", "Machine")
```

### 4. APK Build
```bash
# Prebuild
npx expo prebuild --platform android --clean

# APK oluştur
cd android
.\gradlew assembleRelease

# APK burada olacak:
# android/app/build/outputs/apk/release/app-release.apk
```

---

## 🔧 Seçenek 3: Expo Application Services (Öneri)
EAS kullanmaya devam edin ama şu iyileştirmeleri yapın:

### app.json güncellendi:
```json
{
  "android": {
    "usesCleartextTraffic": true,
    "networkSecurityConfig": "network_security_config"
  }
}
```

### network_security_config.xml oluşturuldu:
Bu dosya cleartext (HTTP/WS) trafiğine izin veriyor.

---

## 🚀 ÖNERİ: EAS Kullanmaya Devam Edin

**Neden?**
1. ✅ Kolay ve hızlı
2. ✅ Her zaman güncel Android build tools
3. ✅ Hiçbir kurulum yok
4. ✅ Cross-platform

**Build komutu:**
```bash
eas build -p android --profile preview
```

**Build sonrası APK:**
Link veya QR kod ile doğrudan telefonunuza indirin.

---

## 🐛 Bağlantı Sorununu Çözmek İçin

Uygulamada **hata logları** ekledim. Yeni build aldığınızda:
1. APK'yı yükleyin
2. Sunucuya bağlanmayı deneyin
3. Hata mesajında şunlar gösterilecek:
   - Error Type
   - Error Message
   - Error Code
   - Server URL

Bu bilgilerle sorunu tam olarak tespit edebiliriz!

---

## 📝 Build Aldıktan Sonra Test

1. Python sunucuyu çalıştırın:
```bash
cd server
python server.py
```

2. PC'nizin IP adresini bulun:
```bash
ipconfig
```

3. Mobil uygulamada IP'yi girin:
```
ws://192.168.1.XXX:5000
```

4. Hata alırsanız, hata detaylarını paylaşın!
