"""
User (Kullanıcı) Modeli

Bu model sistemdeki tüm kullanıcıları temsil eder.
İki rol vardır: 'employee' (çalışan) ve 'it_staff' (IT personeli).
"""

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    """Kullanıcı rolleri enum"""
    EMPLOYEE = "employee"      # Normal çalışan
    IT_STAFF = "it_staff"      # IT personeli (admin)

class User(Base):
    """
    Kullanıcı tablosu
    
    Attributes:
        id: Benzersiz kullanıcı kimliği (primary key)
        full_name: Kullanıcının ad ve soyadı
        email: E-posta adresi (giriş için kullanılır, benzersiz)
        hashed_password: Bcrypt ile hash'lenmiş şifre
        role: Kullanıcı rolü (employee veya it_staff)
        department: Kullanıcının departmanı (opsiyonel)
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    department = Column(String(50), nullable=True)
    
    # İlişkiler (Relationships)
    # Bir kullanıcının oluşturduğu talepler
    created_tickets = relationship(
        "Ticket",
        back_populates="creator",
        foreign_keys="Ticket.creator_id",
        cascade="all, delete-orphan"
    )
    
    # IT personeline atanan talepler
    assigned_tickets = relationship(
        "Ticket",
        back_populates="assigned_to_user",
        foreign_keys="Ticket.assigned_to_id"
    )
    
    # Kullanıcının yazdığı yorumlar
    comments = relationship(
        "TicketComment",
        back_populates="author",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
