"""
Tickets Router

Talep (ticket) yönetimi endpoint'leri.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Ticket, User, UserRole, TicketStatus
from schemas import TicketCreate, TicketUpdate, TicketResponse, TicketListResponse
from auth import get_current_user, require_it_staff

router = APIRouter()

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Yeni talep oluştur
    
    Herhangi bir kullanıcı (employee veya it_staff) yeni talep açabilir.
    Talep varsayılan olarak "Açık" durumunda oluşturulur.
    
    Args:
        ticket_data: Talep bilgileri
        current_user: Talebi oluşturan kullanıcı
        db: Veritabanı session
    
    Returns:
        Oluşturulan talep
    """
    # Yeni talep oluştur
    new_ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        category=ticket_data.category,
        priority=ticket_data.priority,
        status=TicketStatus.OPEN,  # Varsayılan durum
        creator_id=current_user.id
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    return TicketResponse.model_validate(new_ticket)

@router.get("/", response_model=List[TicketListResponse])
def list_tickets(
    status_filter: Optional[str] = Query(None, description="Duruma göre filtrele"),
    category: Optional[str] = Query(None, description="Kategoriye göre filtrele"),
    priority: Optional[str] = Query(None, description="Önceliğe göre filtrele"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Talep listesi
    
    ROL BAZLI DAVRANŞ:
    - Çalışan (employee): Sadece kendi açtığı talepleri görür
    - IT Personeli (it_staff): Tüm talepleri görür
    
    Filtreleme opsiyonları:
    - status: Duruma göre filtre (Açık, İşleme Alındı, vb.)
    - category: Kategoriye göre filtre
    - priority: Önceliğe göre filtre
    
    Args:
        status_filter: Durum filtresi (opsiyonel)
        category: Kategori filtresi (opsiyonel)
        priority: Öncelik filtresi (opsiyonel)
        current_user: Mevcut kullanıcı
        db: Veritabanı session
    
    Returns:
        Talep listesi
    """


    # Base query
    query = db.query(Ticket)
    
    # ROL BAZLI FİLTRELEME - ÖNEMLİ!
    if current_user.role == UserRole.EMPLOYEE:
        # Çalışan sadece kendi taleplerini görebilir
        query = query.filter(Ticket.creator_id == current_user.id)
    # IT personeli tüm talepleri görebilir (ek filtre yok)
    
    # Durum filtresi
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    
    # Kategori filtresi
    if category:
        query = query.filter(Ticket.category == category)
    
    # Öncelik filtresi
    if priority:
        query = query.filter(Ticket.priority == priority)
    
    # Son güncellenen en üstte
    query = query.order_by(Ticket.updated_at.desc())
    
    tickets = query.all()
    return [TicketListResponse.model_validate(t) for t in tickets]

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Talep detayı
    
    ROL BAZLI ERİŞİM:
    - Çalışan: Sadece kendi talebini görebilir
    - IT Personeli: Herhangi bir talebi görebilir
    
    Args:
        ticket_id: Talep ID
        current_user: Mevcut kullanıcı
        db: Veritabanı session
    
    Returns:
        Talep detayları
    
    Raises:
        HTTPException 404: Talep bulunamadı
        HTTPException 403: Bu talebe erişim yetkiniz yok
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talep bulunamadı"
        )
    
    # ROL BAZLI YETKİLENDİRME
    if current_user.role == UserRole.EMPLOYEE and ticket.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu talebe erişim yetkiniz yok"
        )
    
    return TicketResponse.model_validate(ticket)

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    it_user: User = Depends(require_it_staff),  # Sadece IT personeli
    db: Session = Depends(get_db)
):
    """
    Talep güncelle (Sadece IT Personeli)
    
    IT personeli talep durumunu, atanan kişiyi ve önceliği güncelleyebilir.
    
    Args:
        ticket_id: Talep ID
        ticket_update: Güncellenecek alanlar
        it_user: IT personeli kullanıcı
        db: Veritabanı session
    
    Returns:
        Güncellenmiş talep
    
    Raises:
        HTTPException 404: Talep bulunamadı
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talep bulunamadı"
        )
    
    # Güncellemeleri uygula
    if ticket_update.status is not None:
        ticket.status = ticket_update.status
    
    if ticket_update.assigned_to_id is not None:
        ticket.assigned_to_id = ticket_update.assigned_to_id
    
    if ticket_update.priority is not None:
        ticket.priority = ticket_update.priority
    
    db.commit()
    db.refresh(ticket)
    
    return TicketResponse.model_validate(ticket)

@router.post("/{ticket_id}/assign-to-me", response_model=TicketResponse)
def assign_to_me(
    ticket_id: int,
    it_user: User = Depends(require_it_staff),
    db: Session = Depends(get_db)
):
    """
    Talebi kendine ata (IT Personeli)
    
    IT personeli bir talebi hızlıca kendine atayabilir.
    
    Args:
        ticket_id: Talep ID
        it_user: IT personeli kullanıcı
        db: Veritabanı session
    
    Returns:
        Güncellenmiş talep
    
    Raises:
        HTTPException 404: Talep bulunamadı
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talep bulunamadı"
        )
    
    # Kendine ata
    ticket.assigned_to_id = it_user.id
    
    # Durum "Açık" ise "İşleme Alındı" yap
    if ticket.status == TicketStatus.OPEN:
        ticket.status = TicketStatus.IN_PROGRESS
    
    db.commit()
    db.refresh(ticket)
    
    return TicketResponse.model_validate(ticket)

@router.post("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Talebi kapat
    
    Talep sahibi veya IT personeli talebi kapatabilir.
    Genellikle sorun çözüldükten sonra kullanılır.
    
    Args:
        ticket_id: Talep ID
        current_user: Mevcut kullanıcı
        db: Veritabanı session
    
    Returns:
        Kapatılmış talep
    
    Raises:
        HTTPException 404: Talep bulunamadı
        HTTPException 403: Bu işlem için yetkiniz yok
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talep bulunamadı"
        )
    
    # Yetki kontrolü: Talep sahibi veya IT personeli
    if current_user.role == UserRole.EMPLOYEE and ticket.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu talebi kapatma yetkiniz yok"
        )
    
    ticket.status = TicketStatus.CLOSED
    
    db.commit()
    db.refresh(ticket)
    
    return TicketResponse.model_validate(ticket)
