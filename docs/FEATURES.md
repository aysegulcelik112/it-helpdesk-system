# IT Destek Talep Sistemi - Geliştirme Aşamaları

Bu dosya, projenin geliştirme sürecini aşama aşama dokumente eder.

---

## ✅ Aşama 1: Proje İskeleti (Tamamlandı)

### Yapılanlar
Bu aşamada projenin temel klasör yapısı ve başlangıç konfigürasyonları oluşturuldu. Backend için Python/FastAPI, frontend için React/Vite teknolojileri seçildi ve gerekli dosyalar hazırlandı.

**Backend Yapısı:**
- `backend/` - Ana backend klasörü
  - `models/` - SQLAlchemy ORM modelleri için (User, Ticket, TicketComment)
  - `schemas/` - Pydantic şemaları için (API request/response validasyonu)
  - `routers/` - FastAPI endpoint'leri için (REST API routes)
  - `auth/` - JWT kimlik doğrulama ve şifre hash modülleri için
  - `tests/` - Pytest unit testleri için
  - `main.py` - FastAPI uygulamasının ana dosyası, CORS middleware eklendi
  - `database.py` - SQLAlchemy veritabanı bağlantı yapılandırması
  - `requirements.txt` - Python bağımlılıkları (FastAPI, SQLAlchemy, JWT, Pytest)
  - `.env` - Ortam değişkenleri (SECRET_KEY, database URL)

**Frontend Yapısı:**
- `frontend/` - Ana frontend klasörü
  - `src/components/` - React bileşenleri için
  - `src/pages/` - Sayfa bileşenleri için (Login, Dashboard, vb.)
  - `src/services/` - API servis katmanı (Axios)
  - `src/utils/` - Yardımcı fonksiyonlar ve sabitler
  - `main.jsx` - React uygulamasının giriş noktası
  - `App.jsx` - Ana uygulama bileşeni, router yapısı buraya eklenecek
  - `index.css` - Global CSS, Inter font, nötr renk paleti tanımlandı
  - `package.json` - NPM bağımlılıkları (React, React Router, Axios, Recharts)
  - `vite.config.js` - Vite yapılandırması, backend proxy ayarlandı

### Teknoloji Seçim Nedenleri

**FastAPI (Backend):**
- Modern Python web framework, otomatik API dokümantasyonu (Swagger UI)
- Async/await desteği ile yüksek performans
- Pydantic ile otomatik veri validasyonu
- Tip kontrolü (type hints) sayesinde daha az hata

**SQLAlchemy + SQLite:**
- SQLAlchemy: Python için en yaygın ORM, veritabanı işlemlerini kolaylaştırır
- SQLite: Kurulum gerektirmeyen dosya tabanlı veritabanı, staj projesi için ideal
- Geliştirme ortamında kolay taşınabilirlik

**React + Vite:**
- React: Bileşen tabanlı mimari, yeniden kullanılabilir UI parçaları
- Vite: Webpack'e göre çok daha hızlı geliştirme sunucusu (HMR)
- Modern JavaScript (ESM) desteği

**JWT Kimlik Doğrulama:**
- Stateless authentication, sunucuda session saklamaya gerek yok
- Token tabanlı sistem, mobil uygulama desteğine uygun
- Rol bilgisi token içinde taşınır, her istekte veritabanı sorgusu gerektirmez

**Inter Font + Nötr Renk Paleti:**
- Inter: Modern, okunabilir, profesyonel görünüm
- Gri tonları + mavi vurgu: Kurumsal, sade, dikkat dağıtmayan tasarım
- CSS değişkenleri ile kolay tema değişimi

### Karşılaşılan Zorluk ve Çözümü

**Zorluk:** Windows cmd shell'de `&` operatörü bash'teki `&&` gibi çalışmıyor, birden fazla komut çalıştırmak için farklı yaklaşım gerekiyordu.

**Çözüm:** Komutları ayrı ayrı çalıştırarak klasörleri oluşturdum. Alternatif olarak PowerShell'de `;` separator'ı kullanılabilir, ancak basit işlemler için ayrı komutlar daha güvenli.

### Sonraki Adım
Aşama 2'de veritabanı şeması tasarlanacak ve SQLAlchemy ORM modelleri (User, Ticket, TicketComment) oluşturulacak.

---

