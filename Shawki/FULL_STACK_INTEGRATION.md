# Full Stack Integration Guide

## Overview

This guide shows how to run the complete system: Auth Service + Frontend

---

## Quick Start (5 minutes)

### Step 1: Start Auth Service (Terminal 1)

```bash
cd services/auth-service
docker-compose up --build
```

Wait for: "Database tables created successfully!"

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:3000**

---

## Complete System Architecture

```
┌─────────────┐
│   Browser   │
│ localhost:  │
│    3000     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Frontend   │
│   (React)   │
│  Port: 3000 │
└──────┬──────┘
       │
       │ HTTP Requests
       │ Authorization: Bearer {token}
       │
       ▼
┌─────────────┐
│Auth Service │
│   (Flask)   │
│  Port: 5001 │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │
│  Port: 5432 │
└─────────────┘
```

---

## Test the Complete Flow

### 1. Register a New User

**Frontend:**
1. Go to http://localhost:3000/register
2. Fill in:
   - Name: Masum Ahmed
   - Email: masum@example.com
   - Phone: 01712345678
   - Password: password123
3. Click "Create Account"

**Backend:**
```bash
# Check logs
docker-compose logs auth-service

# Should see:
# POST /api/auth/register - 201
```

**Result:**
- User created in database
- JWT token generated
- User logged in automatically
- Redirected to dashboard

---

### 2. Login

**Frontend:**
1. Go to http://localhost:3000/login
2. Enter:
   - Email: masum@example.com
   - Password: password123
3. Click "Login"

**Backend:**
```bash
# Check logs
docker-compose logs auth-service

# Should see:
# POST /api/auth/login - 200
```

**Result:**
- Credentials verified
- JWT token returned
- Token stored in localStorage
- Redirected to dashboard

---

### 3. Search Trains

**Frontend:**
1. On dashboard, select:
   - From: Dhaka
   - To: Chittagong
   - Date: Today
2. Click "Search Trains"

**Result:**
- Shows 3 mock trains
- Displays prices and availability
- Can select a train

---

### 4. Select Seat

**Frontend:**
1. Click "Select" on a train
2. See seat map (5x11 grid)
3. Click a green seat
4. Click "Reserve Seat"

**Result:**
- Seat selected
- Booking created
- 5-minute timer starts
- Redirected to booking page

---

### 5. Verify OTP

**Frontend:**
1. Click "Resend OTP"
2. See toast: "Test OTP: 123456"
3. Enter: 123456
4. Click "Verify OTP"

**Backend:**
```bash
# Check logs
docker-compose logs auth-service

# Should see:
# POST /api/auth/otp/request - 200
# POST /api/auth/otp/verify - 200
```

**Result:**
- OTP verified
- Proceeds to payment

---

### 6. Complete Payment

**Frontend:**
1. Review booking summary
2. Click "Confirm Payment"

**Result:**
- Payment processed (mock)
- Booking confirmed
- Ticket generated
- Success screen shown

---

## API Flow Diagram

```
Frontend                Auth Service           Database
   │                         │                     │
   │  POST /api/auth/register│                     │
   ├────────────────────────>│                     │
   │                         │  INSERT user        │
   │                         ├────────────────────>│
   │                         │<────────────────────┤
   │                         │  Generate JWT       │
   │<────────────────────────┤                     │
   │  { token, user }        │                     │
   │                         │                     │
   │  POST /api/auth/login   │                     │
   ├────────────────────────>│                     │
   │                         │  SELECT user        │
   │                         ├────────────────────>│
   │                         │<────────────────────┤
   │                         │  Verify password    │
   │                         │  Generate JWT       │
   │<────────────────────────┤                     │
   │  { token, user }        │                     │
   │                         │                     │
   │  GET /api/auth/me       │                     │
   │  Authorization: Bearer  │                     │
   ├────────────────────────>│                     │
   │                         │  Decode JWT         │
   │                         │  SELECT user        │
   │                         ├────────────────────>│
   │                         │<────────────────────┤
   │<────────────────────────┤                     │
   │  { user }               │                     │
```

---

## Environment Variables

### Auth Service (.env)
```bash
DATABASE_URL=postgresql://postgres:password@postgres:5432/auth_db
SECRET_KEY=hackathon-secret-key-2024
JWT_EXPIRATION_HOURS=24
PORT=5001
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:5001
```

---

## Troubleshooting

### Frontend can't connect to backend

**Check:**
1. Auth service is running: `docker-compose ps`
2. Port 5001 is accessible: `curl http://localhost:5001/health`
3. CORS is enabled (already configured in auth service)
4. .env file has correct VITE_API_URL

**Fix:**
```bash
# Restart auth service
cd services/auth-service
docker-compose restart

# Check frontend .env
cd frontend
cat .env
# Should have: VITE_API_URL=http://localhost:5001
```

---

### CORS errors

**Symptom:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Fix:**
Auth service already has Flask-CORS enabled. If still seeing errors:

```python
# In services/auth-service/app.py
# CORS is already configured:
CORS(app)  # Allows all origins
```

---

### JWT token not working

**Check:**
1. Token is stored: `localStorage.getItem('token')`
2. Token is sent: Check Network tab → Headers → Authorization
3. Token is valid: Decode at jwt.io

**Fix:**
```javascript
// In frontend/src/utils/api.js
// Token is automatically added:
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

---

### Database connection error

**Symptom:**
```
could not connect to server: Connection refused
```

**Fix:**
```bash
# Check postgres is running
docker-compose ps

# Restart postgres
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

---

## Testing Checklist

- [ ] Auth service health check works
- [ ] Frontend loads at localhost:3000
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Dashboard shows after login
- [ ] Can search trains
- [ ] Can select seat
- [ ] Can request OTP
- [ ] Can verify OTP
- [ ] Can complete payment
- [ ] Can see ticket

---

## Next Steps

### For Person 2 (Backend):

1. **Create Train Service**
   - Copy jwt_helper.py from auth service
   - Use same SECRET_KEY
   - Implement train search API
   - Implement seat availability API

2. **Create Booking Service**
   - Copy jwt_helper.py from auth service
   - Use same SECRET_KEY
   - Implement seat locking with Redis
   - Implement booking confirmation

3. **Update Frontend API**
   - Replace mock data in `frontend/src/utils/api.js`
   - Point to real Train/Booking services

---

## Docker Compose (All Services)

When all services are ready, create main `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  auth-service:
    build: ./services/auth-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/auth_db
      SECRET_KEY: hackathon-secret-key-2024
    ports:
      - "5001:5001"
    depends_on:
      - postgres

  train-service:
    build: ./services/train-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/train_db
      SECRET_KEY: hackathon-secret-key-2024
    ports:
      - "5002:5002"
    depends_on:
      - postgres

  booking-service:
    build: ./services/booking-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/booking_db
      SECRET_KEY: hackathon-secret-key-2024
      REDIS_URL: redis://redis:6379
    ports:
      - "5003:5003"
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    environment:
      VITE_API_URL: http://localhost:80
    ports:
      - "3000:3000"
    depends_on:
      - auth-service
```

---

## Summary

✅ Auth Service running on port 5001
✅ Frontend running on port 3000
✅ Complete authentication flow working
✅ JWT tokens working
✅ Database connected
✅ Ready for additional services

**The foundation is solid! Time to build the rest!** 🚀
