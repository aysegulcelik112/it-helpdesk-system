"""
Şifre Hash ve Doğrulama Modülü

Bu modül kullanıcı şifrelerini güvenli bir şekilde hash'ler ve doğrular.
Bcrypt algoritması kullanılır.
"""

from passlib.context import CryptContext

# Bcrypt context oluştur
# schemes=["bcrypt"]: Bcrypt algoritması kullan
# deprecated="auto": Eski hash'leri otomatik güncelle
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Düz metni bcrypt ile hash'le
    
    Args:
        password: Kullanıcının düz metin şifresi
    
    Returns:
        Hash'lenmiş şifre (veritabanında saklanır)
    
    Örnek:
        hashed = hash_password("user123")
        # Sonuç: "$2b$12$KIX..." gibi bir hash
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Düz metin şifre ile hash'lenmiş şifreyi karşılaştır
    
    Args:
        plain_password: Kullanıcının girdiği şifre
        hashed_password: Veritabanındaki hash'lenmiş şifre
    
    Returns:
        True: Şifre doğru
        False: Şifre yanlış
    
    Örnek:
        is_valid = verify_password("user123", user.hashed_password)
    """
    return pwd_context.verify(plain_password, hashed_password)
