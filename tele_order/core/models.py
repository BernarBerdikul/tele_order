from io import BytesIO
import os
import qrcode
from django.core.files import File
from django.db import models
from translations.models import Translatable
from tele_order.mixins.models import UpdateTimestampMixin, ValidateErrorMixin
from tele_order.mixins.resized_field import ResizedImageField
from tele_order.static_translation.models import StaticTranslation
from tele_order.utils import constants
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from tele_order.utils.image_utils import (
    qr_codes_path, promotion_image
)
from tele_order.utils.validators import validate_image
from dotenv import load_dotenv
from tele_order.utils.validators import validate_tag
import telebot

load_dotenv()

BOT_PATH = os.getenv('telegram_bot_address')
TOKEN = os.getenv('telegram_bot_token')


class UserManager(BaseUserManager):
    """ Django Manager class for model User """

    def create_superuser(self, username, password):
        """ overwrite method for superuser creating """
        user = self.model(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.role = constants.SUPER_ADMIN
        user.save(using=self._db)
        return user


class User(Translatable, AbstractBaseUser, PermissionsMixin,
           UpdateTimestampMixin):
    """ A class used to represent a Manager of Restaurant """
    username = models.CharField(
        max_length=128, unique=True, verbose_name=_("Логин пользователя"))
    password = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_("Пароль"))
    first_name = models.CharField(
        max_length=128, verbose_name=_("Логин пользователя"))
    last_name = models.CharField(
        max_length=128, verbose_name=_("Логин пользователя"))
    telegram_chat_id = models.CharField(
        max_length=10, unique=True, db_index=True,
        verbose_name=_("ID пользователя в Телеграм"))
    language_code = models.CharField(
        max_length=2, default=constants.DEFAULT_LANGUAGE,
        verbose_name=_("Язык"))
    role = models.CharField(
        max_length=30, choices=constants.USER_TYPES,
        default=constants.USER, verbose_name=_("Роль пользователя"))
    is_active = models.BooleanField(
        default=True, verbose_name=_("Пользователь активен"))
    last_restaurant_id = models.IntegerField(
        blank=True, null=True, verbose_name=_("ID последнего ресторана"))

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """ Return user's username and role when calling object """
        return f'{self.pk} - {self.username} - {self.role}'

    @property
    def is_staff(self):
        # Anyone who is superuser can enter admin
        return self.is_superuser


class Restaurant(Translatable, UpdateTimestampMixin, ValidateErrorMixin):
    """ A class used to represent a Restaurant """
    manager = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='restaurant',
        verbose_name=_("Пользователь"))
    tag = models.SlugField(
        max_length=constants.TAG_MAX_LENGTH, blank=True, null=True,
        verbose_name=_("Тэг ресторана"), validators=[validate_tag])
    title = models.CharField(
        blank=True, null=True, max_length=64,
        verbose_name=_("Название ресторана"))
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Описание ресторана"),
        max_length=1024)
    enable = models.BooleanField(
        default=True, verbose_name=_("Активен"))
    qr_code = ResizedImageField(
        upload_to=qr_codes_path, size=[400, 400], blank=True, null=True,
        force_format='JPEG', verbose_name=_("QR код"),
        validators=[validate_image])

    def save(self, *args, **kwargs):
        """ overwrite save method for QR-code generating when
            we will dump db data """
        site = f"https://{BOT_PATH}?start={self.tag}"
        buffer = BytesIO()
        qr = qrcode.QRCode(version=1, box_size=15, border=0,
                           error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(site)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(buffer, 'PNG')
        fname = f'qr_code-{self.tag}.png'
        self.qr_code.save(fname, File(buffer), save=False)
        """ before save"""
        super().save(*args, **kwargs)
        """ after save"""

    def __str__(self):
        """ Return restaurant title when calling object """
        return f'{self.pk} - {self.title}'

    class Meta:
        db_table = 'restaurant'
        verbose_name = _('Ресторан')
        verbose_name_plural = _('Рестораны')

    class TranslatableMeta:
        """ fields that are translated in the database """
        fields = ['title', 'description']


class Order(Translatable, UpdateTimestampMixin, ValidateErrorMixin):
    """ A class used to represent an Order of User """
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='orders',
        blank=True, null=True,
        verbose_name=_("Ресторан"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders',
        verbose_name=_("Пользователь"))
    order_number = models.PositiveIntegerField(
        verbose_name=_("Статус заказа"))
    order_accepted = models.BooleanField(
        default=False, verbose_name=_("Завершен"))

    def save(self, *args, **kwargs):
        if self.pk is not None and self.order_accepted is True:
            bot = telebot.TeleBot(TOKEN)
            chat_id = self.user.telegram_chat_id
            text = StaticTranslation.objects.translate(
                self.user.language_code
            ).get(key=constants.MESSAGE_6).value
            bot.send_message(chat_id=chat_id, text=text)
            send_promotion(bot=bot, chat_id=chat_id)
        """ before save"""
        super().save(*args, **kwargs)
        """ after save"""

    class Meta:
        db_table = 'order'
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def __str__(self):
        """ Return user's username when calling object """
        return f'{self.pk} - {self.user.first_name}'


class Promotion(Translatable, UpdateTimestampMixin, ValidateErrorMixin):
    """ A class used to represent a Restaurant """
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, blank=True, null=True,
        related_name='promotions', verbose_name=_("Ресторан"))
    title = models.CharField(
        max_length=64, verbose_name=_("Заголовок"))
    description = models.TextField(
        max_length=1024, blank=True, null=True, verbose_name=_("Описание"))
    enable = models.BooleanField(
        default=False, verbose_name=_("Активен"))
    image = models.ImageField(
        upload_to=promotion_image, blank=True, null=True,
        verbose_name=_("Фото"), validators=[validate_image])

    def __str__(self):
        """ Return promotion's title when calling object """
        return f'{self.pk} - {self.title}'

    class Meta:
        db_table = 'promotion'
        verbose_name = _('Реклама')
        verbose_name_plural = _('Реклама')

    class TranslatableMeta:
        """ fields that are translated in the database """
        fields = ['title', 'description']


def send_promotion(bot, chat_id):
    promotions = Promotion.objects.all()
    if promotions.exists():
        promotion = promotions.first()
        promotion_image = promotion.image
        bot.send_message(
            chat_id=chat_id,
            text=f"{promotion.title}\n\n{promotion.description}")
        bot.send_photo(chat_id=chat_id, photo=promotion_image)


