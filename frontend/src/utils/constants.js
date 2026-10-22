/**
 * Sabitler ve Enum Değerleri
 * 
 * Uygulama genelinde kullanılan sabit değerler.
 */

// Kullanıcı Rolleri
export const USER_ROLES = {
  EMPLOYEE: 'employee',
  IT_STAFF: 'it_staff',
};

// Talep Kategorileri
export const TICKET_CATEGORIES = {
  HARDWARE: 'Donanım',
  SOFTWARE: 'Yazılım',
  NETWORK: 'Ağ/İnternet',
  PASSWORD: 'Şifre Sıfırlama',
  OTHER: 'Diğer',
};

// Talep Öncelikleri
export const TICKET_PRIORITIES = {
  LOW: 'Düşük',
  MEDIUM: 'Orta',
  HIGH: 'Yüksek',
  URGENT: 'Acil',
};

// Talep Durumları
export const TICKET_STATUSES = {
  OPEN: 'Açık',
  IN_PROGRESS: 'İşleme Alındı',
  PENDING: 'Beklemede',
  RESOLVED: 'Çözüldü',
  CLOSED: 'Kapatıldı',
};

// Durum Renkleri (Kauçuk Damga Renkleri)
export const STATUS_COLORS = {
  'Açık': '#C1440E',           // Damga kırmızısı
  'İşleme Alındı': '#D9A02C',  // Amber
  'Beklemede': '#3B5998',      // Lacivert
  'Çözüldü': '#2F6B4F',        // Damga yeşili
  'Kapatıldı': '#6b7280',      // Gri
};

// Öncelik Renkleri
export const PRIORITY_COLORS = {
  'Düşük': '#2F6B4F',    // Yeşil
  'Orta': '#3B5998',     // Lacivert
  'Yüksek': '#D9A02C',   // Amber
  'Acil': '#C1440E',     // Kauçuk damga kırmızısı
};

// Departmanlar
export const DEPARTMENTS = [
  'Muhasebe',
  'İnsan Kaynakları',
  'Satış',
  'Pazarlama',
  'Üretim',
  'Lojistik',
  'IT',
  'Yönetim',
];
