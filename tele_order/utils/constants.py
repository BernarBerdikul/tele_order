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

MEDIA_DISHES = "dish"

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
    (USER, _("Менеджер")),
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
