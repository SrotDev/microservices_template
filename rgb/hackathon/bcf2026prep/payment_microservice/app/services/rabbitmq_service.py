import json
import pika
from pika.exceptions import AMQPConnectionError
import logging

logger = logging.getLogger(__name__)


class RabbitMQService:
    """
    RabbitMQ service for event-driven architecture.
    Enables horizontal scaling and async communication.
    """
    
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.channel = None
        self._connect()
    
    def _connect(self):
        """Establish connection to RabbitMQ."""
        try:
            credentials = pika.PlainCredentials(
                self.config['RABBITMQ_USER'],
                self.config['RABBITMQ_PASSWORD']
            )
            parameters = pika.ConnectionParameters(
                host=self.config['RABBITMQ_HOST'],
                port=self.config['RABBITMQ_PORT'],
                virtual_host=self.config['RABBITMQ_VHOST'],
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchange
            self.channel.exchange_declare(
                exchange=self.config['RABBITMQ_EXCHANGE'],
                exchange_type='topic',
                durable=True
            )
            
            # Declare queue
            self.channel.queue_declare(
                queue=self.config['RABBITMQ_QUEUE'],
                durable=True
            )
            
            # Bind queue to exchange
            self.channel.queue_bind(
                exchange=self.config['RABBITMQ_EXCHANGE'],
                queue=self.config['RABBITMQ_QUEUE'],
                routing_key='payment.*'
            )
            
            logger.info("Connected to RabbitMQ successfully")
        except AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None
    
    def _ensure_connection(self):
        """Ensure connection is alive, reconnect if needed."""
        if not self.connection or self.connection.is_closed:
            self._connect()
    
    def publish_event(self, event_type, data):
        """
        Publish payment event to RabbitMQ.
        
        Args:
            event_type: Event type (e.g., 'payment.created', 'payment.completed')
            data: Event data dictionary
        """
        if not self.config.get('RABBITMQ_ENABLED'):
            logger.debug("RabbitMQ disabled, skipping event publish")
            return False
        
        try:
            self._ensure_connection()
            
            if not self.channel:
                logger.error("No RabbitMQ channel available")
                return False
            
            message = json.dumps({
                'event_type': event_type,
                'data': data
            })
            
            self.channel.basic_publish(
                exchange=self.config['RABBITMQ_EXCHANGE'],
                routing_key=event_type,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistent message
                    content_type='application/json'
                )
            )
            
            logger.info(f"Published event: {event_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            return False
    
    def close(self):
        """Close RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")


# Event types constants
class PaymentEvents:
    CREATED = 'payment.created'
    PROCESSING = 'payment.processing'
    COMPLETED = 'payment.completed'
    FAILED = 'payment.failed'
    REFUNDED = 'payment.refunded'
