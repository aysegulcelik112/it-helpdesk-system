"""
Veritabanı Başlatma Script'i

Bu script:
1. Tüm tabloları oluşturur (users, tickets, ticket_comments)
2. Test kullanıcıları ekler (bir IT personeli ve bir çalışan)

Kullanım: python init_db.py
"""

from database import engine, SessionLocal, Base
from models import User, UserRole
from passlib.context import CryptContext

# Şifre hash'leme için bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Şifreyi bcrypt ile hash'le"""
    return pwd_context.hash(password)

def init_database():
    """Veritabanını başlat ve test verilerini ekle"""
    
    print("🗄️  Veritabanı tabloları oluşturuluyor...")
    
    # Tüm modellerin tablolarını oluştur
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tablolar başarıyla oluşturuldu!")
    print("\n📝 Test kullanıcıları ekleniyor...")
    
    # Database session oluştur
    db = SessionLocal()
    
    try:
        # Daha önce kullanıcı eklenmiş mi kontrol et
        existing_users = db.query(User).count()
        
        if existing_users > 0:
            print("⚠️  Veritabanında zaten kullanıcılar var. Test kullanıcıları eklenmedi.")
            return
        
        # Test kullanıcıları oluştur
        test_users = [
            User(
                full_name="Admin Kullanıcı",
                email="admin@company.com",
                hashed_password=hash_password("admin123"),
                role=UserRole.IT_STAFF,
                department="IT"
            ),
            User(
                full_name="Ahmet Yılmaz",
                email="user@company.com",
                hashed_password=hash_password("user123"),
                role=UserRole.EMPLOYEE,
                department="Muhasebe"
            ),
            User(
                full_name="Ayşe Demir",
                email="ayse.demir@company.com",
                hashed_password=hash_password("user123"),
                role=UserRole.EMPLOYEE,
                department="İnsan Kaynakları"
            ),
            User(
                full_name="Mehmet Kaya",
                email="mehmet.kaya@company.com",
                hashed_password=hash_password("user123"),
                role=UserRole.EMPLOYEE,
                department="Satış"
            ),
        ]
        
        # Kullanıcıları veritabanına ekle
        db.add_all(test_users)
        db.commit()
        
        print("✅ Test kullanıcıları başarıyla eklendi!")
        print("\n👤 Giriş Bilgileri:")
        print("\n📌 IT Personeli:")
        print("   E-posta: admin@company.com")
        print("   Şifre: admin123")
        print("\n📌 Çalışan:")
        print("   E-posta: user@company.com")
        print("   Şifre: user123")
        print("\n🎉 Veritabanı hazır! Backend'i başlatabilirsiniz.")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
