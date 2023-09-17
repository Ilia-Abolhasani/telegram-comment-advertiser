from flask import jsonify
from app.util.LoggerBot import LoggerBot
logger_bot = LoggerBot()


def register_error_handlers(app):
    app.register_error_handler(404, _access_denied_error)
    app.register_error_handler(404, _not_found_error)
    app.register_error_handler(500, _internal_error)
    app.register_error_handler(
        Exception, _handle_global_exception)


def _access_denied_error(error):
    return jsonify({"error": "Access denied."}), 403


def _not_found_error(error):
    return jsonify({"error": "Page not found."}), 404


def _internal_error(error):
    try:
        logger_bot.announce(error, "Internal server error:")
    except Exception as send_error:
        return jsonify("Internal server error."), 500
    return jsonify({"error": "Internal server error."}), 500


def _handle_global_exception(error):
    try:
        logger_bot.announce(error, "An error occurred:")
    except Exception as send_error:
        return jsonify("An error occurred, also for send."), 500
    return jsonify("An error occurred"), 500
