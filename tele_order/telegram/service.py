from django.contrib.auth.models import User
from tele_order.utils import constants


def check_it_is_bot(message, bot) -> None:
    """ return error message, if user is bot """
    if message.from_user.is_bot:
        text = "Мы с ботами не работаем"
        bot.send_message(chat_id=message.from_user.id, text=text)
    return None


def create_new_user(message, chat_id: int):
    """ try create new user, else return user from DB """
    if message.from_user.last_name is not None:
        last_name = message.from_user.last_name
    else:
        last_name = None
    """ find user in db """
    users = User.objects.filter(telegram_chat_id=chat_id)
    if users.exists():
        user = users.first()
    else:
        language_code = message.from_user.language_code
        if language_code is None:
            language_code = constants.DEFAULT_LANGUAGE
        user = User.objects.create(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=last_name,
            telegram_chat_id=chat_id,
            language_code=language_code[:2]
        )
    return user
