import os
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv
import django

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tele_order.settings')
django.setup()

application = get_asgi_application()
