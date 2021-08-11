from django.contrib import admin
from .models import StaticTranslation
from ..mixins.paginator import OBJECTS_PER_PAGE_IN_ADMIN, LargeTablePaginator
from translations.admin import TranslatableAdmin, TranslationInline


@admin.register(StaticTranslation)
class StaticTranslationAdmin(TranslatableAdmin):
    """ A class used to represent a Order model in admin page """
    list_display = ['id', 'key', 'value']
    list_display_links = ['id', 'key']
    search_fields = ('id',)
    list_per_page = OBJECTS_PER_PAGE_IN_ADMIN
    paginator = LargeTablePaginator
    inlines = [TranslationInline]
    fields = ('key', 'value', 'description')
