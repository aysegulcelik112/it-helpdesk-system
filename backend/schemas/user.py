"""
User Pydantic Şemaları

API request ve response için veri doğrulama şemaları.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from models import UserRole

class UserRegister(BaseModel):
    """Kullanıcı kayıt isteği"""
    full_name: str = Field(..., min_length=2, max_length=100, description="Ad ve soyad")
    email: EmailStr = Field(..., description="E-posta adresi")
    password: str = Field(..., min_length=6, max_length=50, description="Şifre (min 6 karakter)")
    department: Optional[str] = Field(None, max_length=50, description="Departman")
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Ahmet Yılmaz",
                "email": "ahmet.yilmaz@company.com",
                "password": "secure123",
                "department": "Muhasebe"
            }
        }

class UserLogin(BaseModel):
    """Kullanıcı giriş isteği"""
    username: EmailStr = Field(..., description="E-posta adresi")
    password: str = Field(..., description="Şifre")
    
    # email field'ı için alias
    @property
    def email(self):
        return self.username
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@company.com",
                "password": "user123"
            }
        }

class UserResponse(BaseModel):
    """Kullanıcı bilgileri yanıtı (şifre hariç)"""
    id: int
    full_name: str
    email: str
    role: UserRole
    department: Optional[str] = None
    
    class Config:
        from_attributes = True  # SQLAlchemy model'den Pydantic'e dönüşüm için

class TokenResponse(BaseModel):
    """JWT token yanıtı"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "full_name": "Ahmet Yılmaz",
                    "email": "ahmet.yilmaz@company.com",
                    "role": "employee",
                    "department": "Muhasebe"
                }
            }
        }
