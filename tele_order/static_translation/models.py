from django.db import models
from translations.models import Translatable
from tele_order.mixins.models import UpdateTimestampMixin, ValidateErrorMixin
from django.utils.translation import gettext_lazy as _
from tele_order.utils import constants


class StaticTranslation(Translatable, UpdateTimestampMixin, ValidateErrorMixin):
    """ A class used to represent an Update Logs """
    key = models.PositiveIntegerField(
        unique=True, choices=constants.CHAT_MESSAGES, verbose_name=_("Ключ"))
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
