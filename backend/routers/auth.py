"""
Authentication Router

Kullanıcı kayıt ve giriş endpoint'leri.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserRole
from schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Yeni kullanıcı kaydı
    
    Yeni bir çalışan hesabı oluşturur (varsayılan rol: employee).
    E-posta adresi benzersiz olmalıdır.
    
    Args:
        user_data: Kullanıcı kayıt bilgileri
        db: Veritabanı session
    
    Returns:
        JWT token ve kullanıcı bilgileri
    
    Raises:
        HTTPException 400: E-posta zaten kayıtlı
    """
    # E-posta zaten kayıtlı mı kontrol et
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu e-posta adresi zaten kayıtlı"
        )
    
    # Yeni kullanıcı oluştur
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=UserRole.EMPLOYEE,  # Varsayılan olarak çalışan rolü
        department=user_data.department
    )
    
    # Veritabanına kaydet
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # JWT token oluştur
    access_token = create_access_token(
        data={
            "sub": str(new_user.id),
            "role": new_user.role.value,
            "email": new_user.email
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(new_user)
    )

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Kullanıcı girişi
    
    E-posta ve şifre ile giriş yapar.
    Başarılı girişte JWT token döndürür.
    
    Args:
        credentials: E-posta ve şifre
        db: Veritabanı session
    
    Returns:
        JWT token ve kullanıcı bilgileri
    
    Raises:
        HTTPException 401: E-posta veya şifre yanlış
    """
    # Kullanıcıyı e-posta ile bul
    user = db.query(User).filter(User.email == credentials.username).first()
    
    # Kullanıcı bulunamadı veya şifre yanlış
    if not user or not verify_password(credentials.password, user.hashed_password):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-posta veya şifre yanlış",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWT token oluştur
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value,
            "email": user.email
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Mevcut kullanıcının bilgilerini al
    
    Token'dan kullanıcı bilgilerini döndürür.
    Frontend'de kullanıcı durumunu kontrol etmek için kullanılır.
    
    Args:
        current_user: Token'dan alınan mevcut kullanıcı
    
    Returns:
        Kullanıcı bilgileri (şifre hariç)
    """
    return UserResponse.model_validate(current_user)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Token yenileme
    
    Mevcut geçerli token ile yeni bir token oluşturur.
    Token süresi dolmak üzereyken kullanılabilir.
    
    Args:
        current_user: Mevcut kullanıcı
    
    Returns:
        Yeni JWT token ve kullanıcı bilgileri
    """
    # Yeni token oluştur
    access_token = create_access_token(
        data={
            "sub": str(current_user.id),
            "role": current_user.role.value,
            "email": current_user.email
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(current_user)
    )
