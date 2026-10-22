"""
Veritabanı Bağlantı Yapılandırması

Bu modül SQLAlchemy ile SQLite veritabanı bağlantısını yönetir.
Session yönetimi ve veritabanı engine'i burada tanımlanır.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite veritabanı dosya yolu
# Proje kök dizininde 'helpdesk.db' adında bir dosya oluşturulur
SQLALCHEMY_DATABASE_URL = "sqlite:///./helpdesk.db"

# SQLAlchemy engine oluştur
# check_same_thread=False: SQLite'ın thread güvenliği için gerekli
# FastAPI birden fazla thread kullanabilir, bu parametre bunu sağlar
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session oluşturucu - veritabanı işlemleri için session açmak için kullanılır
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base sınıf - tüm ORM modelleri bu sınıftan türetilecek
Base = declarative_base()

# Dependency: Her request için yeni bir DB session oluştur
def get_db():
    """
    FastAPI dependency fonksiyonu.
    Her API isteği için yeni bir veritabanı session'ı oluşturur
    ve işlem bitince kapatır (kaynak sızıntısını önler).
    
    Kullanım:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
