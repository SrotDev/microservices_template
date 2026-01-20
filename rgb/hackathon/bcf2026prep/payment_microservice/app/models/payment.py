from datetime import datetime
from app import db
import uuid


class Payment(db.Model):
    """
    Payment model - simple and scalable.
    """
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(36), unique=True, nullable=False, index=True, 
                           default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    booking_id = db.Column(db.String(100), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending', index=True)
    # Status: pending, processing, completed, failed, refunded
    payment_method = db.Column(db.String(50), nullable=True)
    transaction_ref = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.payment_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'payment_id': self.payment_id,
            'user_id': self.user_id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'transaction_ref': self.transaction_ref,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
