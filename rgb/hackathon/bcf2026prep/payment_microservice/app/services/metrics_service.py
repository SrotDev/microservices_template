from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
from functools import wraps
from flask import request

# Request metrics
REQUEST_COUNT = Counter(
    'payment_service_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'payment_service_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Business metrics
PAYMENTS_CREATED = Counter(
    'payment_service_payments_created_total',
    'Total number of payments created',
    ['currency', 'payment_method']
)

PAYMENTS_PROCESSED = Counter(
    'payment_service_payments_processed_total',
    'Total number of payments processed',
    ['status']  # completed, failed
)

PAYMENTS_REFUNDED = Counter(
    'payment_service_payments_refunded_total',
    'Total number of payments refunded'
)

PAYMENT_AMOUNT = Histogram(
    'payment_service_payment_amount',
    'Payment amounts',
    ['currency'],
    buckets=[10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]
)

ACTIVE_REQUESTS = Gauge(
    'payment_service_active_requests',
    'Number of active requests'
)

DB_CONNECTIONS = Gauge(
    'payment_service_db_connections',
    'Number of database connections'
)


def track_request_metrics(f):
    """Decorator to track request metrics."""
    @wraps(f)
    def decorated(*args, **kwargs):
        ACTIVE_REQUESTS.inc()
        start_time = time.time()
        
        try:
            response = f(*args, **kwargs)
            status_code = response[1] if isinstance(response, tuple) else 200
            return response
        except Exception as e:
            status_code = 500
            raise
        finally:
            latency = time.time() - start_time
            endpoint = request.endpoint or 'unknown'
            
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status_code=status_code
            ).inc()
            
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=endpoint
            ).observe(latency)
            
            ACTIVE_REQUESTS.dec()
    
    return decorated


def track_payment_created(amount, currency='USD', payment_method='unknown'):
    """Track payment creation metric."""
    PAYMENTS_CREATED.labels(
        currency=currency,
        payment_method=payment_method or 'unknown'
    ).inc()
    PAYMENT_AMOUNT.labels(currency=currency).observe(amount)


def track_payment_processed(status='completed'):
    """Track payment processing metric."""
    PAYMENTS_PROCESSED.labels(status=status).inc()


def track_payment_refunded():
    """Track payment refund metric."""
    PAYMENTS_REFUNDED.inc()


def get_metrics():
    """Generate Prometheus metrics output."""
    return generate_latest(), CONTENT_TYPE_LATEST
