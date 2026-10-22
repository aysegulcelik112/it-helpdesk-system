"""
IT Destek Talep Sistemi - Ana Uygulama Dosyası

Bu dosya FastAPI uygulamasını başlatır ve tüm router'ları yapılandırır.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Modelleri import et (Base.metadata'ya kaydetmek için gerekli)
from models import User, Ticket, TicketComment

# Veritabanı tablolarını oluştur
# Uygulama başlatılırken tablolar otomatik olarak oluşturulur
Base.metadata.create_all(bind=engine)

# Uygulama instance'ı oluştur
app = FastAPI(
    title="IT Helpdesk System API",
    description="Şirket içi IT destek taleplerini yönetmek için REST API",
    version="1.0.0"
)

# CORS ayarları - Frontend'in backend'e erişebilmesi için
# Geliştirme ortamında tüm origin'lere izin veriyoruz
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173"
    ],  # Vite ve React default portları
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver (GET, POST, PUT, DELETE vb.)
    allow_headers=["*"],  # Tüm header'lara izin ver
)

# Sağlık kontrolü endpoint'i - API'nin çalışıp çalışmadığını kontrol etmek için
@app.get("/")
def root():
    """Ana endpoint - API'nin aktif olduğunu doğrular"""
    return {
        "message": "IT Helpdesk System API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {"status": "healthy"}

# Router'ları import et
from routers import auth, tickets, comments

# Router'ları ekle
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(comments.router, tags=["Comments"])
