from django.utils.translation import gettext_lazy as _
from . import constants

MAX_IMAGE_SIZE = _(f"Максимально допустимый размер изображения - "
                   f"{constants.MAX_IMAGE_SIZE} мб")

FIRST_SYMBOL_VALIDATION = _("Первый символ должен быть маленькой "
                            "буквой английского алфавита")
TAG_ANOTHER_SYMBOLS = _("тэг должен состоять из английского алфавита, "
                        "чисел или нижнего прочерка '_'")
TAG_MIN_LENGTH = _(f"Тэг должен быть больше "
                   f"{constants.TAG_MIN_LENGTH} символов")
TAG_MAX_LENGTH = _(f"Тэг должен быть меньше "
                   f"{constants.TAG_MAX_LENGTH} символов")
TAG_ALREADY_EXIST = _("Такой тэг уже есть")
