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
telegram_api = Telegram(
    Config.telegram_app_id,
    Config.telegram_app_hash,
    Config.telegram_phone,
    Config.database_encryption_key,
    Config.tdlib_directory
)
telegram_api.remove_all_proxies()
mess, id = telegram_api.channel_history(-1001923615081, 10, None)
telegram_api.send_message("سرعتشون عالیه", -1001923615081, 0, 191889408)
logger_api = LoggerBot()

context = Context()
start_jobs(context, telegram_api, logger_api)
