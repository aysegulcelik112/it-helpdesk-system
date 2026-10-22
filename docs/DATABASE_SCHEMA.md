# Veritabanı Şeması Dokümantasyonu

Bu doküman IT Helpdesk System'in veritabanı yapısını açıklar.

## Tablolar

### 1. `users` - Kullanıcılar Tablosu

Sistemdeki tüm kullanıcıları saklar (hem çalışanlar hem IT personeli).

| Sütun | Tip | Açıklama | Kısıtlamalar |
|-------|-----|----------|--------------|
| `id` | Integer | Benzersiz kullanıcı kimliği | Primary Key, Auto Increment |
| `full_name` | String(100) | Kullanıcının ad ve soyadı | NOT NULL |
| `email` | String(100) | E-posta adresi (giriş için) | UNIQUE, NOT NULL, Indexed |
| `hashed_password` | String(255) | Bcrypt ile hash'lenmiş şifre | NOT NULL |
| `role` | Enum | Kullanıcı rolü | NOT NULL, Values: 'employee', 'it_staff' |
| `department` | String(50) | Kullanıcının departmanı | Nullable |

**İlişkiler:**
- `created_tickets`: Kullanıcının oluşturduğu talepler (One-to-Many)
- `assigned_tickets`: IT personeline atanan talepler (One-to-Many)
- `comments`: Kullanıcının yazdığı yorumlar (One-to-Many)

---

### 2. `tickets` - Talepler Tablosu

IT destek taleplerini saklar.

| Sütun | Tip | Açıklama | Kısıtlamalar |
|-------|-----|----------|--------------|
| `id` | Integer | Benzersiz talep kimliği | Primary Key, Auto Increment |
| `title` | String(200) | Talep başlığı | NOT NULL |
| `description` | Text | Detaylı açıklama | NOT NULL |
| `category` | Enum | Talep kategorisi | NOT NULL, Values: 'Donanım', 'Yazılım', 'Ağ/İnternet', 'Şifre Sıfırlama', 'Diğer' |
| `priority` | Enum | Öncelik seviyesi | NOT NULL, Default: 'Orta', Values: 'Düşük', 'Orta', 'Yüksek', 'Acil' |
| `status` | Enum | Talep durumu | NOT NULL, Default: 'Açık', Values: 'Açık', 'İşleme Alındı', 'Beklemede', 'Çözüldü', 'Kapatıldı' |
| `creator_id` | Integer | Talebi oluşturan kullanıcı | Foreign Key → users.id, NOT NULL |
| `assigned_to_id` | Integer | Atanan IT personeli | Foreign Key → users.id, Nullable |
| `created_at` | DateTime | Oluşturulma tarihi | NOT NULL, Auto-set |
| `updated_at` | DateTime | Son güncellenme tarihi | NOT NULL, Auto-update |

**İlişkiler:**
- `creator`: Talebi oluşturan kullanıcı (Many-to-One)
- `assigned_to_user`: Atanan IT personeli (Many-to-One)
- `comments`: Talebe ait yorumlar (One-to-Many)

---

### 3. `ticket_comments` - Talep Yorumları Tablosu

Taleplere yapılan yorumları ve mesajlaşma geçmişini saklar.

| Sütun | Tip | Açıklama | Kısıtlamalar |
|-------|-----|----------|--------------|
| `id` | Integer | Benzersiz yorum kimliği | Primary Key, Auto Increment |
| `ticket_id` | Integer | İlişkili talep | Foreign Key → tickets.id, NOT NULL |
| `author_id` | Integer | Yorumu yazan kullanıcı | Foreign Key → users.id, NOT NULL |
| `message` | Text | Yorum metni | NOT NULL |
| `created_at` | DateTime | Oluşturulma tarihi | NOT NULL, Auto-set |

**İlişkiler:**
- `ticket`: İlgili talep (Many-to-One)
- `author`: Yorumu yazan kullanıcı (Many-to-One)

---

## İlişki Diyagramı

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │◄────┐
│ full_name       │     │
│ email (UNIQUE)  │     │
│ hashed_password │     │
│ role            │     │
│ department      │     │
└─────────────────┘     │
        ▲               │
        │               │
        │               │
┌───────┴──────┐        │
│              │        │
│   created    │        │ assigned
│   tickets    │        │ tickets
│              │        │
│              │        │
┌──────────────▼────────┴──┐
│       tickets            │
├──────────────────────────┤
│ id (PK)                  │◄────┐
│ title                    │     │
│ description              │     │
│ category                 │     │
│ priority                 │     │
│ status                   │     │
│ creator_id (FK)          │     │
│ assigned_to_id (FK)      │     │
│ created_at               │     │
│ updated_at               │     │
└──────────────────────────┘     │
                                 │
                                 │
                          ┌──────┴──────────────┐
                          │  ticket_comments    │
                          ├─────────────────────┤
                          │ id (PK)             │
                          │ ticket_id (FK)      │
                          │ author_id (FK)      │
                          │ message             │
                          │ created_at          │
                          └─────────────────────┘
```

## Cascade Davranışları

**User silindiğinde:**
- `created_tickets`: Talepler de silinir (CASCADE)
- `comments`: Yorumlar da silinir (CASCADE)

**Ticket silindiğinde:**
- `comments`: İlgili yorumlar da silinir (CASCADE)

## İndeksler

Sorgu performansını artırmak için şu sütunlar indexlenmiştir:
- `users.id` (Primary Key, otomatik)
- `users.email` (UNIQUE constraint, otomatik)
- `tickets.id` (Primary Key, otomatik)
- `ticket_comments.id` (Primary Key, otomatik)

## Enum Değerleri

### UserRole
- `employee`: Normal çalışan
- `it_staff`: IT personeli (admin)

### TicketCategory
- `Donanım`: Bilgisayar, yazıcı, mouse vb.
- `Yazılım`: Uygulama kurulumu, lisans sorunları
- `Ağ/İnternet`: Bağlantı sorunları, VPN
- `Şifre Sıfırlama`: Hesap erişimi sorunları
- `Diğer`: Kategoriye uymayan talepler

### TicketPriority
- `Düşük`: Acil olmayan, ertele bilen
- `Orta`: Normal iş akışını etkileyen
- `Yüksek`: İş akışını ciddi şekilde engelleyen
- `Acil`: Kritik, hemen müdahale gerekiyor

### TicketStatus
- `Açık`: Yeni oluşturulmuş, henüz işleme alınmamış
- `İşleme Alındı`: IT personeli üzerinde çalışıyor
- `Beklemede`: Ek bilgi veya harici kaynak bekleniyor
- `Çözüldü`: Sorun çözüldü, onay bekleniyor
- `Kapatıldı`: Talep kapatıldı, arşivlendi

## Test Verileri

`init_db.py` script'i çalıştırıldığında şu test kullanıcıları oluşturulur:

1. **IT Personeli:**
   - E-posta: admin@company.com
   - Şifre: admin123
   - Rol: it_staff
   - Departman: IT

2. **Çalışanlar:**
   - E-posta: user@company.com
   - Şifre: user123
   - Rol: employee
   - Departman: Muhasebe
   
   (ve diğer test kullanıcıları)
