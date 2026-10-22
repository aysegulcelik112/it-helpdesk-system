"""
Comment Pydantic Şemaları

Talep yorumları için API şemaları.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from schemas.user import UserResponse

class CommentCreate(BaseModel):
    """Yorum oluşturma isteği"""
    message: str = Field(..., min_length=1, description="Yorum metni")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Bilgisayarın güç kablosunu kontrol ettim, çalışıyor. Monitör kablosu gevşek olabilir mi?"
            }
        }

class CommentResponse(BaseModel):
    """Yorum yanıtı"""
    id: int
    ticket_id: int
    author_id: int
    message: str
    created_at: datetime
    author: UserResponse
    
    class Config:
        from_attributes = True
