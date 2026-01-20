# Auth Service - Quick Start Guide

## Step 1: Build and Run with Docker Compose

```bash
cd services/auth-service

# Build and start services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The service will be available at: `http://localhost:5001`

## Step 2: Test the API

### Option A: Using curl (Manual Testing)

```bash
# 1. Health Check
curl http://localhost:5001/health

# 2. Register a user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "masum@example.com",
    "password": "password123",
    "name": "Masum Ahmed",
    "phone": "01712345678"
  }'

# Save the token from response
TOKEN="your_token_here"

# 3. Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "masum@example.com",
    "password": "password123"
  }'

# 4. Request OTP
curl -X POST http://localhost:5001/api/auth/otp/request \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "01712345678"
  }'

# 5. Verify OTP
curl -X POST http://localhost:5001/api/auth/otp/verify \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "01712345678",
    "otp": "123456"
  }'

# 6. Get current user (requires token)
curl -X GET http://localhost:5001/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Option B: Using the Test Script

```bash
# Make script executable (Linux/Mac)
chmod +x test_api.sh

# Run tests
./test_api.sh
```

### Option C: Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5001"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User",
    "phone": "01712345678"
})
print(response.json())
token = response.json()['token']

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
print(response.json())

# Get current user
response = requests.get(f"{BASE_URL}/api/auth/me", 
    headers={"Authorization": f"Bearer {token}"})
print(response.json())
```

## Step 3: Run Unit Tests

```bash
# Install test dependencies
pip install pytest requests

# Run tests
docker-compose exec auth-service pytest test_auth.py -v
```

## Step 4: View Logs

```bash
# View all logs
docker-compose logs

# View auth-service logs only
docker-compose logs auth-service

# Follow logs in real-time
docker-compose logs -f auth-service
```

## Step 5: Stop Services

```bash
# Stop services
docker-compose down

# Stop and remove volumes (clean database)
docker-compose down -v
```

## Troubleshooting

### Database Connection Issues

If you see database connection errors:

```bash
# Check if postgres is running
docker-compose ps

# Check postgres logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Port Already in Use

If port 5001 or 5432 is already in use:

```bash
# Change ports in docker-compose.yml
# For auth-service: "5002:5001"
# For postgres: "5433:5432"

# Update DATABASE_URL accordingly
```

### Reset Everything

```bash
# Stop and remove everything
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

## Integration with Other Services

Other services can use this auth service by:

1. **Sending JWT token in headers:**
```python
headers = {
    "Authorization": f"Bearer {token}"
}
```

2. **Decoding JWT directly (recommended):**
```python
import jwt

SECRET_KEY = "hackathon-secret-key-2024"  # Same as auth service

def get_user_from_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id'], payload['email']
    except:
        return None, None
```

3. **Calling verify-token endpoint:**
```python
response = requests.get(
    "http://auth-service:5001/api/auth/verify-token",
    headers={"Authorization": f"Bearer {token}"}
)
if response.status_code == 200:
    user = response.json()['user']
```

## Next Steps

1. ✅ Auth Service is running
2. Create Notification Service
3. Create API Gateway
4. Integrate with other services
5. Add to main docker-compose.yml

## Production Checklist

Before deploying to production:

- [ ] Change SECRET_KEY to a strong random value
- [ ] Use environment-specific configuration
- [ ] Integrate real SMS service for OTP
- [ ] Add rate limiting
- [ ] Enable HTTPS only
- [ ] Add logging and monitoring
- [ ] Use Redis for OTP storage
- [ ] Implement refresh tokens
- [ ] Add input validation and sanitization
- [ ] Set up database backups
