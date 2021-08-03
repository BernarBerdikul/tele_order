import io
import logging
import traceback
import requests

from tele_order.utils.constants import TELEGRAM_ERROR_CHAT_ID

api_url = 'https://api.telegram.org/'


class TelegramFormatter(logging.Formatter):
    """
    an extension of the usual logging.Formatter to simplify transmitted data
    """
    meta_attrs = ['REMOTE_ADDR',
                  'HOSTNAME',
                  'HTTP_REFERER']
    limit = -1  # default per logging.Formatter is None

    def format(self, record):
        """
        same as logging.Formatter.format, with added reporting of the
        meta_attrs when found in request.META, and the
        username that generated the Exception
        """
        s = super().format(record)

        s += "\n{attr}: {value}".format(
            attr='USER',
            value=record.request.user
        )
        for attr in self.meta_attrs:
            if attr in record.request.META:
                s += f"\n{attr}: {record.request.META[attr]}"
        return s

    def formatException(self, ei):
        """ same as logging.Formatter.formatException except for
        the limit passed as a variable """
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, self.limit, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s


class AdminTelegramHandler(logging.Handler):
    """
    An exception log handler that send a short log to a telegram bot.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        if 'bot_token' in kwargs:
            self.bot_token = kwargs['bot_token']

        self.bot_url = f"{api_url}bot{self.bot_token}/"
        self.setFormatter(TelegramFormatter())

    def emit(self, record):
        self.send_message(self.format(record))

    def prepare_json_for_answer(self, data):
        if TELEGRAM_ERROR_CHAT_ID is not None:
            json_data = {
                "chat_id": TELEGRAM_ERROR_CHAT_ID,
                "text": data,
                "parse_mode": 'HTML',
            }
            return json_data
        else:
            return {}

    def send_message(self, message):
        prepared_data = self.prepare_json_for_answer(message)
        message_url = f'{self.bot_url}sendMessage'
        requests.post(message_url, json=prepared_data)
