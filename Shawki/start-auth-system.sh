#!/bin/bash

echo "========================================"
echo "Starting Authentication System"
echo "========================================"
echo ""

echo "[1/2] Starting Auth Service with Docker..."
cd services/auth-service
docker-compose up --build -d
cd ../..

echo ""
echo "[2/2] Waiting for Auth Service to be ready..."
sleep 15

echo ""
echo "========================================"
echo "Auth Service Status"
echo "========================================"
curl http://localhost:5001/health
echo ""
echo ""

echo "========================================"
echo "Services Running:"
echo "========================================"
echo "- Auth Service: http://localhost:5001"
echo "- PostgreSQL: localhost:5432"
echo ""
echo "To start frontend, run:"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""
