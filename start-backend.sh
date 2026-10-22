#!/bin/bash

echo "==================================="
echo "IT Helpdesk System - Backend"
echo "==================================="
echo ""

cd backend

echo "Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Checking database..."
if [ ! -f "helpdesk.db" ]; then
    echo "Initializing database..."
    python init_db.py
fi

echo ""
echo "==================================="
echo "Starting Backend Server..."
echo "==================================="
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo ""

uvicorn main:app --reload
