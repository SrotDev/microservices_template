from datetime import datetime
from app import db


class User(db.Model):
    """
    User model - stores user info from JWT token.
    This is a cache of user data from auth microservice.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    auth_user_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with payments
    payments = db.relationship('Payment', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.auth_user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'auth_user_id': self.auth_user_id,
            'email': self.email,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def get_or_create(cls, auth_user_id, email=None, is_verified=False):
        """Get existing user or create new one from JWT data."""
        user = cls.query.filter_by(auth_user_id=auth_user_id).first()
        if not user:
            user = cls(
                auth_user_id=auth_user_id,
                email=email,
                is_verified=is_verified
            )
            db.session.add(user)
            db.session.commit()
        else:
            # Update user info if changed
            if email and user.email != email:
                user.email = email
            if user.is_verified != is_verified:
                user.is_verified = is_verified
            db.session.commit()
        return user
