# How to Test Auth Service

## Quick Test (Recommended)

### Step 1: Start the service
```bash
cd services/auth-service
docker-compose up --build
```

Wait for the message: "Database tables created successfully!"

### Step 2: Test in another terminal

#### Option A: Using curl (Windows PowerShell)
```powershell
# Health check
curl http://localhost:5001/health

# Register user
curl -X POST http://localhost:5001/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"masum@example.com\",\"password\":\"password123\",\"name\":\"Masum Ahmed\",\"phone\":\"01712345678\"}'

# Login
curl -X POST http://localhost:5001/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"masum@example.com\",\"password\":\"password123\"}'
```

#### Option B: Using Python
```bash
# Install requests
pip install requests

# Run test
python -c "
import requests

# Register
r = requests.post('http://localhost:5001/api/auth/register', json={
    'email': 'test@example.com',
    'password': 'password123',
    'name': 'Test User',
    'phone': '01712345678'
})
print('Register:', r.json())
token = r.json()['token']

# Login
r = requests.post('http://localhost:5001/api/auth/login', json={
    'email': 'test@example.com',
    'password': 'password123'
})
print('Login:', r.json())

# Get user info
r = requests.get('http://localhost:5001/api/auth/me',
    headers={'Authorization': f'Bearer {token}'})
print('User Info:', r.json())
"
```

#### Option C: Using Browser/Postman

1. Open Postman or any REST client
2. Import this collection:

**Register User:**
- Method: POST
- URL: http://localhost:5001/api/auth/register
- Body (JSON):
```json
{
  "email": "masum@example.com",
  "password": "password123",
  "name": "Masum Ahmed",
  "phone": "01712345678"
}
```

**Login:**
- Method: POST
- URL: http://localhost:5001/api/auth/login
- Body (JSON):
```json
{
  "email": "masum@example.com",
  "password": "password123"
}
```

**Get User Info:**
- Method: GET
- URL: http://localhost:5001/api/auth/me
- Headers:
  - Authorization: Bearer YOUR_TOKEN_HERE

## Unit Tests

```bash
# Install pytest
pip install pytest requests

# Run tests
docker-compose exec auth-service pytest test_auth.py -v

# Or run locally
pytest test_auth.py -v
```

## Expected Results

### ✅ Successful Registration
```json
{
  "message": "User registered successfully",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "masum@example.com",
    "name": "Masum Ahmed",
    "phone": "01712345678",
    "created_at": "2024-01-20T10:30:00"
  }
}
```

### ✅ Successful Login
```json
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "masum@example.com",
    "name": "Masum Ahmed",
    "phone": "01712345678",
    "created_at": "2024-01-20T10:30:00"
  }
}
```

### ✅ OTP Request
```json
{
  "message": "OTP sent successfully",
  "otp": "123456",
  "expires_in": 300
}
```

### ✅ OTP Verify
```json
{
  "message": "OTP verified successfully",
  "verified": true
}
```

## Troubleshooting

### Port 5001 already in use
```bash
# Find process using port
netstat -ano | findstr :5001

# Kill process or change port in docker-compose.yml
```

### Database connection error
```bash
# Check if postgres is running
docker-compose ps

# Restart services
docker-compose restart

# Check logs
docker-compose logs postgres
```

### "User already exists" error
```bash
# This is expected if you register the same email twice
# Use a different email or reset database:
docker-compose down -v
docker-compose up --build
```

## Clean Up

```bash
# Stop services
docker-compose down

# Remove volumes (clean database)
docker-compose down -v
```

## Next Steps

Once auth service is working:
1. ✅ Auth Service (Done!)
2. Create Notification Service
3. Create API Gateway
4. Integrate with other services
