import qrcode
import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

BOT_PATH = os.getenv('telegram_bot_address')


def generate_qr_code() -> str:
    """ method for QR-code generating """
    site = f'https://{BOT_PATH}?start=1'
    file_name = f"{settings.MEDIA_ROOT}/tm_bot_test.png"
    qr = qrcode.QRCode(
        version=1, box_size=15, border=0,
        error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(site)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)
    return os.path.dirname(os.path.abspath(file_name))


print(generate_qr_code())
