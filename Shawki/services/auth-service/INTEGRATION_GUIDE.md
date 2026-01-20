# Auth Service Integration Guide

## For Other Team Members (Person 2 & Person 3)

This guide explains how to integrate the Auth Service with your microservices.

---

## Quick Integration Steps

### Step 1: Copy JWT Helper

Copy `jwt_helper.py` to your service directory:

```bash
cp services/auth-service/jwt_helper.py services/your-service/
```

### Step 2: Install PyJWT

Add to your `requirements.txt`:
```
PyJWT==2.8.0
```

### Step 3: Set SECRET_KEY

In your service, use the **same SECRET_KEY** as auth service:
```python
# In your app.py or config
SECRET_KEY = 'hackathon-secret-key-2024'
```

### Step 4: Use in Your Routes

```python
from flask import Flask, request, jsonify
from jwt_helper import token_required, get_user_from_request

app = Flask(__name__)

# Method 1: Using decorator (recommended)
@app.route('/api/bookings/my-bookings')
@token_required
def get_my_bookings(user_id, email):
    # user_id and email are automatically available
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify({'bookings': [b.to_dict() for b in bookings]})

# Method 2: Manual extraction
@app.route('/api/bookings/create', methods=['POST'])
def create_booking():
    user_id, email = get_user_from_request(request)
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    booking = Booking(
        user_id=user_id,
        seat_id=data['seat_id'],
        ...
    )
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'booking': booking.to_dict()})
```

---

## Frontend Integration

### Registration Flow

```javascript
// Register new user
const response = await fetch('http://localhost:5001/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123',
    name: 'John Doe',
    phone: '01712345678'
  })
});

const data = await response.json();
const token = data.token;

// Store token in localStorage
localStorage.setItem('token', token);
localStorage.setItem('user', JSON.stringify(data.user));
```

### Login Flow

```javascript
// Login existing user
const response = await fetch('http://localhost:5001/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const data = await response.json();
localStorage.setItem('token', data.token);
localStorage.setItem('user', JSON.stringify(data.user));
```

### Making Authenticated Requests

```javascript
// Get token from localStorage
const token = localStorage.getItem('token');

// Make authenticated request
const response = await fetch('http://localhost:5002/api/trains/search', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

const trains = await response.json();
```

### OTP Flow

```javascript
// Step 1: Request OTP
const otpResponse = await fetch('http://localhost:5001/api/auth/otp/request', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ phone: '01712345678' })
});

const otpData = await otpResponse.json();
console.log('OTP:', otpData.otp); // For testing only!

// Step 2: Verify OTP
const verifyResponse = await fetch('http://localhost:5001/api/auth/otp/verify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: '01712345678',
    otp: '123456'
  })
});

const verifyData = await verifyResponse.json();
if (verifyData.verified) {
  console.log('OTP verified successfully!');
}
```

---

## API Gateway Integration

When setting up nginx as API Gateway, add this route:

```nginx
# nginx.conf

upstream auth_service {
    server auth-service:5001;
}

server {
    listen 80;
    
    # Auth routes
    location /api/auth/ {
        proxy_pass http://auth_service/api/auth/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # Other service routes...
}
```

---

## Database Schema Reference

The auth service creates this user table:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Using User ID in Other Services

When creating bookings, payments, etc., use the `user_id` from the JWT token:

```python
# In Booking Service
@app.route('/api/bookings/create', methods=['POST'])
@token_required
def create_booking(user_id, email):
    data = request.get_json()
    
    booking = Booking(
        user_id=user_id,  # From JWT token
        seat_id=data['seat_id'],
        status='pending'
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'booking': booking.to_dict()})
```

---

## JWT Token Structure

The JWT token contains:

```json
{
  "user_id": 1,
  "email": "user@example.com",
  "exp": 1705843200,
  "iat": 1705756800
}
```

You can decode it to get:
- `user_id`: Use this for database queries
- `email`: Use this for display/logging
- `exp`: Token expiration timestamp
- `iat`: Token issued at timestamp

---

## Common Patterns

### Pattern 1: Protect All Routes

