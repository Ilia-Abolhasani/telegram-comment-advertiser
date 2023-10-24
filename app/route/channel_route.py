import json
from flask import Blueprint, jsonify, request
from app.controller.message_controller import LogController

blueprint = Blueprint('channel', __name__)
controller = LogController()


@blueprint.route('/recive', methods=['POST'])
def post_log(agent_id):
    data = request.data
    decoded_data = data.decode('utf-8')
    json_object = json.loads(decoded_data)
    message = json_object['message']
    result = controller.send_log(agent_id, message)
    return jsonify({"message_id": result.message_id}), 200
