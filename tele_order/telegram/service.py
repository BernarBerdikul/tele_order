from telebot import types
from tele_order.core.models import User, Order, Restaurant
from tele_order.static_translation.models import StaticTranslation
from tele_order.utils import constants
from tele_order.utils.timestamp_converter import (
    convert_datetime_with_hours_long
)


def check_it_is_bot(message, bot, language: str) -> None:
    """ return error message, if user is bot """
    if message.from_user.is_bot:
        text = StaticTranslation.objects.translate(
            language
        ).get(key=constants.MESSAGE_10).value
        bot.send_message(chat_id=message.from_user.id, text=text)
    return None


def create_new_user(message, chat_id: int, restaurant_id: int):
    """ try create new user, else return user from DB """
    if message.from_user.last_name is not None:
        last_name = message.from_user.last_name
    else:
        last_name = None
    """ find user in db """
    users = User.objects.filter(telegram_chat_id=chat_id)
    if users.exists():
        user = users.first()
        if user.last_restaurant_id != restaurant_id:
            User.objects.filter(id=user.id).update(
                last_restaurant_id=restaurant_id
            )
    else:
        language_code = message.from_user.language_code
        if language_code is None:
            language_code = constants.DEFAULT_LANGUAGE
        user = User.objects.create(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=last_name,
            telegram_chat_id=chat_id,
            language_code=language_code[:2],
            last_restaurant_id=restaurant_id
        )
    return user


def get_user(message):
    """ if user exists in DB then return them
        else create new user """
    chat_id = message.from_user.id
    user = User.objects.filter(telegram_chat_id=chat_id)
    if user.exists():
        return user.first()


def is_client(message) -> bool:
    if User.objects.filter(telegram_chat_id=message.from_user.id,
                           role=constants.USER):
        return True
    return False


def client_orders(message):
    orders = Order.objects.filter(
        user_id=get_user(message=message).id, order_accepted=False
    )
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for order in orders:
        markup.add(types.KeyboardButton(f'№{order.order_number}'))
    return markup, orders.count()


def is_manager(message):
    if User.objects.filter(telegram_chat_id=message.from_user.id,
                           role=constants.MANAGER):
        return True
    return False


def manager_orders(message):
    restaurant_orders = Restaurant.objects.filter(
        manager_id=get_user(message=message).id,
        orders__order_accepted=False
    )
    markup = types.ReplyKeyboardMarkup(row_width=2)
    if restaurant_orders.count() != 0:
        orders = restaurant_orders.first().orders.all()
        for order in orders:
            markup.add(types.KeyboardButton(f'№{order.order_number}'))
        return markup, orders.count()
    else:
        return markup, 0


def order_detail(message, bot, chat_id, language):
    if str(message.text[1:]).isnumeric():
        order_number = message.text[1:]
        orders = Order.objects.filter(order_number=order_number)
        if orders.exists():
            order = orders.translate_related(
                'restaurant'
            ).translate(language).first()
            """ prepare answer about order """
            answer = StaticTranslation.objects.translate(
                language
            ).get(key=constants.MESSAGE_9).value % (
                order.order_number, convert_datetime_with_hours_long(
                    datetime=order.date_create
                )
            )
            bot.send_message(chat_id, answer)


def display_markup(chat_id, markup, count, bot, language):
    if count != 0:
        text = StaticTranslation.objects.translate(
            language
        ).get(key=constants.MESSAGE_7).value
        bot.send_message(chat_id, text, reply_markup=markup)
    else:
        text = StaticTranslation.objects.translate(
            language
        ).get(key=constants.MESSAGE_8).value
        bot.send_message(chat_id, text)


def get_language(message):
    if message.from_user.language_code is not None:
        language = message.from_user.language_code
    else:
        language = constants.ANALOG_LANGUAGE
    return language