```python
from jwt_helper import token_required

@app.route('/api/bookings/<int:booking_id>')
@token_required
def get_booking(user_id, email, booking_id):
    booking = Booking.query.get(booking_id)
    
    # Ensure user owns this booking
    if booking.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({'booking': booking.to_dict()})
```

### Pattern 2: Optional Authentication

```python
from jwt_helper import get_user_from_request

@app.route('/api/trains/search')
def search_trains():
    # Get user if authenticated (optional)
    user_id, email = get_user_from_request(request)
    
    # Search trains (works for both authenticated and anonymous users)
    trains = Train.query.filter_by(...).all()
    
    # If authenticated, can show personalized results
    if user_id:
        # Add user-specific data
        pass
    
    return jsonify({'trains': [t.to_dict() for t in trains]})
```

### Pattern 3: Admin Routes

```python
ADMIN_EMAILS = ['admin@railway.gov.bd']

@app.route('/api/admin/users')
@token_required
def list_users(user_id, email):
    # Check if user is admin
    if email not in ADMIN_EMAILS:
        return jsonify({'error': 'Admin access required'}), 403
    
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]})
```

---

## Testing Your Integration

### Test with curl

```bash
# 1. Get token
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.token')

# 2. Use token in your service
curl -X GET http://localhost:5002/api/your-endpoint \
  -H "Authorization: Bearer $TOKEN"
```

### Test with Python

```python
import requests

# Get token
response = requests.post('http://localhost:5001/api/auth/login', json={
    'email': 'test@example.com',
    'password': 'password123'
})
token = response.json()['token']

# Use token
response = requests.get('http://localhost:5002/api/your-endpoint',
    headers={'Authorization': f'Bearer {token}'})
print(response.json())
```

---

## Troubleshooting

### "Invalid token" error

**Cause**: SECRET_KEY mismatch between services

**Solution**: Ensure all services use the same SECRET_KEY:
```python
SECRET_KEY = 'hackathon-secret-key-2024'
```

### "Token has expired" error

**Cause**: Token is older than 24 hours

**Solution**: User needs to login again to get a new token

### "Token is missing" error

**Cause**: Authorization header not sent

**Solution**: Ensure frontend sends header:
```javascript
headers: {
  'Authorization': `Bearer ${token}`
}
```

### CORS errors in frontend

**Cause**: Auth service CORS not configured

**Solution**: Already configured in auth service with `Flask-CORS`

---

## Environment Variables

All services should have these environment variables:

```bash
# .env file
SECRET_KEY=hackathon-secret-key-2024
DATABASE_URL=postgresql://postgres:password@postgres:5432/your_db
```

---

## Docker Compose Integration

When adding to main docker-compose.yml:

```yaml
services:
  auth-service:
    build: ./services/auth-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/auth_db
      SECRET_KEY: hackathon-secret-key-2024
      JWT_EXPIRATION_HOURS: 24
    ports:
      - "5001:5001"
    depends_on:
      - postgres

  your-service:
    build: ./services/your-service
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/your_db
      SECRET_KEY: hackathon-secret-key-2024  # SAME SECRET KEY!
    ports:
      - "5002:5002"
    depends_on:
      - postgres
      - auth-service  # Ensure auth service starts first
```

---

## Quick Reference

### Get User ID from Token
```python
from jwt_helper import get_user_from_request

user_id, email = get_user_from_request(request)
```

### Protect Route
```python
from jwt_helper import token_required

@app.route('/protected')
@token_required
def protected_route(user_id, email):
    return jsonify({'message': f'Hello {email}'})
```

### Frontend: Store Token
```javascript
localStorage.setItem('token', token);
```

### Frontend: Send Token
```javascript
headers: { 'Authorization': `Bearer ${token}` }
```

---

## Need Help?

- Check `services/auth-service/README.md` for detailed API docs
- Check `services/auth-service/QUICKSTART.md` for setup instructions
- Check `services/auth-service/test_auth.py` for example usage
- Run `services/auth-service/test_api.sh` to test all endpoints

---

## Summary for Team

✅ **Person 1 (You)**: Auth service is ready!

📋 **Person 2**: Copy `jwt_helper.py` to your services and use `@token_required` decorator

🎨 **Person 3**: Use the frontend integration code above for login/register

🔑 **Everyone**: Use the same `SECRET_KEY` in all services!
