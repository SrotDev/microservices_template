from flask import Blueprint, request, jsonify, current_app
from app.services.jwt_service import jwt_required, verified_user_required
from app.services.payment_service import PaymentService
from app.services.rabbitmq_service import PaymentEvents
from app.services.metrics_service import (
    track_request_metrics, 
    track_payment_created, 
    track_payment_processed, 
    track_payment_refunded
)

payment_bp = Blueprint('payments', __name__)


@payment_bp.route('', methods=['POST'])
@jwt_required
@track_request_metrics
def create_payment():
    """Create a new payment."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate required fields
    required_fields = ['booking_id', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount'}), 400
    
    payment = PaymentService.create_payment(
        user_id=request.current_user.id,
        booking_id=data['booking_id'],
        amount=amount,
        currency=data.get('currency', 'USD'),
        payment_method=data.get('payment_method')
    )
    
    # Track metrics
    track_payment_created(
        amount=amount,
        currency=data.get('currency', 'USD'),
        payment_method=data.get('payment_method')
    )
    
    # Publish event if RabbitMQ is enabled
    if hasattr(current_app, 'rabbitmq'):
        current_app.rabbitmq.publish_event(
            PaymentEvents.CREATED,
            payment.to_dict()
        )
    
    return jsonify({
        'message': 'Payment created successfully',
        'payment': payment.to_dict()
    }), 201


@payment_bp.route('/<payment_id>', methods=['GET'])
@jwt_required
@track_request_metrics
def get_payment(payment_id):
    """Get payment by ID."""
    payment = PaymentService.get_payment_by_id(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    # Check if user owns this payment
    if payment.user_id != request.current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({'payment': payment.to_dict()}), 200


@payment_bp.route('', methods=['GET'])
@jwt_required
@track_request_metrics
def get_user_payments():
    """Get all payments for current user."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Limit per_page to prevent abuse
    per_page = min(per_page, 100)
    
    pagination = PaymentService.get_payments_by_user(
        user_id=request.current_user.id,
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'payments': [p.to_dict() for p in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200


@payment_bp.route('/booking/<booking_id>', methods=['GET'])
@jwt_required
def get_booking_payments(booking_id):
    """Get all payments for a booking."""
    payments = PaymentService.get_payments_by_booking(booking_id)
    
    # Filter to only show user's own payments
    user_payments = [p for p in payments if p.user_id == request.current_user.id]
    
    return jsonify({
        'payments': [p.to_dict() for p in user_payments]
    }), 200


@payment_bp.route('/<payment_id>/process', methods=['POST'])
@jwt_required
@track_request_metrics
def process_payment(payment_id):
    """Process a pending payment."""
    payment = PaymentService.get_payment_by_id(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    if payment.user_id != request.current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    payment, error = PaymentService.process_payment(payment_id)
    
    if error:
        track_payment_processed(status='failed')
        return jsonify({'error': error}), 400
    
    # Track metrics
    track_payment_processed(status='completed')
    
    # Publish event if RabbitMQ is enabled
    if hasattr(current_app, 'rabbitmq'):
        current_app.rabbitmq.publish_event(
            PaymentEvents.COMPLETED,
            payment.to_dict()
        )
    
    return jsonify({
        'message': 'Payment processed successfully',
        'payment': payment.to_dict()
    }), 200


@payment_bp.route('/<payment_id>/refund', methods=['POST'])
@jwt_required
@track_request_metrics
def refund_payment(payment_id):
    """Refund a completed payment."""
    payment = PaymentService.get_payment_by_id(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    if payment.user_id != request.current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    payment, error = PaymentService.refund_payment(payment_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Track metrics
    track_payment_refunded()
    
    # Publish event if RabbitMQ is enabled
    if hasattr(current_app, 'rabbitmq'):
        current_app.rabbitmq.publish_event(
            PaymentEvents.REFUNDED,
            payment.to_dict()
        )
    
    return jsonify({
        'message': 'Payment refunded successfully',
        'payment': payment.to_dict()
    }), 200


@payment_bp.route('/<payment_id>/status', methods=['PATCH'])
@jwt_required
def update_payment_status(payment_id):
    """Update payment status (for webhook callbacks)."""
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': 'status is required'}), 400
    
    valid_statuses = ['pending', 'processing', 'completed', 'failed', 'refunded']
    if data['status'] not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
    
    payment = PaymentService.update_payment_status(
        payment_id=payment_id,
        status=data['status'],
        transaction_ref=data.get('transaction_ref')
    )
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    return jsonify({
        'message': 'Payment status updated',
        'payment': payment.to_dict()
    }), 200
