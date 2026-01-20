"""WSGI entry point for production deployment with Gunicorn."""
from app import create_app
from config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run()
