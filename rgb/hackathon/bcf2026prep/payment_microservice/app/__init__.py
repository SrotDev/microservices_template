from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config

db = SQLAlchemy()


def create_app(config_class=None):
    """Application factory pattern for scalability."""
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes.payment_routes import payment_bp
    from app.routes.health_routes import health_bp
    from app.routes.metrics_routes import metrics_bp
    
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(metrics_bp, url_prefix='/metrics')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Initialize RabbitMQ if enabled
    if app.config.get('RABBITMQ_ENABLED'):
        from app.services.rabbitmq_service import RabbitMQService
        app.rabbitmq = RabbitMQService(app.config)
    
    return app
