@echo off
echo ========================================
echo Testing Authentication System
echo ========================================
echo.

echo [1/4] Testing Health Check...
curl -s http://localhost:5001/health
echo.
echo.

echo [2/4] Testing User Registration...
curl -s -X POST http://localhost:5001/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test%RANDOM%@example.com\",\"phone\":\"01712345678\",\"password\":\"password123\"}"
echo.
echo.

echo [3/4] Testing User Login...
curl -s -X POST http://localhost:5001/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"masum@example.com\",\"password\":\"password123\"}"
echo.
echo.

echo [4/4] Testing OTP Request...
curl -s -X POST http://localhost:5001/api/auth/otp/request ^
  -H "Content-Type: application/json" ^
  -d "{\"phone\":\"01712345678\"}"
echo.
echo.

echo ========================================
echo Test Complete!
echo ========================================
echo.
pause
