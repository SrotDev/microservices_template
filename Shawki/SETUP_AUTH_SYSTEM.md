# 🚀 Setup Authentication System

## Quick Start (3 Steps)

### Step 1: Start Auth Service (Docker)

**Windows:**
```bash
cd services/auth-service
docker-compose up --build
```

**Or use the startup script:**
```bash
start-auth-system.bat
```

**Linux/Mac:**
```bash
cd services/auth-service
docker-compose up --build
```

**Or:**
```bash
chmod +x start-auth-system.sh
./start-auth-system.sh
```

Wait for the message: `Database tables created successfully!`

### Step 2: Verify Auth Service

Open a new terminal and test:
```bash
curl http://localhost:5001/health
```

Expected response:
```json
{"status": "healthy"}
```

### Step 3: Start Frontend

Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:3000**

---

## 🎯 What's Running

| Service | URL | Port |
|---------|-----|------|
| Auth Service | http://localhost:5001 | 5001 |
| PostgreSQL | localhost:5432 | 5432 |
| Frontend | http://localhost:3000 | 3000 |

---

## ✅ Test the System

### 1. Register a New User

**Frontend:**
- Go to http://localhost:3000/register
- Fill in the form:
  - Name: Masum Ahmed
  - Email: masum@example.com
  - Phone: 01712345678
  - Password: password123
  - Confirm Password: password123
- Click "Create Account"

**Or via API:**
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Masum Ahmed",
    "email": "masum@example.com",
    "phone": "01712345678",
    "password": "password123"
  }'
```

### 2. Login

**Frontend:**
- Go to http://localhost:3000/login
- Email: masum@example.com
- Password: password123
- Click "Login"

**Or via API:**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "masum@example.com",
    "password": "password123"
  }'
```

### 3. Navigate the App

After login, you can:
- ✅ View Dashboard
- ✅ Search Trains (mock data)
- ✅ Select Seats (mock data)
- ✅ Complete Booking (mock data)

---

## 🔧 Configuration

### Auth Service Environment Variables

Located in `services/auth-service/docker-compose.yml`:

```yaml
environment:
  DATABASE_URL: postgresql://postgres:password@postgres:5432/auth_db
  SECRET_KEY: hackathon-secret-key-2024
  JWT_EXPIRATION_HOURS: 24
  PORT: 5001
```

### Frontend Environment Variables

Located in `frontend/.env`:

```
VITE_API_URL=http://localhost:5001
```

---

## 🐛 Troubleshooting

### Issue: Port 5001 already in use

**Solution:**
```bash
# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5001 | xargs kill -9
```

### Issue: Port 5432 already in use (PostgreSQL)

**Solution:**
Stop your local PostgreSQL or change the port in docker-compose.yml:
```yaml
ports:
  - "5433:5432"  # Use 5433 instead
```

### Issue: Frontend can't connect to backend

**Check:**
1. Auth service is running: `curl http://localhost:5001/health`
2. CORS is enabled (already configured)
3. Frontend .env has correct URL: `VITE_API_URL=http://localhost:5001`

**Fix:**
```bash
# Restart auth service
cd services/auth-service
docker-compose restart

# Restart frontend
cd frontend
npm run dev
```

### Issue: "Database connection error"

**Solution:**
```bash
# Stop and remove containers
cd services/auth-service
docker-compose down -v

# Start fresh
docker-compose up --build
```

### Issue: Login fails with "Invalid credentials"

**Check:**
1. User is registered
2. Password is correct
3. Check auth service logs:
```bash
docker-compose logs auth-service
```

---

## 📊 Database Access

### Connect to PostgreSQL

```bash
# Using Docker
docker exec -it auth-postgres psql -U postgres -d auth_db

# View users
SELECT * FROM users;

# Exit
\q
```

### Reset Database

```bash
cd services/auth-service
docker-compose down -v
docker-compose up --build
```

---

## 🔐 API Endpoints

### Public Endpoints (No Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/otp/request` | Request OTP |
| POST | `/api/auth/otp/verify` | Verify OTP |

### Protected Endpoints (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/verify-token` | Verify JWT token |
| GET | `/api/auth/me` | Get current user |

### Example: Protected Request

```bash
# Get token from login
TOKEN="your-jwt-token-here"

# Make authenticated request
curl http://localhost:5001/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎨 Frontend Features

### Connected to Auth Service:
- ✅ Real user registration
- ✅ Real user login
- ✅ JWT token storage
- ✅ Protected routes
- ✅ User session management

### Still Using Mock Data:
- ⏳ Train search (will connect to Train Service)
- ⏳ Seat selection (will connect to Booking Service)
- ⏳ OTP verification (will connect to Notification Service)
- ⏳ Payment (will connect to Payment Service)

---

## 📝 Next Steps

1. ✅ **Auth Service** - RUNNING!
2. ⏭️ **Train Service** - Create and connect
3. ⏭️ **Booking Service** - Create and connect
4. ⏭️ **Payment Service** - Create and connect
5. ⏭️ **Notification Service** - Create and connect

---

## 🛑 Stop Services

### Stop Auth Service
```bash
cd services/auth-service
docker-compose down
```

### Stop Frontend
Press `Ctrl+C` in the terminal running `npm run dev`

### Stop All and Clean Up
```bash
cd services/auth-service
docker-compose down -v  # -v removes volumes (database data)
```

---

## 📦 Docker Commands Reference

```bash
# Start services
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f auth-service

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart a service
docker-compose restart auth-service

# Rebuild a service
docker-compose up --build auth-service
```

---

## ✨ Success Checklist

- [ ] Auth service running on port 5001
- [ ] PostgreSQL running on port 5432
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Frontend running on port 3000
- [ ] Frontend can register users
- [ ] Frontend can login users
- [ ] Dashboard shows after login
- [ ] User name displayed in navbar

---

## 🎉 You're All Set!

The authentication system is now fully operational with:
- ✅ Docker containerization
- ✅ PostgreSQL database
- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ CORS enabled
- ✅ Frontend integration
- ✅ Real user registration & login

**Ready to build the rest of the microservices!** 🚀
