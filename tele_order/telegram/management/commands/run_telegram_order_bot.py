import logging
import telebot
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from tele_order.core.models import (User, Order, Restaurant, Promotion)
from dotenv import load_dotenv
from tele_order.telegram.service import check_it_is_bot, create_new_user
from tele_order.utils import constants

load_dotenv()

BASE_DIR = settings.BASE_DIR
LOGS_DIR = os.path.join(BASE_DIR, os.getenv('LOGS_BASE_DIR'))
TOKEN = os.getenv('telegram_bot_token')

formatter = \
    '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
logging.basicConfig(
    filename=f'{LOGS_DIR}/bot-from-{timezone.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING
)


class Command(BaseCommand):
    help = "Run telegram bot."

    def handle(self, *args, **options):
        bot = telebot.TeleBot(TOKEN)

        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            check_it_is_bot(message=message, bot=bot)

            text = "Рад тебя видеть друг мой"
            chat_id = message.from_user.id

            user = create_new_user(message=message, chat_id=chat_id)

            if message.text is not None:
                try:
                    tag = str(message.text).split(" ")[1]
                except Exception:
                    tag = message.text
                restaurants = Restaurant.objects.filter(tag=tag)
                if restaurants.exists():
                    restaurant = restaurants.first()
                    text = f"Здравствуй {user.first_name}. Добро пожаловать в ресторан '{restaurant.title}'." \
                           f"\nВведите номер вашего заказа:"
            bot.send_message(chat_id=message.from_user.id, text=text)

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            text = 'Я создан для отправки заказов, а не для того что бы разговаривать с вами 😐'
            chat_id = message.from_user.id
            if str(message.text).isnumeric():
                users = User.objects.filter(telegram_chat_id=chat_id)
                if not users.exists():
                    text = "Упс. Попробуйте просканировать QR еще раз"
                    bot.send_message(chat_id=chat_id, text=text)
                user = users.first()
                new_order = Order.objects.create(
                    user_id=user.id, order_number=message.text
                )
                text = f"Отлично {user.first_name}. Ваш заказ №{new_order.order_number} зарегестрирован.\n" \
                       f"Вам напишут когда ваш заказ будет готов."
            bot.send_message(chat_id=message.from_user.id, text=text)

        bot.polling(none_stop=True)
