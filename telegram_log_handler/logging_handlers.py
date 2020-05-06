from logging import StreamHandler

from telegram.error import NetworkError
from telegram.ext import Updater


class TelegramLog:
    def __init__(self, bot_token: str, chat_ids: dict, project_name: str, use_proxy: bool, request_kwargs: dict = None):
        updater = Updater(
            token=bot_token,
            request_kwargs=request_kwargs if use_proxy else None
        )

        self.bot = updater.bot
        self.chat_ids = list(chat_ids.values())
        self.project_name = project_name

    def send(self, data):
        for _id in self.chat_ids:
            try:
                self.bot.send_message(chat_id=_id, text=f"#{self.project_name}:\n{data}")
            except NetworkError as e:
                pass


class TelegramHandler(StreamHandler):
    def __init__(self, bot_token: str, chat_ids: dict, project_name: str,
                 use_proxy: bool = False, request_kwargs: dict = None):

        StreamHandler.__init__(self)
        self.telegram_broker = TelegramLog(bot_token, chat_ids, project_name, use_proxy, request_kwargs)

    def emit(self, record):
        msg = self.format(record)
        self.telegram_broker.send(msg)
