from app import db
from app.models.payment import Payment
import uuid


class PaymentService:
    """Service to handle payment operations."""
    
    @staticmethod
    def create_payment(user_id, booking_id, amount, currency='USD', payment_method=None):
        """Create a new payment."""
        payment = Payment(
            payment_id=str(uuid.uuid4()),
            user_id=user_id,
            booking_id=booking_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            status='pending'
        )
        db.session.add(payment)
        db.session.commit()
        return payment
    
    @staticmethod
    def get_payment_by_id(payment_id):
        """Get payment by payment_id."""
        return Payment.query.filter_by(payment_id=payment_id).first()
    
    @staticmethod
    def get_payments_by_user(user_id, page=1, per_page=20):
        """Get paginated payments for a user."""
        return Payment.query.filter_by(user_id=user_id)\
            .order_by(Payment.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_payments_by_booking(booking_id):
        """Get all payments for a booking."""
        return Payment.query.filter_by(booking_id=booking_id).all()
    
    @staticmethod
    def process_payment(payment_id):
        """
        Mock payment processing.
        In production, integrate with payment gateway.
        """
        payment = PaymentService.get_payment_by_id(payment_id)
        if not payment:
            return None, 'Payment not found'
        
        if payment.status != 'pending':
            return None, f'Payment already {payment.status}'
        
        # Mock processing - in production, call payment gateway
        payment.status = 'processing'
        db.session.commit()
        
        # Simulate successful payment
        payment.status = 'completed'
        payment.transaction_ref = f'TXN-{uuid.uuid4().hex[:12].upper()}'
        db.session.commit()
        
        return payment, None
    
    @staticmethod
    def update_payment_status(payment_id, status, transaction_ref=None):
        """Update payment status."""
        payment = PaymentService.get_payment_by_id(payment_id)
        if not payment:
            return None
        
        payment.status = status
        if transaction_ref:
            payment.transaction_ref = transaction_ref
        db.session.commit()
        return payment
    
    @staticmethod
    def refund_payment(payment_id):
        """Refund a completed payment."""
        payment = PaymentService.get_payment_by_id(payment_id)
        if not payment:
            return None, 'Payment not found'
        
        if payment.status != 'completed':
            return None, 'Only completed payments can be refunded'
        
        # Mock refund - in production, call payment gateway
        payment.status = 'refunded'
        db.session.commit()
        
        return payment, None
