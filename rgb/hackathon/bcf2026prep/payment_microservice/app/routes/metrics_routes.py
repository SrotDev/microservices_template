from flask import Blueprint, Response
from app.services.metrics_service import get_metrics

metrics_bp = Blueprint('metrics', __name__)


@metrics_bp.route('', methods=['GET'])
@metrics_bp.route('/', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint."""
    metrics_data, content_type = get_metrics()
    return Response(metrics_data, mimetype=content_type)
