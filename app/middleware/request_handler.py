import hashlib
from flask import abort, request, jsonify
from datetime import datetime, timezone
from app.config.config import Config


def request_handler_middleware():
    # Exclude the test_route from middleware
    if request.path == '/favicon.ico':
        return None
    if request.endpoint == "route.test_route":
        return None

    # check for hash
    request_time = request.headers.get('X-Request-Time')
    hashed_timestamp = request.headers.get('X-Hashed-Timestamp')

    # Check if request_time and hashed_timestamp are present in the headers
    if not request_time or not hashed_timestamp:
        response = jsonify({"error": "Missing required headers."})
        response.status_code = 400
        return response

    # Calculate the hash of the received time
    message = f'{request_time}{Config.encrypted_key}'
    calculated_hash = hashlib.sha256(message.encode()).hexdigest()

    # Check if the calculated hash matches the received hashed_timestamp
    if calculated_hash != hashed_timestamp:
        response = jsonify({"error": "Hash mismatch."})
        response.status_code = 400
        return response

    # Convert the received time string to a datetime object
    received_time = datetime.strptime(request_time, '%Y-%m-%d %H:%M:%S')
    received_time = received_time.replace(tzinfo=timezone.utc)
    # Calculate the time difference
    current_time = datetime.now(timezone.utc)
    time_difference = current_time - received_time
    # Check if the time difference is less than 1 minute (60 seconds)
    if time_difference.total_seconds() > 60:
        response = jsonify({"error": "Request time exceeds 1 minute."})
        response.status_code = 400
        return response

    return None
