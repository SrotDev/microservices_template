"""
JWT Helper for Other Services

This file can be copied to other microservices to decode and verify JWT tokens
without making HTTP calls to the auth service.

Usage in other services:
    from jwt_helper import decode_token, get_user_from_request
    
    # Option 1: Decode token directly
    user_id, email = decode_token(token)
    
    # Option 2: Get user from Flask request
    user_id, email = get_user_from_request(request)
"""

import jwt
import os
from functools import wraps
from flask import request, jsonify

# IMPORTANT: This SECRET_KEY must match the auth service SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'hackathon-secret-key-2024')

def decode_token(token):
    """
    Decode JWT token and return user info
    
    Args:
        token (str): JWT token string
        
    Returns:
        tuple: (user_id, email) if valid, (None, None) if invalid
    """
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id'), payload.get('email')
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None, None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None, None
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None, None

def get_user_from_request(request_obj):
    """
    Extract and decode JWT token from Flask request
    
    Args:
        request_obj: Flask request object
        
    Returns:
        tuple: (user_id, email) if valid, (None, None) if invalid
    """
    token = request_obj.headers.get('Authorization', '')
    if not token:
        return None, None
    
    return decode_token(token)

def token_required(f):
    """
    Decorator to protect routes that require authentication
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(user_id, email):
            return jsonify({'message': f'Hello {email}'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id, email = decode_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return f(user_id, email, *args, **kwargs)
    
    return decorated

# Example usage in other services:
"""
from flask import Flask, request, jsonify
from jwt_helper import token_required, get_user_from_request

app = Flask(__name__)

# Method 1: Using decorator
@app.route('/api/bookings/my-bookings')
@token_required
def get_my_bookings(user_id, email):
    # user_id and email are automatically extracted from token
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify({'bookings': [b.to_dict() for b in bookings]})

# Method 2: Manual extraction
@app.route('/api/bookings/create')
def create_booking():
    user_id, email = get_user_from_request(request)
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Create booking for user_id
    booking = Booking(user_id=user_id, ...)
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'booking': booking.to_dict()})
"""
