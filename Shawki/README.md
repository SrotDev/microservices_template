# 🚂 Train Ticketing System - Hackathon Project

A scalable microservices-based train ticketing system built for Bangladesh Railway to handle high traffic during Eid season.

## 🎯 Project Status

### ✅ Completed (20%)
- **Auth Service** - User registration, login, JWT authentication
- **Frontend** - Complete UI with all pages (Login, Register, Dashboard, Search, Seat Selection, Booking)
- **Docker Setup** - Auth service containerized with PostgreSQL

### ⏭️ In Progress (80%)
- Train Service
- Booking Service (Critical - seat locking with Redis)
- Payment Service
- Notification Service
- API Gateway
- Load Testing
- CI/CD Pipeline

---

## 🚀 Quick Start

### 1. Start Auth Service
```bash
cd services/auth-service
docker-compose up --build
```

Wait for: `Database tables created successfully!`

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:3000**

### 3. Test the System
- Register: Create a new account
- Login: Use your credentials
- Explore: Navigate through all pages

📖 **Detailed Guide:** See [SETUP_AUTH_SYSTEM.md](SETUP_AUTH_SYSTEM.md)

---

## 📁 Project Structure

```
train-ticketing-system/
├── services/
│   ├── auth-service/          ✅ COMPLETE
│   ├── train-service/         ⏭️ TODO
│   ├── booking-service/       ⏭️ TODO (CRITICAL)
│   ├── payment-service/       ⏭️ TODO
│   └── notification-service/  ⏭️ TODO
├── frontend/                  ✅ COMPLETE
├── SETUP_AUTH_SYSTEM.md      📖 Setup guide
├── HACKATHON_PLAN.md         📋 Full plan
└── PROJECT_STATUS.md         📊 Progress tracker
```

---

## 🏗️ Architecture

```
Frontend (React)
    ↓
API Gateway (Nginx)
    ↓
┌─────────┬─────────┬──────────┬─────────┬────────────┐
Auth      Train     Booking    Payment   Notification
Service   Service   Service    Service   Service
    ↓         ↓         ↓          ↓          ↓
PostgreSQL    Redis (Locks)    RabbitMQ
```

---

## 🔑 Key Features

### Implemented
- ✅ User authentication (JWT)
- ✅ Password hashing (bcrypt)
- ✅ Modern React UI
- ✅ Multiple ticket booking
- ✅ Responsive design
- ✅ Docker containerization

### Planned
- ⏭️ Seat locking mechanism (Redis)
- ⏭️ Event-driven architecture (RabbitMQ)
- ⏭️ Horizontal scaling
- ⏭️ Load testing (Locust)
- ⏭️ CI/CD pipeline
- ⏭️ Monitoring (Prometheus/Grafana)

---

## 🛠️ Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router
- Axios

### Backend
- Flask (Python)
- PostgreSQL
- Redis
- RabbitMQ
- JWT

### DevOps
- Docker
- Docker Compose
- Nginx
- GitHub Actions

---

## 📊 Services Overview

### Auth Service (Port 5001) ✅
- User registration
- User login
- JWT token generation
- OTP system (mock)
- Password hashing

### Train Service (Port 5002) ⏭️
- Train search
- Seat availability
- Train schedules
- Seed data

### Booking Service (Port 5003) ⏭️
- Seat selection with Redis locking
- 5-minute timeout
- Booking confirmation
- Event publishing

### Payment Service (Port 5004) ⏭️
- Payment processing (mock)
- Transaction records
- Event publishing

### Notification Service (Port 5005) ⏭️
- Email notifications (mock)
- SMS/OTP (mock)
- RabbitMQ consumer

---

## 🧪 Testing

### Test Auth Service
```bash
# Health check
curl http://localhost:5001/health

# Register user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","phone":"01712345678","password":"password123"}'

# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Or use the test script:
```bash
test-auth-system.bat
```

---

## 📖 Documentation

- [SETUP_AUTH_SYSTEM.md](SETUP_AUTH_SYSTEM.md) - Complete setup guide
- [HACKATHON_PLAN.md](HACKATHON_PLAN.md) - Full implementation plan
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current progress
- [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - System architecture
- [FULL_STACK_INTEGRATION.md](FULL_STACK_INTEGRATION.md) - Integration guide

---

## 🐛 Troubleshooting

### Port Conflicts
```bash
# Check what's using port 5001
netstat -ano | findstr :5001

# Kill process
taskkill /PID <PID> /F
```

### Database Issues
```bash
# Reset database
cd services/auth-service
docker-compose down -v
docker-compose up --build
```

### Frontend Connection Issues
```bash
# Check .env file
cat frontend/.env
# Should have: VITE_API_URL=http://localhost:5001

# Restart frontend
cd frontend
npm run dev
```

---

## 🎯 Next Steps

1. ✅ Auth Service - DONE!
2. ✅ Frontend - DONE!
3. ⏭️ Train Service (2 hours)
4. ⏭️ Booking Service (3 hours) - CRITICAL!
5. ⏭️ Payment Service (1.5 hours)
6. ⏭️ Notification Service (1.5 hours)
7. ⏭️ API Gateway (1.5 hours)
8. ⏭️ Docker Compose Integration (2 hours)
9. ⏭️ Load Testing (3 hours)
10. ⏭️ CI/CD Pipeline (2 hours)

---

## 👥 Team

Built for Bangladesh Railway Hackathon 2024

---

## 📝 License

MIT

---

## 🎉 Current Status

**Auth system is fully operational!** 🚀

- ✅ Backend running in Docker
- ✅ Frontend connected
- ✅ Real authentication working
- ✅ Database persisting data
- ✅ Ready for next microservice

**Time to build the Train Service!** 🚂