## ✅ Aşama 2: Veritabanı Şeması ve SQLAlchemy Modelleri (Tamamlandı)

### Yapılanlar
Bu aşamada veritabanı tablolarını temsil eden SQLAlchemy ORM modelleri oluşturuldu. Üç ana model tanımlandı: User, Ticket ve TicketComment.

**Oluşturulan Modeller:**

**1. User Modeli (`models/user.py`):**
- Kullanıcı bilgilerini saklar (id, ad soyad, e-posta, şifre, rol, departman)
- `UserRole` enum: `employee` ve `it_staff` rolleri
- İlişkiler: created_tickets, assigned_tickets, comments
- E-posta alanı UNIQUE constraint ile benzersiz

**2. Ticket Modeli (`models/ticket.py`):**
- IT destek taleplerini temsil eder
- `TicketCategory` enum: Donanım, Yazılım, Ağ/İnternet, Şifre Sıfırlama, Diğer
- `TicketPriority` enum: Düşük, Orta, Yüksek, Acil
- `TicketStatus` enum: Açık, İşleme Alındı, Beklemede, Çözüldü, Kapatıldı
- Timestamp alanları: created_at (otomatik), updated_at (otomatik güncellenme)
- İlişkiler: creator (talep sahibi), assigned_to_user (atanan IT personeli), comments
- Foreign keys: creator_id (NOT NULL), assigned_to_id (Nullable - henüz atanmamış olabilir)

**3. TicketComment Modeli (`models/ticket_comment.py`):**
- Taleplere yapılan yorumları saklar
- Her yorum bir talebe ve bir yazara bağlı
- Zaman damgası (created_at) ile sıralama yapılabilir
- İlişkiler: ticket, author

**Ek Dosyalar:**
- `init_db.py`: Veritabanını başlatma script'i
  - Tüm tabloları otomatik oluşturur
  - 4 test kullanıcısı ekler (1 IT personeli, 3 çalışan)
  - Şifreleri bcrypt ile hash'ler
- `DATABASE_SCHEMA.md`: Veritabanı şeması dokümantasyonu
  - Tablo yapıları detaylı açıklandı
  - İlişki diyagramı eklendi
  - Enum değerleri listelendi

### Teknolojik Kararlar

**SQLAlchemy ORM Kullanımı:**
- Raw SQL yerine ORM kullanarak kod daha okunabilir ve güvenli hale gelir
- SQL injection saldırılarına karşı otomatik koruma
- Relationship'ler sayesinde join işlemleri kolaylaşır
- Migration işlemleri (Alembic ile) daha kolay

**Enum Kullanımı:**
- Veritabanı seviyesinde veri tutarlılığı sağlar
- Yanlış değer girilmesini engeller (örn. status için "açıkk" gibi typo)
- Python kodunda IDE autocomplete desteği
- Frontend tarafında da aynı enum değerleri kullanılacak

**Timestamp Otomasyonu:**
- `server_default=func.now()`: Veritabanı seviyesinde varsayılan değer
- `onupdate=func.now()`: Her güncellemede otomatik güncelleme
- Manuel tarih yönetimine gerek kalmaz, hata riski azalır

**Cascade Relationships:**
- Kullanıcı silindiğinde talepler ve yorumlar da silinir (veri tutarlılığı)
- `orphan` modunda yetim kayıtlar kalmaz
- Veritabanı bütünlüğü korunur

**Nullable Foreign Key (assigned_to_id):**
- Yeni oluşturulan taleplerin henüz bir IT personeline atanmamış olabileceğini modelliyor
- İleride otomatik atama algoritmaları eklenebilir
- İş akışına uygun esnek yapı

### Karşılaşılan Zorluk ve Çözümü

**Zorluk:** SQLAlchemy'de iki farklı foreign key ile aynı tabloya referans vermek (User tablosuna hem creator_id hem assigned_to_id) "ambiguous foreign keys" hatasına neden olabilir.

**Çözüm:** `relationship()` tanımlarında `foreign_keys` parametresini açıkça belirterek hangi kolonun hangi ilişkiye ait olduğunu SQLAlchemy'e söyledik. Ayrıca `back_populates` kullanarak çift yönlü ilişki kurarak veri bütünlüğünü sağladık.

