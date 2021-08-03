from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from translations.admin import TranslatableAdmin, TranslationInline
from .models import (User, Restaurant, Order, Promotion)
from ..mixins.paginator import OBJECTS_PER_PAGE_IN_ADMIN, LargeTablePaginator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from tele_order.utils import constants


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ A class used to represent a Manager model in admin page """
    list_display = ['id', 'username', 'first_name', 'last_name', 'role',
                    'telegram_chat_id']
    list_display_links = ['id', 'username', 'first_name', 'last_name']
    fieldsets = (
        ('Main Fields', {'fields': (
            'username', 'first_name', 'last_name', 'role', 'is_active', 
            'language_code', 'telegram_chat_id'
        )}),
        ('Password', {'fields': ('password',)})
    )
    search_fields = ('id', 'username', 'telegram_chat_id')
    list_per_page = OBJECTS_PER_PAGE_IN_ADMIN
    paginator = LargeTablePaginator


@admin.register(Restaurant)
class RestaurantAdmin(TranslatableAdmin):
    """ A class used to represent a Restaurant model in admin page """
    list_display = ('id', 'tag', 'title', 'enable')
    list_display_links = ('id', 'tag', 'title', 'enable')
    inlines = [TranslationInline]
    fieldsets = (
        (_('Основные поля'), {
            'fields': (
                ('manager', 'tag', 'title', 'description', 'enable')
            )
        }),
        (_('QR'), {
            'fields': (
                ('image_qr_code', 'qr_code', 'get_qr_download_url'),
            )
        }),
    )
    list_per_page = OBJECTS_PER_PAGE_IN_ADMIN
    search_fields = ('id', 'tag')
    paginator = LargeTablePaginator
    readonly_fields = ['image_qr_code', 'get_qr_download_url']

    def image_qr_code(self, obj):
        """ function for representing restaurant's qr-code
            image on admin Restaurant change/add page """
        if obj.qr_code:
            print(obj.qr_code.name)
            url = f"{settings.MEDIA_URL}/" \
                  f"{obj.qr_code.name}"
            return mark_safe(f'<img src="{url}" width="320px" />')

    image_qr_code.short_description = _('QR код')

    def get_qr_download_url(self, obj):
        """ qr-code download url """
        if obj.qr_code:
            return format_html(
                f'<a href="{obj.qr_code.url}" download="{obj.qr_code.url}">{_("Скачать")}</a>')

    get_qr_download_url.short_description = _('скачать QR код')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ A class used to represent a Order model in admin page """
    list_display = ['id', 'restaurant', 'user', 'order_number', 'order_accepted']
    list_display_links = ['id', 'restaurant', 'user', 'order_number']
    search_fields = ('id', 'user__username', 'restaurant__title', 'user__id')
    list_per_page = OBJECTS_PER_PAGE_IN_ADMIN
    paginator = LargeTablePaginator
    fields = ('restaurant', 'user', 'order_number', 'order_accepted')
    # readonly_fields = ['restaurant', 'user']


@admin.register(Promotion)
class PromotionAdmin(TranslatableAdmin):
    """ A class used to represent a Order model in admin page """
    list_display = ['id', 'title', 'enable', 'restaurant']
    list_display_links = ['id', 'title', 'enable', 'restaurant']
    search_fields = ('id', 'restaurant__id', 'restaurant__title')
    list_per_page = OBJECTS_PER_PAGE_IN_ADMIN
    paginator = LargeTablePaginator
    inlines = [TranslationInline]
    fields = ('restaurant', 'title', 'description', 'enable', 'image')
    readonly_fields = ['promotion_image']

    def promotion_image(self, obj):
        """ function for representing promotion's image
            on admin Restaurant change/add page """
        if obj.qr_code:
            url = f"{settings.MEDIA_URL}/{constants.IMAGE_PROMOTION_SAVE_PATH}/" \
                  f"{obj.image.name}"
            return mark_safe(f'<img src="{url}" width="320px" />')

    promotion_image.short_description = _('Фото рекламы')
