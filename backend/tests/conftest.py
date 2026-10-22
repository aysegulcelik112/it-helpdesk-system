"""
Pytest Konfigürasyon ve Fixture'lar

Test için ortak kullanılan fixture'lar burada tanımlanır.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import User, UserRole
from auth import hash_password

# Test için in-memory SQLite veritabanı
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Her test için yeni bir veritabanı oluştur"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """FastAPI test client"""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_employee(db):
    """Test çalışan kullanıcısı"""
    user = User(
        full_name="Test Employee",
        email="employee@test.com",
        hashed_password=hash_password("test123"),
        role=UserRole.EMPLOYEE,
        department="Test"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_it_staff(db):
    """Test IT personeli kullanıcısı"""
    user = User(
        full_name="Test IT Staff",
        email="it@test.com",
        hashed_password=hash_password("test123"),
        role=UserRole.IT_STAFF,
        department="IT"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
