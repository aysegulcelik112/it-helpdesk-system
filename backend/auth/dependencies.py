"""
Kimlik Doğrulama Dependencies (Bağımlılıklar)

Bu modül FastAPI dependency injection için fonksiyonlar içerir.
Endpoint'lerde kullanıcı kimlik doğrulama ve yetkilendirme kontrolü yapar.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials as HTTPAuthCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserRole
from auth.jwt import decode_access_token

# HTTP Bearer token şeması (Authorization: Bearer <token>)
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Token'dan mevcut kullanıcıyı al
    
    Bu dependency her korumalı endpoint'te kullanılır.
    Token'ı doğrular ve kullanıcı nesnesini döndürür.
    
    Args:
        credentials: HTTP Authorization header'ından alınan token
        db: Veritabanı session
    
    Returns:
        User: Mevcut kullanıcı nesnesi
    
    Raises:
        HTTPException 401: Token geçersiz veya kullanıcı bulunamadı
    
    Kullanım:
        @app.get("/profile")
        def get_profile(current_user: User = Depends(get_current_user)):
            return {"user": current_user.email}
    """
    # Token'ı decode et
    token = credentials.credentials
    payload = decode_access_token(token)
    
    # Token'dan user_id'yi al
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token içinde kullanıcı bilgisi bulunamadı"
        )
    
    # Kullanıcıyı veritabanından al
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı bulunamadı"
        )
    
    return user

def require_it_staff(current_user: User = Depends(get_current_user)) -> User:
    """
    Sadece IT personeline izin ver
    
    Bu dependency IT personeline özel endpoint'lerde kullanılır.
    Çalışan rolündeki kullanıcılar erişemez.
    
    Args:
        current_user: Mevcut kullanıcı (get_current_user'dan)
    
    Returns:
        User: IT personeli kullanıcı nesnesi
    
    Raises:
        HTTPException 403: Kullanıcı IT personeli değilse
    
    Kullanım:
        @app.post("/tickets/{ticket_id}/assign")
        def assign_ticket(
            ticket_id: int,
            it_user: User = Depends(require_it_staff)
        ):
            # Sadece IT personeli bu endpoint'e erişebilir
            ...
    """
    if current_user.role != UserRole.IT_STAFF:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu işlem için IT personeli yetkisi gereklidir"
        )
    return current_user

def get_current_user_optional(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Opsiyonel kimlik doğrulama
    
    Token varsa kullanıcıyı döndürür, yoksa None.
    Public endpoint'lerde kullanılabilir (login olmuş/olmamış kullanıcılar).
    
    Args:
        credentials: HTTP Authorization header'ından alınan token
        db: Veritabanı session
    
    Returns:
        User | None: Kullanıcı veya None
    """
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None
