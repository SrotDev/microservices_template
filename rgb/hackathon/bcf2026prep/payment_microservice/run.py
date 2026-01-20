from app import create_app
from config import get_config

app = create_app()

if __name__ == '__main__':
    config = get_config()
    app.run(
        host='0.0.0.0',
        port=config.SERVICE_PORT,
        debug=config.DEBUG if hasattr(config, 'DEBUG') else True
    )
