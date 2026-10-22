# 🚀 Quick Start - 5 Dakikada Çalıştır!

## Windows Kullanıcıları

### 1. Backend'i başlat
Çift tıkla: `start-backend.bat`

Terminal açılacak ve backend otomatik başlayacak.

### 2. Frontend'i başlat (Yeni terminal)
Çift tıkla: `start-frontend.bat`

Yeni terminal açılacak ve frontend otomatik başlayacak.

### 3. Tarayıcıda aç
http://localhost:5173

**Giriş bilgileri:**
- IT: `admin@company.com` / `admin123`
- Çalışan: `user@company.com` / `user123`

---

## Mac/Linux Kullanıcıları

### 1. Script'lere çalıştırma izni ver
```bash
chmod +x start-backend.sh
chmod +x start-frontend.sh
```

### 2. Backend'i başlat
```bash
./start-backend.sh
```

### 3. Frontend'i başlat (Yeni terminal)
```bash
./start-frontend.sh
```

### 4. Tarayıcıda aç
http://localhost:5173

---

## Manuel Kurulum İsterseniz

Detaylı adımlar için: `SETUP_GUIDE.md`

---

## Sorun mu yaşıyorsunuz?

### Backend başlamıyor
- Python 3.10+ yüklü mü? → `python --version`
- Port 8000 kullanımda mı? → Farklı port kullanın

### Frontend başlamıyor
- Node.js yüklü mü? → `node --version`
- `npm install` çalıştı mı?

### Daha fazla yardım
`SETUP_GUIDE.md` → Detaylı sorun giderme

---

## Test Kullanıcıları

| Rol | E-posta | Şifre |
|-----|---------|-------|
| IT Personeli | admin@company.com | admin123 |
| Çalışan | user@company.com | user123 |

---

## İlk Adımlar

1. ✅ **IT olarak giriş yap** → Dashboard'u incele
2. ✅ **Çalışan olarak giriş yap** → Yeni talep oluştur
3. ✅ **IT olarak talebi gör** → Kendine ata
4. ✅ **Yorum ekle** → Durumu güncelle
5. ✅ **Çalışan olarak kapat** → Talebi tamamla

---

## API Dokümantasyonu

Backend çalışırken: http://localhost:8000/docs

Swagger UI ile tüm endpoint'leri test edebilirsiniz!

---

## Testleri Çalıştır

```bash
cd backend
pytest
```

29 test geçmeli ✅

---

Hızlı başlangıç tamamlandı! 🎉

Detaylı dokümantasyon:
- `README.md` - Genel bilgi
- `SETUP_GUIDE.md` - Adım adım kurulum
- `FEATURES.md` - Geliştirme süreci
- `PROJECT_SUMMARY.md` - Proje özeti
