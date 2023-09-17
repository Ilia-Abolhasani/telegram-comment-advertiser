from flask import Flask
from app.cron.manager import start_jobs
from app.Context import Context
from app.middleware.request_handler import request_handler_middleware
from app.route import route_bp
from app.util.Telegram import Telegram
from app.util.LoggerBot import LoggerBot
from app.config.config import Config


# sys.excepthook = custom_excepthook

app = Flask(__name__)
app.register_blueprint(route_bp)
app.before_request(request_handler_middleware)

# Initialize
context = Context()
telegram_api = Telegram(
    Config.telegram_app_id,
    Config.telegram_app_hash,
    Config.telegram_phone,
    Config.database_encryption_key,
    Config.tdlib_directory
)
telegram_api.remove_all_proxies()
logger_api = LoggerBot()

start_jobs(context, telegram_api, logger_api)
