from django.contrib.contenttypes.models import ContentType
from django.db import models
from translations.models import Translatable
from tele_order.mixins.models import UpdateTimestampMixin, ValidateErrorMixin
from django.utils.translation import gettext_lazy as _


HELLO_MESSAGE = 0  # Рад тебя видеть друг мой
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

CHAT_MESSAGES = (
    (HELLO_MESSAGE, "hello_message"),
    (FEBRUARY, _('фев')),
    (MARCH, _('мар')),
    (APRIL, _('апр')),
    (MAY, _('май')),
    (JUNE, _('июнь')),
    (JULY, _('июль')),
    (AUGUST, _('авг')),
    (SEPTEMBER, _('сен')),
    (OCTOBER, _('окт')),
    (NOVEMBER, _('ноя')),
    (DECEMBER, _('дек')),
)


class StaticTranslation(Translatable, UpdateTimestampMixin, ValidateErrorMixin):
    """ A class used to represent an Update Logs """
    key = models.PositiveIntegerField(
        choices=CHAT_MESSAGES, verbose_name=_("Ключ в словаре"))
    value = models.CharField(
        blank=True, null=True, max_length=255,
        verbose_name=_("Статичная запись"))
    description = models.CharField(
        max_length=256, verbose_name=_("Дополнительное поле"))

    class Meta:
        db_table = 'static_translation'
        verbose_name = _('Статический перевод')
        verbose_name_plural = _('Статические переводы')

    class TranslatableMeta:
        """ fields that are translated in the database """
        fields = ['value']

    def __str__(self):
        """ Return key and value of changes when calling object """
        return f'{self.pk} - {self.key} - {self.value}'
