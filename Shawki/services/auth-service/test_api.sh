#!/bin/bash

# Test script for Auth Service API
BASE_URL="http://localhost:5001"

echo "========================================="
echo "Testing Auth Service API"
echo "========================================="
echo ""

# 1. Health Check
echo "1. Testing Health Check..."
curl -X GET "$BASE_URL/health"
echo -e "\n"

# 2. Register User
echo "2. Testing User Registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "masum@example.com",
    "password": "password123",
    "name": "Masum Ahmed",
    "phone": "01712345678"
  }')
echo $REGISTER_RESPONSE | python -m json.tool
TOKEN=$(echo $REGISTER_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)
echo -e "\n"

# 3. Login
echo "3. Testing User Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "masum@example.com",
    "password": "password123"
  }')
echo $LOGIN_RESPONSE | python -m json.tool
echo -e "\n"

# 4. Request OTP
echo "4. Testing OTP Request..."
OTP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/otp/request" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "01712345678"
  }')
echo $OTP_RESPONSE | python -m json.tool
echo -e "\n"

# 5. Verify OTP
echo "5. Testing OTP Verification..."
curl -s -X POST "$BASE_URL/api/auth/otp/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "01712345678",
    "otp": "123456"
  }' | python -m json.tool
echo -e "\n"

# 6. Verify Token
echo "6. Testing Token Verification..."
curl -s -X GET "$BASE_URL/api/auth/verify-token" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
echo -e "\n"

# 7. Get Current User
echo "7. Testing Get Current User..."
curl -s -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
echo -e "\n"

echo "========================================="
echo "All tests completed!"
echo "========================================="
