@echo off
echo ===================================
echo IT Helpdesk System - Backend
echo ===================================
echo.

cd backend

echo Checking virtual environment...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Checking database...
if not exist "helpdesk.db" (
    echo Initializing database...
    python init_db.py
)

echo.
echo ===================================
echo Starting Backend Server...
echo ===================================
echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo.

uvicorn main:app --reload
