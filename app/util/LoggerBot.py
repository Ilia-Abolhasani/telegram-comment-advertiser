import os
import traceback
from pytgbot import Bot
import logging
from app.config.config import Config
logging.basicConfig(level=logging.DEBUG)


class LoggerBot:
    def __init__(self):
        self.bot = Bot(Config.loggger_bot_api_key)
        self.chat = Config.loggger_bot_chat_id

    def send(self, text):
        result = self.bot.send_message(self.chat, text)
        return result

    def announce(self, error, extra_message=None):
        traceback_str = traceback.format_exc()
        error_message = str(error)
        if extra_message:
            error_message = extra_message + " " + error_message
        message = f"{error_message}\n\n{traceback_str}"
        print(message)
        self.send(message)
