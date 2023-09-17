from app.route.channel_route import blueprint as channel_bp
from app.route.message_route import blueprint as message_bp
from app.route.history_route import blueprint as history_bp
from flask import Blueprint, jsonify

route_bp = Blueprint('route', __name__)

route_bp.register_blueprint(channel_bp, url_prefix='/api/channel')
route_bp.register_blueprint(message_bp, url_prefix='/api/message')
route_bp.register_blueprint(history_bp, url_prefix='/api/history')


@route_bp.route('/api/test', methods=['GET'])
def test_route():
    return jsonify(message="successful"), 200
