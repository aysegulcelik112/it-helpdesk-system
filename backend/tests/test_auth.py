"""
Kimlik Doğrulama Testleri

JWT authentication ve rol bazlı yetkilendirme testleri.
"""

import pytest
from fastapi import status

def test_register_success(client):
    """Test: Başarılı kullanıcı kaydı"""
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Yeni Kullanıcı",
            "email": "yeni@test.com",
            "password": "secure123",
            "department": "Test"
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "yeni@test.com"
    assert data["user"]["role"] == "employee"  # Varsayılan rol

def test_register_duplicate_email(client, test_employee):
    """Test: Aynı e-posta ile tekrar kayıt olma (başarısız olmalı)"""
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Başka Kullanıcı",
            "email": test_employee.email,  # Zaten kayıtlı e-posta
            "password": "password123",
            "department": "Test"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "zaten kayıtlı" in response.json()["detail"].lower()

def test_login_success(client, test_employee):
    """Test: Başarılı giriş"""
    response = client.post(
        "/auth/login",
        json={
            "username": test_employee.email,
            "password": "test123"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_employee.email

def test_login_wrong_password(client, test_employee):
    """Test: Yanlış şifre ile giriş (başarısız olmalı)"""
    response = client.post(
        "/auth/login",
        json={
            "username": test_employee.email,
            "password": "yanlis_sifre"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_nonexistent_user(client):
    """Test: Var olmayan kullanıcı ile giriş (başarısız olmalı)"""
    response = client.post(
        "/auth/login",
        json={
            "username": "yokolmayan@test.com",
            "password": "test123"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_me_with_token(client, test_employee):
    """Test: Token ile kullanıcı bilgilerini alma"""
    # Önce login ol ve token al
    login_response = client.post(
        "/auth/login",
        json={
            "username": test_employee.email,
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Token ile /me endpoint'ine istek at
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_employee.email
    assert data["id"] == test_employee.id

def test_get_me_without_token(client):
    """Test: Token olmadan /me endpoint'ine erişim (başarısız olmalı)"""
    response = client.get("/auth/me")
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_me_invalid_token(client):
    """Test: Geçersiz token ile erişim (başarısız olmalı)"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer gecersiz_token_12345"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_role_in_token(client, test_it_staff):
    """Test: Token içinde rol bilgisi doğru mu"""
    # IT personeli ile login ol
    login_response = client.post(
        "/auth/login",
        json={
            "username": test_it_staff.email,
            "password": "test123"
        }
    )
    
    assert login_response.status_code == status.HTTP_200_OK
    data = login_response.json()
    assert data["user"]["role"] == "it_staff"
    
    # Token ile kullanıcı bilgilerini al
    token = data["access_token"]
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert me_response.status_code == status.HTTP_200_OK
    assert me_response.json()["role"] == "it_staff"

def test_refresh_token(client, test_employee):
    """Test: Token yenileme"""
    # Login ol
    login_response = client.post(
        "/auth/login",
        json={
            "username": test_employee.email,
            "password": "test123"
        }
    )
    old_token = login_response.json()["access_token"]
    
    # Token'ı yenile
    refresh_response = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {old_token}"}
    )
    
    assert refresh_response.status_code == status.HTTP_200_OK
    new_token = refresh_response.json()["access_token"]
    # Not: Token aynı olabilir çünkü aynı data ile oluşturuluyor
    # Önemli olan yeni token'ın çalışması
    
    # Yeni token ile istek yapabilmeli
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {new_token}"}
    )
    assert me_response.status_code == status.HTTP_200_OK
