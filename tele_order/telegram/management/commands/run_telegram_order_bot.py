import logging
import telebot
import os
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from tele_order.core.models import (User, Order, Restaurant, Promotion)
from tele_order.static_translation.models import StaticTranslation
from dotenv import load_dotenv
from tele_order.telegram.service import check_it_is_bot, create_new_user, \
    is_client, is_manager, manager_orders, client_orders, display_markup, \
    order_detail, get_language
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
            chat_id = message.from_user.id
            language = get_language(message=message)

            check_it_is_bot(message=message, bot=bot)
            user = create_new_user(message=message, chat_id=chat_id)

            content_type_id = \
                ContentType.objects.get_for_model(StaticTranslation).id
            text = StaticTranslation.objects.filter(
                content_type_id=content_type_id, key=1
            ).translate(language).first().value

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
            language = get_language(message=message)
            if message.text[0] == "№":
                order_detail(message=message, bot=bot,
                             chat_id=chat_id, language=language)
            elif message.text == "/my_orders":
                if is_client(message=message):
                    markup, count = client_orders(message=message)
                    display_markup(
                        chat_id=chat_id, markup=markup,
                        count=count, bot=bot
                    )
                elif is_manager(message=message):
                    markup, count = manager_orders(message=message)
                    display_markup(
                        chat_id=chat_id, markup=markup,
                        count=count, bot=bot
                    )
            elif str(message.text).isnumeric():
                users = User.objects.filter(
                    telegram_chat_id=chat_id, role=constants.USER
                )
                if not users.exists():
                    text = "Упс. Попробуйте просканировать QR еще раз"
                    bot.send_message(chat_id=chat_id, text=text)
                else:
                    user = users.first()
                    new_order = Order.objects.create(
                        # restaurant_id=restaurant_id,
                        user_id=user.id, order_number=message.text
                    )
                    text = f"Отлично {user.first_name}. Ваш заказ №{new_order.order_number} зарегестрирован.\n" \
                           f"Вам напишут когда ваш заказ будет готов."
                    bot.send_message(chat_id=message.from_user.id, text=text)
            else:
                bot.send_message(chat_id=message.from_user.id, text=text)

        bot.polling(none_stop=True)
