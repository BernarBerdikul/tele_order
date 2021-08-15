from django.utils.translation import gettext_lazy as _

ANALOG_LANGUAGE = "en"
DEFAULT_LANGUAGE = "ru"

""" LANGUAGES """
TRANSLATION_LANGUAGES = (
    ("ru", _("Русский")),
    ("en", _('Английский')),
    ("kk", _('Казахский')),
)
###############################################################################
""" PROJECT CONSTANTS """
DEVELOPERS_TIMEZONE = "Asia/Almaty"

IMAGE_QR_SAVE_PATH = 'restaurants'
IMAGE_PROMOTION_SAVE_PATH = 'promotions'

PHONES_MIN_LENGTH = 11
MAX_IMAGE_SIZE = 20  # in Mb

JANUARY = 1
FEBRUARY = 2
MARCH = 3
APRIL = 4
MAY = 5
JUNE = 6
JULY = 7
AUGUST = 8
SEPTEMBER = 9
OCTOBER = 10
NOVEMBER = 11
DECEMBER = 12

MONTHS = (
    (JANUARY, _('янв'), _('января')),
    (FEBRUARY, _('фев'), _('февраля')),
    (MARCH, _('мар'), _('марта')),
    (APRIL, _('апр'), _('апреля')),
    (MAY, _('май'), _('мая')),
    (JUNE, _('июнь'), _('июня')),
    (JULY, _('июль'), _('июля')),
    (AUGUST, _('авг'), _('августа')),
    (SEPTEMBER, _('сен'), _('сентября')),
    (OCTOBER, _('окт'), _('октября')),
    (NOVEMBER, _('ноя'), _('ноября')),
    (DECEMBER, _('дек'), _('декабря')),
)

""" CORE APP """
USER = 'USER'
MANAGER = 'MANAGER'
SUPER_ADMIN = 'SUPER_ADMIN'

USER_TYPES = (
    (USER, _("Пользователь")),
    (MANAGER, _("Менеджер")),
    (SUPER_ADMIN, _("Супер админ")),
)

TAG_MIN_LENGTH = 3
TAG_MAX_LENGTH = 32
REGEX_FOR_TAG = r"^[a-zA-Z0-9_]+$"
REGEX_FOR_FIRST_SYMBOL = r"^[a-z]"
""" RESTAURANT's TAG """
RESERVED_TAG_LIST = [
    'api', 'super-secret-admin', 'media', 'admin', 'login', 'static',
]

WELCOME_MESSAGE = 0

TELEGRAM_ERROR_CHAT_ID = 421591563
TELEGRAM_MESSAGES = (
    (WELCOME_MESSAGE, _("HELLO"))
)

###############################################################################
""" Translation keys """
MESSAGE_1 = 1
MESSAGE_2 = 2
MESSAGE_3 = 3
MESSAGE_4 = 4
MESSAGE_5 = 5
MESSAGE_6 = 6
MESSAGE_7 = 7
MESSAGE_8 = 8
MESSAGE_9 = 9
MESSAGE_10 = 10
MESSAGE_11 = 11
MESSAGE_12 = 12

CHAT_MESSAGES = (
    (MESSAGE_1, "Рад тебя видеть друг мой"),
    (MESSAGE_2, f"Здравствуй %s. Добро пожаловать в ресторан '%s'."
                f"\nВведите номер вашего заказа:"),
    (MESSAGE_3, 'Я создан для отправки заказов, а не для того '
                'что бы разговаривать с вами 😐'),
    (MESSAGE_4, f"Отлично %s. Ваш заказ №%d зарегестрирован.\n"
                f"Вам напишут когда ваш заказ будет готов."),
    (MESSAGE_5, "Упс. Попробуйте просканировать QR еще раз"),
    (MESSAGE_6, "Спасибо за ожидание ваш заказ готов!"),
    (MESSAGE_7, "Выберите активный заказ"),
    (MESSAGE_8, "У вас нет активных заказов"),
    (MESSAGE_9, f"Номер заказа: %d\nДата заказа: %s"),
    (MESSAGE_10, "Мы с ботами не работаем"),
)
