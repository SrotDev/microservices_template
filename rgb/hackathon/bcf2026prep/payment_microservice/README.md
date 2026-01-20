# Payment Microservice

A scalable Flask-based payment microservice for a ticket booking system.

## Features

- **JWT Authentication**: Verifies tokens from auth microservice
- **Simple Models**: User cache and Payment models using SQLAlchemy
- **Database Flexibility**: SQLite for development, PostgreSQL for production
- **Message Queue**: RabbitMQ support for event-driven architecture
- **Health Checks**: Kubernetes-ready liveness and readiness probes
- **Scalable Design**: Stateless architecture for horizontal scaling

## Quick Start

### Development Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py
```

### Docker Deployment

```bash
# Run with Docker Compose (includes PostgreSQL & RabbitMQ)
docker-compose up -d

# Scale horizontally
docker-compose up -d --scale payment-service=4
```

## API Endpoints

### Health Checks
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check (database, RabbitMQ)
- `GET /health/live` - Liveness check

### Payments (Require JWT)
- `POST /api/payments` - Create payment
- `GET /api/payments` - Get user's payments (paginated)
- `GET /api/payments/<payment_id>` - Get payment by ID
- `GET /api/payments/booking/<booking_id>` - Get payments for booking
- `POST /api/payments/<payment_id>/process` - Process payment
- `POST /api/payments/<payment_id>/refund` - Refund payment
- `PATCH /api/payments/<payment_id>/status` - Update payment status

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | development |
| `SECRET_KEY` | Flask secret key | dev-secret-key |
| `JWT_SECRET_KEY` | JWT signing key (must match auth service) | jwt-secret-key |
| `DATABASE_URL` | Database connection string | sqlite:///payments.db |
| `RABBITMQ_ENABLED` | Enable RabbitMQ | False |
| `RABBITMQ_HOST` | RabbitMQ host | localhost |
| `SERVICE_PORT` | Service port | 5001 |

## JWT Token Format

The service expects JWT tokens with the following payload:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "is_verified": true,
  "exp": 1234567890
}
```

## Scaling Considerations

1. **Horizontal Scaling**: Stateless design allows multiple instances
2. **Database**: Use PostgreSQL connection pooling in production
3. **Message Queue**: RabbitMQ for async event processing
4. **Load Balancer**: Use nginx or cloud load balancer
5. **Caching**: Add Redis for session/response caching if needed

## Production Deployment

```bash
# Using Gunicorn
gunicorn --bind 0.0.0.0:5001 --workers 4 --threads 2 wsgi:app
```
