import jwt
from flask import current_app
from functools import wraps
from flask import request, jsonify
from app.models.user import User
from app import db


class JWTService:
    """Service to handle JWT token verification."""
    
    @staticmethod
    def decode_token(token):
        """
        Decode and verify JWT token.
        Returns decoded payload or None if invalid.
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def extract_token_from_header():
        """Extract JWT token from Authorization header."""
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        return None
    
    @staticmethod
    def get_user_from_token(payload):
        """
        Get or create user from token payload.
        Stores user info in database from auth microservice.
        """
        auth_user_id = payload.get('sub') or payload.get('user_id')
        if not auth_user_id:
            return None
        
        email = payload.get('email')
        is_verified = payload.get('is_verified', False) or payload.get('verified', False)
        
        user = User.get_or_create(
            auth_user_id=str(auth_user_id),
            email=email,
            is_verified=is_verified
        )
        return user


def jwt_required(f):
    """Decorator to require valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = JWTService.extract_token_from_header()
        
        if not token:
            return jsonify({
                'error': 'Authorization token is missing',
                'code': 'TOKEN_MISSING'
            }), 401
        
        payload = JWTService.decode_token(token)
        
        if not payload:
            return jsonify({
                'error': 'Invalid or expired token',
                'code': 'TOKEN_INVALID'
            }), 401
        
        user = JWTService.get_user_from_token(payload)
        
        if not user:
            return jsonify({
                'error': 'User not found in token',
                'code': 'USER_NOT_FOUND'
            }), 401
        
        # Attach user and payload to request context
        request.current_user = user
        request.token_payload = payload
        
        return f(*args, **kwargs)
    
    return decorated


def verified_user_required(f):
    """Decorator to require verified user."""
    @wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        if not request.current_user.is_verified:
            return jsonify({
                'error': 'User not verified',
                'code': 'USER_NOT_VERIFIED'
            }), 403
        return f(*args, **kwargs)
    
    return decorated
