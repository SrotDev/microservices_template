from flask import Blueprint, jsonify, current_app
from app import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)


@health_bp.route('', methods=['GET'])
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': current_app.config.get('SERVICE_NAME', 'payment-service')
    }), 200


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """
    Readiness check - verifies all dependencies are available.
    Used by Kubernetes/load balancers.
    """
    checks = {
        'database': False,
        'rabbitmq': True  # Default to True if not enabled
    }
    
    # Check database connection
    try:
        db.session.execute(text('SELECT 1'))
        checks['database'] = True
    except Exception as e:
        checks['database'] = False
        checks['database_error'] = str(e)
    
    # Check RabbitMQ if enabled
    if current_app.config.get('RABBITMQ_ENABLED'):
        if hasattr(current_app, 'rabbitmq') and current_app.rabbitmq.connection:
            checks['rabbitmq'] = not current_app.rabbitmq.connection.is_closed
        else:
            checks['rabbitmq'] = False
    
    all_healthy = all([
        checks['database'],
        checks['rabbitmq']
    ])
    
    status_code = 200 if all_healthy else 503
    
    return jsonify({
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks
    }), status_code


@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """
    Liveness check - verifies the service is running.
    Used by Kubernetes to restart unhealthy pods.
    """
    return jsonify({
        'status': 'alive',
        'service': current_app.config.get('SERVICE_NAME', 'payment-service')
    }), 200
