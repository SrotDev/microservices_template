import pytest
import json
from app import app, db, User

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/auth/register', 
        json={
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User',
            'phone': '01712345678'
        })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user']['email'] == 'test@example.com'

def test_register_duplicate_user(client):
    """Test registering duplicate user"""
    # Register first user
    client.post('/api/auth/register', 
        json={
            'email': 'test@example.com',
            'password': 'password123'
        })
    
    # Try to register same email
    response = client.post('/api/auth/register', 
        json={
            'email': 'test@example.com',
            'password': 'password456'
        })
    
    assert response.status_code == 409

def test_login_success(client):
    """Test successful login"""
    # Register user
    client.post('/api/auth/register', 
        json={
            'email': 'test@example.com',
            'password': 'password123'
        })
    
    # Login
    response = client.post('/api/auth/login', 
        json={
            'email': 'test@example.com',
            'password': 'password123'
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['message'] == 'Login successful'

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', 
        json={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
    
    assert response.status_code == 401

def test_otp_request(client):
    """Test OTP request"""
    response = client.post('/api/auth/otp/request', 
        json={
            'phone': '01712345678'
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'otp' in data
    assert data['otp'] == '123456'

def test_otp_verify_success(client):
    """Test OTP verification success"""
    # Request OTP
    client.post('/api/auth/otp/request', 
        json={
            'phone': '01712345678'
        })
    
    # Verify OTP
    response = client.post('/api/auth/otp/verify', 
        json={
            'phone': '01712345678',
            'otp': '123456'
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['verified'] == True

def test_otp_verify_invalid(client):
    """Test OTP verification with invalid OTP"""
    # Request OTP
    client.post('/api/auth/otp/request', 
        json={
            'phone': '01712345678'
        })
    
    # Verify with wrong OTP
    response = client.post('/api/auth/otp/verify', 
        json={
            'phone': '01712345678',
            'otp': '000000'
        })
    
    assert response.status_code == 400

def test_verify_token(client):
    """Test token verification"""
    # Register and get token
    register_response = client.post('/api/auth/register', 
        json={
            'email': 'test@example.com',
            'password': 'password123'
        })
    
    token = json.loads(register_response.data)['token']
    
    # Verify token
    response = client.get('/api/auth/verify-token',
        headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['valid'] == True

def test_get_current_user(client):
    """Test getting current user info"""
    # Register and get token
    register_response = client.post('/api/auth/register', 
        json={
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        })
    
    token = json.loads(register_response.data)['token']
    
    # Get current user
    response = client.get('/api/auth/me',
        headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user']['email'] == 'test@example.com'
    assert data['user']['name'] == 'Test User'

def test_missing_token(client):
    """Test accessing protected route without token"""
    response = client.get('/api/auth/me')
    assert response.status_code == 401

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
