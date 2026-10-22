# IT Helpdesk System - Hızlı Başlangıç Rehberi

Bu rehber, projeyi sıfırdan kurmanız ve çalıştırmanız için adım adım talimatlar içerir.

## 📋 Ön Gereksinimler

Bilgisayarınızda şunların yüklü olması gerekiyor:

- **Python 3.10+** → [İndir](https://www.python.org/downloads/)
- **Node.js 16+** → [İndir](https://nodejs.org/)
- **Git** (opsiyonel) → [İndir](https://git-scm.com/)

Kurulu olup olmadığını kontrol edin:
```bash
python --version   # 3.10 veya üzeri olmalı
node --version     # 16 veya üzeri olmalı
npm --version
```

## 🚀 Adım 1: Backend Kurulumu

### 1.1 Backend klasörüne gidin
```bash
cd it-helpdesk-system/backend
```

### 1.2 Python sanal ortamı oluşturun

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Sanal ortam aktif olduğunda terminal başında `(venv)` göreceksiniz.

### 1.3 Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

Bu işlem 1-2 dakika sürebilir. FastAPI, SQLAlchemy, JWT ve diğer kütüphaneler yüklenecek.

### 1.4 Veritabanını başlatın
```bash
python init_db.py
```

Çıktı şöyle olmalı:
```
🗄️  Veritabanı tabloları oluşturuluyor...
✅ Tablolar başarıyla oluşturuldu!
✅ Test kullanıcıları başarıyla eklendi!
🎉 Veritabanı hazır! Backend'i başlatabilirsiniz.
```

### 1.5 Backend sunucusunu başlatın
```bash
uvicorn main:app --reload
```

✅ Backend başarıyla çalışıyor!
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

---

## 🎨 Adım 2: Frontend Kurulumu

**YENİ BİR TERMINAL AÇIN** (backend çalışmaya devam etsin!)

### 2.1 Frontend klasörüne gidin
```bash
cd it-helpdesk-system/frontend
```

### 2.2 Bağımlılıkları yükleyin
```bash
npm install
```

Bu işlem 2-3 dakika sürebilir. React, Vite, Axios ve diğer paketler yüklenecek.

### 2.3 Development sunucusunu başlatın
```bash
npm run dev
```

✅ Frontend başarıyla çalışıyor!
- **Uygulama**: http://localhost:5173

---

## 🎯 Adım 3: Uygulamayı Test Edin

### 3.1 Tarayıcıda açın
http://localhost:5173 adresine gidin.

### 3.2 Giriş yapın

**IT Personeli olarak:**
- E-posta: `admin@company.com`
- Şifre: `admin123`

**Çalışan olarak:**
- E-posta: `user@company.com`
- Şifre: `user123`

### 3.3 Özellikleri deneyin

**IT Personeli (admin@company.com) ile:**
- ✅ Tüm talepleri görüntüleyin
- ✅ İstatistikleri inceleyin
- ✅ Filtreleme yapın
- ✅ Bir talebi kendinize atayın
- ✅ Talep durumunu değiştirin

**Çalışan (user@company.com) ile:**
- ✅ Yeni talep oluşturun
- ✅ Kendi taleplerini görüntüleyin
- ✅ Talebe yorum ekleyin
- ✅ Çözülen talebi kapatın

---

## 🧪 Adım 4: Testleri Çalıştırın (Opsiyonel)

Backend klasöründe:
```bash
cd backend
pytest
```

**Beklenen çıktı:** 29 test başarıyla geçmeli ✅

---

## ⚠️ Sorun Giderme

### Backend başlamıyor

**Hata:** `ModuleNotFoundError: No module named 'fastapi'`
**Çözüm:** Sanal ortamı aktif ettiniz mi? `venv\Scripts\activate` (Windows) veya `source venv/bin/activate` (Mac/Linux)

**Hata:** `Address already in use` (Port 8000 kullanımda)
**Çözüm:** 
```bash
uvicorn main:app --reload --port 8001
```
Farklı port kullanın. Frontend'de `src/services/api.js` dosyasında `API_BASE_URL`'i değiştirin.

### Frontend başlamıyor

**Hata:** `command not found: npm`
**Çözüm:** Node.js'i yükleyin: https://nodejs.org/

**Hata:** `EACCES: permission denied`
**Çözüm:** 
```bash
npm install --legacy-peer-deps
```

### API bağlantı hatası

**Hata:** `Network Error` veya `ERR_CONNECTION_REFUSED`
**Çözüm:** 
1. Backend'in çalıştığından emin olun (http://localhost:8000/health)
2. CORS ayarlarını kontrol edin (`main.py`)
3. Tarayıcı console'unda hataları inceleyin (F12)

### Veritabanı hatası

**Hata:** `database is locked`
**Çözüm:** 
1. Backend sunucusunu durdurun (Ctrl+C)
2. `helpdesk.db` dosyasını silin
3. `python init_db.py` ile yeniden oluşturun

---

## 📚 Daha Fazla Bilgi

- **Veritabanı Şeması**: `backend/DATABASE_SCHEMA.md`
- **Geliştirme Süreci**: `FEATURES.md`
- **API Dokümantasyonu**: http://localhost:8000/docs (backend çalışırken)

---

## 🎉 Başarılı Kurulum!

Artık IT Helpdesk System'i kullanmaya hazırsınız!

**Tavsiyeler:**
1. Kod üzerinde değişiklik yaparken her iki terminal de açık olsun
2. Backend değişikliklerinde otomatik reload çalışır
3. Frontend değişikliklerinde de otomatik refresh olur (HMR)
4. Test kullanıcılarının şifrelerini production'da mutlaka değiştirin!

İyi çalışmalar! 🚀
