@echo off
echo ===================================
echo IT Helpdesk System - Frontend
echo ===================================
echo.

cd frontend

echo Checking node_modules...
if not exist "node_modules\" (
    echo Installing dependencies...
    npm install
)

echo.
echo ===================================
echo Starting Frontend Server...
echo ===================================
echo App: http://localhost:5173
echo.

npm run dev
