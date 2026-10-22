#!/bin/bash

echo "==================================="
echo "IT Helpdesk System - Frontend"
echo "==================================="
echo ""

cd frontend

echo "Checking node_modules..."
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "==================================="
echo "Starting Frontend Server..."
echo "==================================="
echo "App: http://localhost:5173"
echo ""

npm run dev
