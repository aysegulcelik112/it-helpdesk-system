"""
Ticket (Talep) Testleri

Talep oluşturma, listeleme ve güncelleme testleri.
Rol bazlı erişim kontrolü özellikle test edilir.
"""

import pytest
from fastapi import status

def get_auth_header(client, email, password):
    """Login yapıp token al"""
    response = client.post("/auth/login", json={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_ticket_success(client, test_employee):
    """Test: Çalışan talep oluşturabilir"""
    headers = get_auth_header(client, test_employee.email, "test123")
    
    response = client.post(
        "/tickets/",
        json={
            "title": "Yazıcı çalışmıyor",
            "description": "Ofis yazıcısı kağıt sıkışması veriyor",
            "category": "Donanım",
            "priority": "Orta"
        },
        headers=headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Yazıcı çalışmıyor"
    assert data["status"] == "Açık"  # Varsayılan durum
    assert data["creator_id"] == test_employee.id

def test_create_ticket_without_auth(client):
    """Test: Token olmadan talep oluşturulamaz"""
    response = client.post(
        "/tickets/",
        json={
            "title": "Test talep",
            "description": "Test açıklama",
            "category": "Yazılım",
            "priority": "Düşük"
        }
    )
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_employee_sees_only_own_tickets(client, test_employee, test_it_staff, db):
    """Test: Çalışan sadece kendi taleplerini görür"""
    from models import Ticket, TicketCategory, TicketPriority
    
    # Çalışanın talebi
    employee_ticket = Ticket(
        title="Çalışan talebi",
        description="Test",
        category=TicketCategory.SOFTWARE,
        priority=TicketPriority.MEDIUM,
        creator_id=test_employee.id
    )
    
    # IT personelinin talebi
    it_ticket = Ticket(
        title="IT talebi",
        description="Test",
        category=TicketCategory.HARDWARE,
        priority=TicketPriority.HIGH,
        creator_id=test_it_staff.id
    )
    
    db.add_all([employee_ticket, it_ticket])
    db.commit()
    
    # Çalışan login
    headers = get_auth_header(client, test_employee.email, "test123")
    response = client.get("/tickets/", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    tickets = response.json()
    
    # Sadece kendi talebini görmeli
    assert len(tickets) == 1
    assert tickets[0]["title"] == "Çalışan talebi"

def test_it_staff_sees_all_tickets(client, test_employee, test_it_staff, db):
    """Test: IT personeli tüm talepleri görür"""
    from models import Ticket, TicketCategory, TicketPriority
    
    # İki farklı kullanıcının talepleri
    ticket1 = Ticket(
        title="Çalışan talebi",
        description="Test",
        category=TicketCategory.SOFTWARE,
        priority=TicketPriority.MEDIUM,
        creator_id=test_employee.id
    )
    
    ticket2 = Ticket(
        title="IT talebi",
        description="Test",
        category=TicketCategory.HARDWARE,
        priority=TicketPriority.HIGH,
        creator_id=test_it_staff.id
    )
    
    db.add_all([ticket1, ticket2])
    db.commit()
    
    # IT personeli login
    headers = get_auth_header(client, test_it_staff.email, "test123")
    response = client.get("/tickets/", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    tickets = response.json()
    
    # Tüm talepleri görmeli
    assert len(tickets) == 2

def test_employee_cannot_view_other_ticket(client, test_employee, test_it_staff, db):
    """Test: Çalışan başka birinin talebini görememeli"""
    from models import Ticket, TicketCategory, TicketPriority
    
    # IT personelinin talebi
    ticket = Ticket(
        title="IT talebi",
        description="Test",
        category=TicketCategory.HARDWARE,
        priority=TicketPriority.HIGH,
        creator_id=test_it_staff.id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    # Çalışan bu talebi görmeye çalışsın
    headers = get_auth_header(client, test_employee.email, "test123")
    response = client.get(f"/tickets/{ticket.id}", headers=headers)
    
    # 403 Forbidden dönmeli
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_it_staff_can_update_ticket(client, test_employee, test_it_staff, db):
    """Test: IT personeli talebi güncelleyebilir"""
    from models import Ticket, TicketCategory, TicketPriority
    
    ticket = Ticket(
        title="Test talep",
        description="Test",
        category=TicketCategory.SOFTWARE,
        priority=TicketPriority.MEDIUM,
        creator_id=test_employee.id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    # IT personeli durumu güncellesin
    headers = get_auth_header(client, test_it_staff.email, "test123")
    response = client.patch(
        f"/tickets/{ticket.id}",
        json={"status": "İşleme Alındı"},
        headers=headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "İşleme Alındı"

def test_employee_cannot_update_ticket(client, test_employee, db):
    """Test: Çalışan talebi güncelleyemez (IT personeli yetkisi gerekir)"""
    from models import Ticket, TicketCategory, TicketPriority
    
    ticket = Ticket(
        title="Test talep",
        description="Test",
        category=TicketCategory.SOFTWARE,
        priority=TicketPriority.MEDIUM,
        creator_id=test_employee.id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    # Çalışan durumu güncellemeye çalışsın
    headers = get_auth_header(client, test_employee.email, "test123")
    response = client.patch(
        f"/tickets/{ticket.id}",
        json={"status": "Çözüldü"},
        headers=headers
    )
    
    # 403 Forbidden dönmeli
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_assign_to_me(client, test_employee, test_it_staff, db):
    """Test: IT personeli talebi kendine atayabilir"""
    from models import Ticket, TicketCategory, TicketPriority
    
    ticket = Ticket(
        title="Test talep",
        description="Test",
        category=TicketCategory.NETWORK,
        priority=TicketPriority.HIGH,
        creator_id=test_employee.id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    assert ticket.assigned_to_id is None  # Başlangıçta atanmamış
    
    # IT personeli kendine atsın
    headers = get_auth_header(client, test_it_staff.email, "test123")
    response = client.post(f"/tickets/{ticket.id}/assign-to-me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["assigned_to_id"] == test_it_staff.id
    assert data["status"] == "İşleme Alındı"  # Durum otomatik güncellenmeli

def test_employee_can_close_own_ticket(client, test_employee, db):
    """Test: Çalışan kendi talebini kapatabilir"""
    from models import Ticket, TicketCategory, TicketPriority, TicketStatus
    
    ticket = Ticket(
        title="Test talep",
        description="Test",
        category=TicketCategory.SOFTWARE,
        priority=TicketPriority.LOW,
        status=TicketStatus.RESOLVED,
        creator_id=test_employee.id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    headers = get_auth_header(client, test_employee.email, "test123")
    response = client.post(f"/tickets/{ticket.id}/close", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "Kapatıldı"
