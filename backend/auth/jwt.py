"""
JWT Token Yönetimi

Bu modül JWT (JSON Web Token) oluşturma ve doğrulama işlemlerini yapar.
Token içinde kullanıcı ID'si ve rolü saklanır.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

# .env dosyasından environment variables'ları yükle
load_dotenv()

# JWT ayarları
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 saat

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT access token oluştur
    
    Args:
        data: Token içine konulacak veri (user_id, role, email)
        expires_delta: Token geçerlilik süresi (opsiyonel)
    
    Returns:
        JWT token string
    
    Örnek:
        token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )
    """
    to_encode = data.copy()
    
    # Token'ın son kullanma tarihini belirle
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Expiration time'ı token'a ekle
    to_encode.update({"exp": expire})
    
    # JWT token'ı encode et
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    JWT token'ı decode et ve içindeki veriyi al
    
    Args:
        token: JWT token string
    
    Returns:
        Token içindeki veri (user_id, role)
    
    Raises:
        HTTPException: Token geçersiz veya süresi dolmuşsa
    
    Örnek:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token doğrulanamadı",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Token'ı decode et
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        # Token geçersiz veya süresi dolmuş
        raise credentials_exception
