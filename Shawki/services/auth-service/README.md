# Auth Service

Authentication microservice for the Train Ticketing System.

## Features

- User registration with password hashing (bcrypt)
- User login with JWT token generation
- OTP request and verification (mock implementation)
- Token verification for other services
- Protected routes with JWT middleware

## Tech Stack

- Flask 2.3.3
- PostgreSQL (via SQLAlchemy)
- JWT for authentication
- Bcrypt for password hashing
- Docker for containerization

## API Endpoints

### Public Endpoints

#### Health Check
```
GET /health
Response: { "status": "healthy", "service": "auth-service" }
```

#### Register User
```
POST /api/auth/register
Body: {
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "phone": "01712345678"
}
Response: {
  "message": "User registered successfully",
  "token": "jwt_token_here",
  "user": { ... }
}
```

#### Login
```
POST /api/auth/login
Body: {
  "email": "user@example.com",
  "password": "password123"
}
Response: {
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": { ... }
}
```

#### Request OTP
```
POST /api/auth/otp/request
Body: {
  "phone": "01712345678"
}
Response: {
  "message": "OTP sent successfully",
  "otp": "123456",  // Only for testing!
  "expires_in": 300
}
```

#### Verify OTP
```
POST /api/auth/otp/verify
Body: {
  "phone": "01712345678",
  "otp": "123456"
}
Response: {
  "message": "OTP verified successfully",
  "verified": true
}
```

### Protected Endpoints (Require JWT Token)

#### Verify Token
```
GET /api/auth/verify-token
Headers: { "Authorization": "Bearer jwt_token_here" }
Response: {
  "valid": true,
  "user": { ... }
}
```

#### Get Current User
```
GET /api/auth/me
Headers: { "Authorization": "Bearer jwt_token_here" }
Response: {
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "01712345678",
    "created_at": "2024-01-20T10:30:00"
  }
}
```

## JWT Token Structure

The JWT token contains:
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "exp": 1705843200,  // Expiration timestamp
  "iat": 1705756800   // Issued at timestamp
}
```

## Using JWT in Other Services

Other services can verify the JWT token by:

1. **Option 1: Call the verify-token endpoint**
```python
import requests

def verify_user_token(token):
    response = requests.get(
        'http://auth-service:5001/api/auth/verify-token',
        headers={'Authorization': f'Bearer {token}'}
    )
    if response.status_code == 200:
        return response.json()['user']
    return None
```

2. **Option 2: Decode JWT directly (recommended for performance)**
```python
import jwt

SECRET_KEY = 'your-secret-key'  # Same as auth service

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload  # Contains user_id and email
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

## Environment Variables

Create a `.env` file:
```
DATABASE_URL=postgresql://postgres:password@postgres:5432/auth_db
SECRET_KEY=your-super-secret-key-change-this
JWT_EXPIRATION_HOURS=24
PORT=5001
```

## Running Locally

### Without Docker
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://postgres:password@localhost:5432/auth_db
export SECRET_KEY=your-secret-key

# Run the application
python app.py
```

### With Docker
```bash
# Build image
docker build -t auth-service .

# Run container
docker run -p 5001:5001 \
  -e DATABASE_URL=postgresql://postgres:password@postgres:5432/auth_db \
  -e SECRET_KEY=your-secret-key \
  auth-service
```

## Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest test_auth.py -v
```

## Database Schema

### Users Table
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

## Security Notes

1. **Password Hashing**: Uses bcrypt with automatic salt generation
2. **JWT Secret**: Change SECRET_KEY in production
3. **Token Expiration**: Default 24 hours, configurable
4. **OTP**: Mock implementation - integrate real SMS service in production
5. **CORS**: Enabled for all origins - restrict in production

## Production Considerations

1. Use Redis for OTP storage with TTL
2. Integrate real SMS service for OTP
3. Use environment-specific secret keys
4. Enable HTTPS only
5. Add rate limiting
6. Implement refresh tokens
7. Add logging and monitoring
8. Use connection pooling for database

## Integration with Other Services

Other services should:
1. Include JWT token in Authorization header: `Bearer <token>`
2. Decode token to get user_id and email
3. Use user_id for database queries
4. Call /api/auth/verify-token for full user details if needed

Example from Booking Service:
```python
from flask import request
import jwt

def get_current_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id'], payload['email']
    except:
        return None, None
```
