"""
Yetkilendirme Testleri

Rol bazlı erişim kontrolü testleri.
Bu testler IT personeli ve çalışan rollerinin doğru çalıştığını kontrol eder.
"""

import pytest
from fastapi import status, Depends
from auth import require_it_staff, get_current_user
from models import User

def test_employee_role_assigned_correctly(client):
    """Test: Yeni kayıt olan kullanıcıya employee rolü atanıyor mu"""
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Çalışan Test",
            "email": "calisan@test.com",
            "password": "test123",
            "department": "Test"
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user"]["role"] == "employee"

def test_it_staff_cannot_register_via_api(client):
    """
    Test: Normal kayıt endpoint'i ile IT personeli oluşturulamaz
    
    Güvenlik: IT personeli manuel olarak veritabanından oluşturulmalı,
    herkes kendini admin yapamamalı.
    """
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Sahte Admin",
            "email": "fake.admin@test.com",
            "password": "test123",
            "department": "IT"
        }
    )
    
    # Kayıt başarılı ama rol employee olmalı
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user"]["role"] == "employee"  # it_staff değil!

def test_password_not_returned_in_response(client, test_employee):
    """Test: API yanıtlarında şifre dönmemeli (güvenlik)"""
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": test_employee.email,
            "password": "test123"
        }
    )
    
    data = login_response.json()
    assert "password" not in data["user"]
    assert "hashed_password" not in data["user"]
    
    # /me endpoint
    token = data["access_token"]
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    me_data = me_response.json()
    assert "password" not in me_data
    assert "hashed_password" not in me_data

def test_token_contains_necessary_info(client, test_employee):
    """Test: Token içinde gerekli bilgiler var mı (user_id, role, email)"""
    from auth.jwt import decode_access_token
    
    # Login ve token al
    login_response = client.post(
        "/auth/login",
        json={
            "username": test_employee.email,
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Token'ı decode et ve içeriğini kontrol et
    payload = decode_access_token(token)
    
    assert "sub" in payload  # user_id
    assert "role" in payload
    assert "email" in payload
    assert payload["role"] == "employee"
    assert payload["email"] == test_employee.email

def test_different_users_get_different_tokens(client, test_employee, test_it_staff):
    """Test: Farklı kullanıcılar farklı token alıyor mu"""
    # Çalışan login
    employee_response = client.post(
        "/auth/login",
        json={
            "username": test_employee.email,
            "password": "test123"
        }
    )
    employee_token = employee_response.json()["access_token"]
    
    # IT personeli login
    it_response = client.post(
        "/auth/login",
        json={
            "username": test_it_staff.email,
            "password": "test123"
        }
    )
    it_token = it_response.json()["access_token"]
    
    # Token'lar farklı olmalı
    assert employee_token != it_token
    
    # Her token kendi kullanıcı bilgilerini döndürmeli
    employee_me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {employee_token}"}
    ).json()
    
    it_me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {it_token}"}
    ).json()
    
    assert employee_me["email"] == test_employee.email
    assert it_me["email"] == test_it_staff.email
    assert employee_me["role"] == "employee"
    assert it_me["role"] == "it_staff"
