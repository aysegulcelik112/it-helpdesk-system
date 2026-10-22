"""
Ticket Pydantic Şemaları

Talep (ticket) ile ilgili API request ve response şemaları.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models import TicketCategory, TicketPriority, TicketStatus
from schemas.user import UserResponse

class TicketCreate(BaseModel):
    """Talep oluşturma isteği"""
    title: str = Field(..., min_length=5, max_length=200, description="Talep başlığı")
    description: str = Field(..., min_length=10, description="Detaylı açıklama")
    category: TicketCategory = Field(..., description="Talep kategorisi")
    priority: TicketPriority = Field(default=TicketPriority.MEDIUM, description="Öncelik seviyesi")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Bilgisayarım açılmıyor",
                "description": "Bu sabahtan beri bilgisayarımı açmaya çalışıyorum ama ekranda hiçbir şey görünmüyor. Güç LED'i yanıyor ama ekran siyah.",
                "category": "Donanım",
                "priority": "Yüksek"
            }
        }

class TicketUpdate(BaseModel):
    """Talep güncelleme isteği (IT personeli için)"""
    status: Optional[TicketStatus] = None
    assigned_to_id: Optional[int] = None
    priority: Optional[TicketPriority] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "İşleme Alındı",
                "assigned_to_id": 1,
                "priority": "Acil"
            }
        }

class TicketResponse(BaseModel):
    """Talep yanıtı"""
    id: int
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    creator_id: int
    assigned_to_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    creator: UserResponse
    assigned_to_user: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    """Talep liste yanıtı (temel bilgiler)"""
    id: int
    title: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    creator_id: int
    assigned_to_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
