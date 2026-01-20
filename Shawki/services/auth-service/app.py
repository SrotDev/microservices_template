from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/auth_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_EXPIRATION_HOURS'] = int(os.getenv('JWT_EXPIRATION_HOURS', 24))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# OTP Storage (Mock - in production use Redis with TTL)
otp_storage = {}

# JWT Token Generation
def generate_token(user_id, email):
    """Generate JWT token with user info"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['JWT_EXPIRATION_HOURS']),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# JWT Token Verification Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user_email = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user_id, current_user_email, *args, **kwargs)
    
    return decorated

# Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'auth-service'}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        name = data.get('name', '')
        phone = data.get('phone', '')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user
        new_user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            phone=phone
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token
        token = generate_token(new_user.id, new_user.email)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        token = generate_token(user.id, user.email)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/otp/request', methods=['POST'])
def request_otp():
    """Request OTP for verification (Mock implementation)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('phone'):
            return jsonify({'error': 'Phone number is required'}), 400
        
        phone = data['phone']
        
        # Generate mock OTP (in production, use random and send via SMS)
        otp = '123456'
        
        # Store OTP (in production, use Redis with TTL)
        otp_storage[phone] = {
            'otp': otp,
            'created_at': datetime.datetime.utcnow(),
            'expires_at': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }
        
        # In production, send OTP via SMS service
        # For hackathon, return OTP in response (ONLY FOR TESTING)
        return jsonify({
            'message': 'OTP sent successfully',
            'otp': otp,  # Remove this in production!
            'expires_in': 300  # 5 minutes
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/otp/verify', methods=['POST'])
def verify_otp():
    """Verify OTP"""
    try:
        data = request.get_json()
        
        if not data or not data.get('phone') or not data.get('otp'):
            return jsonify({'error': 'Phone and OTP are required'}), 400
        
        phone = data['phone']
        otp = data['otp']
        
        # Check if OTP exists
        if phone not in otp_storage:
            return jsonify({'error': 'OTP not found or expired'}), 404
        
        stored_otp_data = otp_storage[phone]
        
        # Check if OTP is expired
        if datetime.datetime.utcnow() > stored_otp_data['expires_at']:
            del otp_storage[phone]
            return jsonify({'error': 'OTP has expired'}), 400
        
        # Verify OTP
        if stored_otp_data['otp'] != otp:
            return jsonify({'error': 'Invalid OTP'}), 400
        
        # OTP verified, remove from storage
        del otp_storage[phone]
        
        return jsonify({
            'message': 'OTP verified successfully',
            'verified': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify-token', methods=['GET'])
@token_required
def verify_token(current_user_id, current_user_email):
    """Verify JWT token and return user info (for other services)"""
    try:
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user_id, current_user_email):
    """Get current user info from token"""
    try:
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Database initialization
@app.before_first_request
def create_tables():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
