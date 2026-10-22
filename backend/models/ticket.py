"""
Ticket (Talep) Modeli

Bu model IT destek taleplerini temsil eder.
Her talep bir çalışan tarafından oluşturulur ve isteğe bağlı olarak
bir IT personeline atanabilir.
"""

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class TicketCategory(str, enum.Enum):
    """Talep kategorileri"""
    HARDWARE = "Donanım"
    SOFTWARE = "Yazılım"
    NETWORK = "Ağ/İnternet"
    PASSWORD = "Şifre Sıfırlama"
    OTHER = "Diğer"

class TicketPriority(str, enum.Enum):
    """Talep öncelik seviyeleri"""
    LOW = "Düşük"
    MEDIUM = "Orta"
    HIGH = "Yüksek"
    URGENT = "Acil"

class TicketStatus(str, enum.Enum):
    """Talep durumları"""
    OPEN = "Açık"              # Yeni oluşturulmuş, henüz işleme alınmamış
    IN_PROGRESS = "İşleme Alındı"  # IT personeli üzerinde çalışıyor
    PENDING = "Beklemede"      # Ek bilgi veya harici kaynak bekleniyor
    RESOLVED = "Çözüldü"       # Sorun çözüldü, onay bekleniyor
    CLOSED = "Kapatıldı"       # Talep kapatıldı

class Ticket(Base):
    """
    Talep (Ticket) tablosu
    
    Attributes:
        id: Benzersiz talep kimliği
        title: Talep başlığı (kısa özet)
        description: Detaylı açıklama
        category: Talep kategorisi (Donanım, Yazılım, vb.)
        priority: Öncelik seviyesi
        status: Mevcut durum
        creator_id: Talebi oluşturan kullanıcı ID'si
        assigned_to_id: Atanan IT personeli ID'si (opsiyonel)
        created_at: Oluşturulma tarihi
        updated_at: Son güncellenme tarihi
    """
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(TicketCategory), nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    
    # Foreign Keys
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps - otomatik olarak ayarlanır
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # İlişkiler (Relationships)
    creator = relationship(
        "User",
        back_populates="created_tickets",
        foreign_keys=[creator_id]
    )
    
    assigned_to_user = relationship(
        "User",
        back_populates="assigned_tickets",
        foreign_keys=[assigned_to_id]
    )
    
    # Talebe ait yorumlar
    comments = relationship(
        "TicketComment",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="TicketComment.created_at"  # Yorumları tarih sırasına göre getir
    )
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, title={self.title}, status={self.status})>"
