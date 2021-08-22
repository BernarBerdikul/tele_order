import logging
import telebot
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from tele_order.core.models import (User, Order, Restaurant)
from tele_order.static_translation.models import StaticTranslation
from dotenv import load_dotenv
from tele_order.telegram.service import (
    check_it_is_bot, get_or_create_user, client_orders,
    display_markup, order_detail_client, get_language, is_manager,
    manager_orders, is_client, order_detail_manager
)
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
            """ get user's params """
            chat_id = message.from_user.id
            language = get_language(message=message)

            keyboard = telebot.types.ReplyKeyboardMarkup()
            check_it_is_bot(message=message, bot=bot, language=language)
            if message.text is not None:
                try:
                    tag = str(message.text).split(" ")[1]
                except Exception:
                    tag = message.text
                restaurants = Restaurant.objects.filter(tag=tag)
                if restaurants.exists():
                    restaurant = restaurants.translate(language).first()
                    user = get_or_create_user(
                        message=message, chat_id=chat_id,
                        restaurant_id=restaurant.id
                    )
                    if user.role == constants.USER:
                        text = StaticTranslation.objects.translate(language).get(
                            key=constants.MESSAGE_2
                        ).value % (user.username, restaurant.title)
                        """ present orders for user """
                        restaurant_orders = Order.objects.filter(
                            restaurant_id=restaurant.id, order_accepted=False
                        )
                        """ generate telegram buttons for user """
                        for order in restaurant_orders:
                            keyboard.add(
                                telebot.types.KeyboardButton(
                                    f"{order.order_number}"
                                )
                            )
                        bot.send_message(
                            chat_id=chat_id, text=text, reply_markup=keyboard)
                    elif user.role == constants.MANAGER:
                        """ Ask Manager to create order """
                        text = StaticTranslation.objects.translate(
                            language
                        ).get(key=constants.MESSAGE_12).value
                        """ send message to Manager """
                        bot.send_message(chat_id=chat_id, text=text)

            else:
                """ get hello message from DB """
                text = StaticTranslation.objects.translate(
                    language
                ).get(key=constants.MESSAGE_1).value
                bot.send_message(chat_id=message.from_user.id, text=text)

        @bot.message_handler(commands=['my_orders'])
        def my_orders(message):
            chat_id = message.from_user.id
            language = get_language(message=message)
            if is_client(message=message):
                markup, count = client_orders(message=message)
                display_markup(
                    chat_id=chat_id, markup=markup,
                    count=count, bot=bot, language=language
                )
            elif is_manager(message=message):
                markup, count = manager_orders(message=message)
                display_markup(
                    chat_id=chat_id, markup=markup,
                    count=count, bot=bot, language=language
                )

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            """ get user's params """
            language = get_language(message=message)
            chat_id = message.from_user.id
            """ check if user created in db """
            users = User.objects.filter(telegram_chat_id=chat_id)
            if users.exclude(role=constants.USER).exists() and \
                    users.exclude(role=constants.MANAGER).exists():
                text = StaticTranslation.objects.translate(
                    language
                ).get(key=constants.MESSAGE_5).value
                bot.send_message(chat_id=chat_id, text=text)
            """ check if message starts from symbol '№' """
            if message.text[0] == "№":
                """ return detail of order """
                if users.filter(role=constants.USER).exists():
                    order_detail_client(
                        message=message, bot=bot,
                        chat_id=chat_id, language=language
                    )
                elif users.filter(role=constants.MANAGER).exists():
                    order_detail_manager(
                        message=message, bot=bot,
                        chat_id=chat_id, language=language
                    )
            elif str(message.text).isnumeric():
                """ check if message is 'number' type 
                    and without symbol '№' """
                order_number = int(message.text)
                if users.filter(role=constants.USER).exists():
                    """ Simple User """
                    user = users.first()
                    """ get restaurant's order """
                    restaurants_orders = Order.objects.filter(
                        restaurant_id=user.last_restaurant_id
                    )
                    """ update order by user """
                    if restaurants_orders.filter(
                            order_number=order_number).exists():
                        """ update order """
                        Order.objects.filter(
                            order_number=order_number,
                        ).update(user_id=user.id)
                        """ accept order """
                        text = StaticTranslation.objects.translate(
                            language
                        ).get(key=constants.MESSAGE_4).value % (
                            user.first_name, order_number
                        )
                        bot.send_message(chat_id=message.from_user.id,
                                         text=text)
                    else:
                        """ return error message that order does not exist """
                        text = StaticTranslation.objects.translate(
                            language
                        ).get(key=constants.MESSAGE_11).value
                        bot.send_message(chat_id=message.from_user.id,
                                         text=text)
                elif users.filter(role=constants.MANAGER).exists():
                    """ Restaurant's manager """
                    user = users.first()
                    """ get restaurant's order """
                    restaurants_orders = Order.objects.filter(
                        restaurant_id=user.last_restaurant_id,
                        order_number=order_number
                    )
                    """ create order if does not exists """
                    if not restaurants_orders.exists():
                        Order.objects.create(
                            restaurant_id=user.restaurant.id,
                            order_number=order_number
                        )
                        """ get message that order was created """
                        text = StaticTranslation.objects.translate(
                            language
                        ).get(key=constants.MESSAGE_15).value % (
                            order_number
                        )
                        bot.send_message(chat_id=message.from_user.id,
                                         text=text)
                    else:
                        """ make order accepted """
                        order = Order.objects.filter(
                            restaurant_id=user.restaurant.id,
                            order_number=order_number
                        ).first()
                        order.order_accepted = True
                        order.save()
                        """ get success updated message and 
                            the user was notified """
                        text = StaticTranslation.objects.translate(
                            language
                        ).get(key=constants.MESSAGE_16).value % (
                            order_number
                        )
                        bot.send_message(chat_id=message.from_user.id,
                                         text=text)
            else:
                """ return default text, that bot only for orders, 
                    neither for dialog """
                text = StaticTranslation.objects.translate(
                    language
                ).get(key=constants.MESSAGE_3).value
                bot.send_message(chat_id=message.from_user.id, text=text)

        bot.infinity_polling()
