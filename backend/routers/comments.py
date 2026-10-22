"""
Comments Router

Talep yorumları endpoint'leri.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import TicketComment, Ticket, User, UserRole
from schemas import CommentCreate, CommentResponse
from auth import get_current_user

router = APIRouter()

@router.post("/tickets/{ticket_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    ticket_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Talebe yorum ekle
    
    Talep sahibi veya IT personeli yorum ekleyebilir.
    Başka bir çalışanın talebine yorum eklenemez.
    
    Args:
        ticket_id: Talep ID
        comment_data: Yorum metni
        current_user: Mevcut kullanıcı
        db: Veritabanı session
    
    Returns:
        Oluşturulan yorum
    
    Raises:
        HTTPException 404: Talep bulunamadı
        HTTPException 403: Bu talebe yorum ekleme yetkiniz yok
    """
    # Talebi bul
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talep bulunamadı"
        )
    
    # Yetki kontrolü: Talep sahibi veya IT personeli yorum ekleyebilir
    if current_user.role == UserRole.EMPLOYEE and ticket.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu talebe yorum ekleme yetkiniz yok"
        )
    
    # Yeni yorum oluştur
    new_comment = TicketComment(
        ticket_id=ticket_id,
        author_id=current_user.id,
        message=comment_data.message
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return CommentResponse.model_validate(new_comment)

@router.get("/tickets/{ticket_id}/comments", response_model=List[CommentResponse])
def get_comments(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Talebin yorumlarını listele
    
    ROL BAZLI ERİŞİM:
    - Çalışan: Sadece kendi talebinin yorumlarını görebilir
    - IT Personeli: Herhangi bir talebin yorumlarını görebilir
    
    Args:
        ticket_id: Talep ID
        current_user: Mevcut kullanıcı
        db: Veritabanı session
    
    Returns:
        Yorum listesi (eskiden yeniye)
    
    Raises:
        HTTPException 404: Talep bulunamadı
        HTTPException 403: Bu talebin yorumlarına erişim yetkiniz yok
    """
    # Talebi bul
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talep bulunamadı"
        )
    
    # Yetki kontrolü
    if current_user.role == UserRole.EMPLOYEE and ticket.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu talebin yorumlarına erişim yetkiniz yok"
        )
    
    # Yorumları getir (eski -> yeni)
    comments = db.query(TicketComment)\
        .filter(TicketComment.ticket_id == ticket_id)\
        .order_by(TicketComment.created_at.asc())\
        .all()
    
    return [CommentResponse.model_validate(c) for c in comments]
