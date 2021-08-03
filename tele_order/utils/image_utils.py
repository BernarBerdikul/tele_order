import os
from urllib.parse import urljoin
from django.conf import settings
from django.utils import timezone
from tele_order.utils.constants import (
    IMAGE_PROMOTION_SAVE_PATH, IMAGE_QR_SAVE_PATH
)


def get_full_url(image):
    """ params: image - instance of ImageField """
    if not image:
        return None
    return urljoin(settings.SITE_URL, image.url)


def __files_unique_name(filename, new_filename: str, folder='images'):
    _, ext = os.path.splitext(filename.lower())
    return f"{folder}/{new_filename}{ext}"


def promotion_image(instance, filename):
    name = f'promotion_image_{instance.title}_{timezone.now().strftime("%Y-%m-%d %H:%M")}'
    return __files_unique_name(
        filename, new_filename=name, folder=IMAGE_PROMOTION_SAVE_PATH)


def qr_codes_path(instance, filename):
    name = f'{instance.tag}_qr_code_{timezone.now().strftime("%Y-%m-%d %H:%M")}'
    return __files_unique_name(
        filename, new_filename=name, folder=IMAGE_QR_SAVE_PATH)