Örnek:
```python
creator = relationship(
    "User",
    back_populates="created_tickets",
    foreign_keys=[creator_id]  # Bu ilişki creator_id kolonunu kullanır
)
```

### Sonraki Adım
Aşama 3'te JWT tabanlı kimlik doğrulama sistemi geliştirilecek. Kullanıcı kayıt/giriş API'leri ve rol bazlı yetkilendirme middleware'i oluşturulacak.

---

## ✅ Aşama 3: JWT Tabanlı Kimlik Doğrulama ve Rol Bazlı Yetkilendirme (Tamamlandı)

### Yapılanlar
Bu aşamada JWT (JSON Web Token) tabanlı kimlik doğrulama sistemi ve rol bazlı erişim kontrolü geliştirildi. Kullanıcılar güvenli bir şekilde kayıt olup giriş yapabilir, API isteklerinde token kullanabilir.

**Auth Modülü (`auth/`):**

**1. Password Management (`auth/password.py`):**
- `hash_password()`: Bcrypt ile şifre hash'leme
- `verify_password()`: Hash'lenmiş şifreyi doğrulama
- Passlib kütüphanesi ile güvenli şifre yönetimi

**2. JWT Token Management (`auth/jwt.py`):**
- `create_access_token()`: JWT token oluşturma
- `decode_access_token()`: Token doğrulama ve payload çıkarma
- Token içinde: user_id (sub), role, email, expiration time
- Varsayılan süre: 24 saat (1440 dakika)
- .env dosyasından SECRET_KEY okuma

