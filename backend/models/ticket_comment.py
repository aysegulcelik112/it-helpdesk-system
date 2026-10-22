"""
TicketComment (Talep Yorumu) Modeli

Bu model bir talebe yapılan yorumları/mesajları temsil eder.
Hem çalışan hem IT personeli yorum ekleyebilir.
Talep geçmişini ve iletişim akışını takip etmek için kullanılır.
"""

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class TicketComment(Base):
    """
    Talep Yorumu tablosu
    
    Attributes:
        id: Benzersiz yorum kimliği
        ticket_id: İlişkili talep ID'si
        author_id: Yorumu yazan kullanıcı ID'si
        message: Yorum metni
        created_at: Yorum oluşturulma tarihi
    """
    __tablename__ = "ticket_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    
    # Timestamp - otomatik ayarlanır
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # İlişkiler (Relationships)
    ticket = relationship(
        "Ticket",
        back_populates="comments"
    )
    
    author = relationship(
        "User",
        back_populates="comments"
    )
    
    def __repr__(self):
        return f"<TicketComment(id={self.id}, ticket_id={self.ticket_id}, author_id={self.author_id})>"