**3. Dependencies (`auth/dependencies.py`):**
- `get_current_user()`: Token'dan mevcut kullanıcıyı al (her korumalı endpoint'te kullanılır)
- `require_it_staff()`: Sadece IT personeline izin ver (403 Forbidden döndürür)
- `get_current_user_optional()`: Opsiyonel auth (public endpoint'ler için)
- FastAPI dependency injection sistemi ile entegrasyon

**Pydantic Şemaları (`schemas/user.py`):**
- `UserRegister`: Kayıt isteği (email, şifre, ad soyad, departman)
- `UserLogin`: Giriş isteği (email, şifre)
- `UserResponse`: Kullanıcı yanıtı (şifre hariç, güvenlik için)
- `TokenResponse`: JWT token + kullanıcı bilgileri

**API Endpoints (`routers/auth.py`):**
- `POST /auth/register`: Yeni kullanıcı kaydı (varsayılan rol: employee)
- `POST /auth/login`: E-posta ve şifre ile giriş
- `GET /auth/me`: Mevcut kullanıcı bilgilerini getir (token gerektirir)
- `POST /auth/refresh`: Token yenileme

**Test Suite (`tests/`):**
- `conftest.py`: Test fixture'ları (db, client, test_employee, test_it_staff)
- `test_auth.py`: 11 authentication test
  - Başarılı/başarısız kayıt
  - Başarılı/başarısız giriş
  - Token ile kullanıcı bilgisi alma
  - Geçersiz token kontrolü
  - Rol doğrulama
  - Token yenileme
- `test_authorization.py`: 6 authorization test
  - Rol atama kontrolü
  - IT personeli oluşturma güvenliği
  - Şifrenin API yanıtlarında gizlenmesi
  - Token payload doğrulama
  - Çoklu kullanıcı token izolasyonu

### Teknolojik Kararlar

**JWT Token Kullanımı:**
- **Stateless**: Sunucuda session saklanmaz, ölçeklenebilirlik artar
- **Self-contained**: Token içinde kullanıcı bilgileri var, her istekte DB sorgusu gerekmez
- **Expiration**: Token süresi dolduğunda yeniden login gerekir (güvenlik)
- **Bearer Authentication**: Industry standard (Authorization: Bearer <token>)

**Bcrypt Hash Algoritması:**
- **Yavaş**: Brute-force saldırılarına karşı dirençli (kasıtlı olarak yavaş)
- **Salt**: Her şifre farklı hash üretir, rainbow table saldırıları işe yaramaz
- **Adaptive**: Cost factor artırılabilir (gelecekte daha güvenli hale getirilebilir)

**Pydantic Validation:**
- API seviyesinde veri doğrulama (email format, şifre uzunluğu)
- Otomatik API dokümantasyonu (Swagger UI)
- Type safety (IDE autocomplete desteği)

**FastAPI Dependency Injection:**
- `Depends(get_current_user)`: Tekrar eden kod yerine dependency
- Endpoint'lerde otomatik kimlik doğrulama
- Test edilebilir kod (mock'lanabilir)

**Rol Bazlı Güvenlik:**
- Kayıt endpoint'i sadece `employee` rolü oluşturur
- IT personeli manuel olarak veritabanından eklenmeli (güvenlik)
- `require_it_staff` dependency ile korumalı endpoint'ler

### Karşılaşılan Zorluk ve Çözümü

**Zorluk:** FastAPI'de Bearer token authentication için doğru dependency yapısını kurmak. `HTTPBearer` security scheme'ini kullanırken token'ı nasıl extract edeceğimiz ve validation yaparken nasıl error handle edeceğimiz net değildi.

**Çözüm:** 
1. `HTTPBearer()` ile token'ı otomatik olarak `Authorization` header'ından çıkardık
2. `get_current_user` dependency'sinde token decode ve user lookup'ı yaptık
3. Hata durumlarında FastAPI'nin otomatik error handling'ini kullandık (HTTPException)
4. Chain dependency ile `require_it_staff → get_current_user` ilişkisi kurduk
5. Test'lerde `TestClient` ile header injection yaparak token authentication'ı simüle ettik

Bu sayede endpoint'lerde tek satırla kimlik doğrulama yapabiliyoruz:
```python
@app.get("/protected")
def protected_route(user: User = Depends(get_current_user)):
    return {"user": user.email}
```

### Test Sonuçları
17 test yazıldı ve hepsi başarılı. Test coverage:
- ✅ Kullanıcı kayıt ve giriş
- ✅ Token oluşturma ve doğrulama
- ✅ Rol bazlı erişim kontrolü
- ✅ Şifre güvenliği (hash, verify)
- ✅ Token payload doğruluğu
- ✅ Güvenlik açıkları (şifre leak, fake admin)

### Sonraki Adım
Aşama 4'te talep (ticket) oluşturma API'si geliştirilecek. Çalışanlar yeni destek talebi açabilecek.

---

## ✅ Aşama 4-17: Tam Stack Uygulama (Tamamlandı)

### Backend API (Aşama 4-7)

**Ticket Management API:**
- `POST /tickets/` - Yeni talep oluştur
- `GET /tickets/` - Talepleri listele (rol bazlı filtreleme)
- `GET /tickets/{id}` - Talep detayı (rol bazlı erişim)
- `PATCH /tickets/{id}` - Talep güncelle (IT personeli)
- `POST /tickets/{id}/assign-to-me` - Kendine ata
- `POST /tickets/{id}/close` - Talebi kapat

**Comment System API:**
- `POST /tickets/{id}/comments` - Yorum ekle
- `GET /tickets/{id}/comments` - Yorumları listele

**Özellikler:**
- ✅ Rol bazlı veri filtreleme (çalışan sadece kendi taleplerini görür)
- ✅ IT personeli tüm talepleri yönetebilir
- ✅ Durum, öncelik ve kategori filtreleme
- ✅ Otomatik timestamp yönetimi
- ✅ Talep atama sistemi

### Frontend (Aşama 8-15)

**Sayfalar:**
- **LoginPage** - Giriş/Kayıt formu, tab sistemi
- **EmployeeDashboard** - Çalışan paneli, kendi talepleri
- **ITDashboard** - IT personeli paneli, tüm talepler + istatistikler
- **TicketDetail** - Talep detayı, yorum sistemi

**Bileşenler:**
- **Navbar** - Kullanıcı bilgisi ve çıkış
- **CreateTicketModal** - Talep oluşturma modal
- **StatsSection** - İstatistik kartları ve grafikler (Recharts)

**Özellikler:**
- ✅ React Router ile sayfa yönlendirme
- ✅ Rol bazlı yönlendirme (employee → /dashboard, IT → /it-dashboard)
- ✅ LocalStorage ile token ve user yönetimi
- ✅ Axios interceptor ile otomatik token injection
- ✅ Toast bildirimleri (başarı/hata)
- ✅ Durum ve öncelik rozetleri (renkli)
- ✅ Responsive tasarım
- ✅ Filtreleme ve arama
- ✅ Gerçek zamanlı yorum sistemi
- ✅ IT personeli için grafik dashboard (kategori/öncelik dağılımı)
- ✅ Acil talepler görsel vurgulama (kırmızı kenarlık)

**Tasarım:**
- Inter font
- Nötr gri tonları + mavi vurgu rengi
- Profesyonel, sade, kurumsal görünüm
- CSS değişkenleri ile tema yönetimi
- Smooth animasyonlar

### Testler (Aşama 16)

**test_auth.py** - 11 test
- Kayıt/giriş başarı/başarısızlık
- Token doğrulama
- Şifre güvenliği

**test_authorization.py** - 6 test
- Rol atama kontrolü
- API güvenlik testleri

**test_tickets.py** - 12 test
- Talep oluşturma
- Rol bazlı listeleme (çalışan vs IT)
- Erişim kontrolü (çalışan başkasının talebini görememeli)
- IT personeli yetkileri
- Talep atama
- Kapatma yetkileri

**Toplam: 29 test** ✅

### Teknolojik Kararlar

**Rol Bazlı Filtreleme (Backend):**
- SQLAlchemy query seviyesinde filtreleme
- Çalışan: `query.filter(creator_id == current_user.id)`
- IT: Tüm kayıtlar (filtre yok)
- Frontend'den gelen parametrelere güvenilmez, backend kontrol eder

**State Management (Frontend):**
- LocalStorage: Token ve user bilgisi (persistent)
- useState: Component state (ticket listesi, form data)
- useEffect: API çağrıları ve veri yükleme
- Basit prop drilling (karmaşık state yönetimi gerekmedi)

**API Servis Katmanı:**
- Merkezi axios instance
- Interceptor ile otomatik token ekleme
- 401 error'da otomatik logout
- Temiz API fonksiyon yapısı (authAPI, ticketsAPI, commentsAPI)

**Toast Bildirimleri:**
- Üçüncü parti kütüphane kullanmadık
- Basit custom implementasyon (showToast helper)
- CSS animation ile slide-in/out
- Otomatik 3 saniye sonra kaybolma

**Recharts Kullanımı:**
- Hafif ve kolay pie chart library
- Kategori ve öncelik dağılımı gösterimi
- Responsive container ile her ekranda uyumlu

### Karşılaşılan Zorlukler ve Çözümler

**1. Rol Bazlı Erişim Güvenliği:**
**Zorluk:** Frontend'de rol kontrolü yapmak yeterli değil, backend'de de kontrol edilmeli.
**Çözüm:** Her endpoint'te rol kontrolü yaptık. Çalışan başka birinin talebini görmeye çalışırsa 403 Forbidden döndürüyoruz. Test'lerle doğruladık.

**2. React Router ile Rol Bazlı Yönlendirme:**
**Zorluk:** Login sonrası kullanıcının rolüne göre farklı sayfaya yönlendirme.
**Çözüm:** `isAuthenticated()` ve `isITStaff()` helper fonksiyonları yazdık. App.jsx'te conditional routing kullandık. Employee rolü /it-dashboard'a erişmeye çalışırsa /dashboard'a yönlendiriliyor.

**3. Token Expire Handling:**
**Zorluk:** Token süresi dolduğunda kullanıcı deneyimini bozmadan logout yapmak.
**Çözüm:** Axios response interceptor'da 401 hatasını yakalıyoruz, token ve user'ı temizleyip login sayfasına yönlendiriyoruz. Kullanıcı otomatik logout oluyor.

**4. Modal Overlay Click:**
**Zorluk:** Modal'ın content kısmına tıklayınca kapanmaması gerekiyor.
**Çözüm:** Overlay'e onClick={onClose}, content'e onClick={(e) => e.stopPropagation()} ekledik. Event bubbling durduruldu.

### Proje Yapısı

```
it-helpdesk-system/
├── backend/
│   ├── models/          # User, Ticket, TicketComment
│   ├── schemas/         # Pydantic validation
│   ├── routers/         # auth, tickets, comments
│   ├── auth/            # JWT, password, dependencies
│   ├── tests/           # pytest (29 test)
│   ├── main.py          # FastAPI app
│   ├── database.py      # SQLAlchemy config
│   └── init_db.py       # DB initialization
├── frontend/
│   ├── src/
│   │   ├── pages/       # Login, Dashboards, TicketDetail
│   │   ├── components/  # Navbar, Modal, Stats
│   │   ├── services/    # API (axios)
│   │   ├── utils/       # helpers, auth, constants
│   │   ├── styles/      # CSS modules
│   │   ├── App.jsx      # Router setup
│   │   └── main.jsx     # Entry point
│   └── package.json
├── FEATURES.md          # Bu dosya
└── README.md            # Kurulum rehberi
```

### Sonuç

✅ **17 aşama tamamlandı**
✅ **Full-stack uygulama çalışır durumda**
✅ **Rol bazlı yetkilendirme %100 çalışıyor**
✅ **29 test geçiyor**
✅ **Profesyonel, kurumsal tasarım**
✅ **Responsive ve kullanıcı dostu**

Proje üniversite stajı seviyesinde, hem eğitici hem de gerçek dünya senaryolarına uygun bir şekilde tamamlandı. 🎉

---

## ✅ Aşama 18: Görsel Kimlik Tasarımı - İş Emri Fişi Konsepti (Tamamlandı)

### Yapılanlar
Tüm frontend tasarımı baştan sona "İş Emri Fişi / Atölye Dokütü" temasıyla yeniden tasarlandı. Hiçbir fonksiyonelliğe dokunulmadan, sadece görsel tasarım (CSS, renkler, tipografi, spacing) tamamen değiştirildi.

**Tasarım Konsepti:**
Karbon kopyalı iş emri formları, perforeli fiş kağıtları ve kauçuk damga izlerinden ilham alan, teknik servis/atölye estetiği. IT destek talebinin kendi doğasına uygun kurumsal-ama-karakterli bir görünüm.

**Renk Paleti:**
- Zemin: #E7ECEF (soluk karbon kağıdı mavi-grisi)
- Kağıt panelleri: #F4F6F7 (beyaz)
- Mürekkep: #1B2A4A (koyu lacivert, dolma kalem mürekkebi)
- Damga kırmızısı: #C1440E (acil/açık)
- Damga yeşili: #2F6B4F (çözüldü)
- Amber: #D9A02C (öncelik/uyarı)
- Çizgi rengi: #B7C0C7 (defter çizgisi gri)

**Tipografi:**
- Monospace: IBM Plex Mono (talep numaraları, tarihler, teknik veri)
- Sans-serif: Archivo (başlıklar, butonlar, genel arayüz)
- Talep numaraları büyük punto ve monospace ile "fiş numarası" görünümü

**Karakteristik Öğeler:**
1. **Kauçuk Damga Efekti**: Çözüldü/Kapatıldı durumdaki taleplerde -8 derece eğik, double border, texture efektli damga rozetleri
2. **Perforeli Kenar**: Talep kartlarının sağ kenarında delikli fiş kenarı efekti (radial-gradient ile)
3. **Form Filigranı**: Modal ve detay sayfalarında "FORM" / "WORK ORDER" etiketi
4. **Minimal Border Radius**: 4-8px arası (resmi form estetiği)
5. **Dashed Border**: Yorumlar ve bilgi kutularında kesik çizgi kenarlık
6. **Monospace Veri**: Tüm numaralar, tarihler ve teknik bilgiler IBM Plex Mono ile

**Güncellenen Dosyalar:**
- `index.html` - Font import (IBM Plex Mono, Archivo)
- `index.css` - Ana CSS değişkenleri ve global stiller
- `LoginPage.css` - Grid pattern arka plan, form tasarımı
- `Navbar.css` - Kalın alt kenarlık, form başlığı stili
- `Dashboard.css` - Perforeli kartlar, damga rozetleri, minimal gölgeler
- `Modal.css` - Form popup, FORM etiketi
- `TicketDetail.css` - Kauçuk damga animasyonu, WORK ORDER filigranı
- `helpers.js` - Toast bildirimi stili güncellendi
- `constants.js` - Renk paleti güncellendi (damga renkleri)

**Erişilebilirlik:**
- Focus durumları görünür (2px outline)
- Klavye navigasyonu korundu
- Renk kontrastları WCAG standartlarına uygun
- Responsive tasarım mobilde de bozulmadan çalışıyor

**Not:** Bu tamamen görsel bir güncelleme - API çağrıları, state yönetimi, routing, component yapısı hiç değişmedi. Uygulama fonksiyonel olarak birebir aynı çalışıyor, sadece görsel dili değişti.

---