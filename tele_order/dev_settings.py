from .settings import *


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS += [

]

SITE_URL = 'https://tele_order.kz'  # example

IS_LOCAL = False

""" LOGS """
LOGS_BASE_DIR = os.path.join(BASE_DIR, os.getenv('LOGS_BASE_DIR'))
LOG_TO_TELEGRAM_BOT_TOKEN = os.getenv('telegram_bot_token')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s path: '
                      '%(pathname)s module: %(module)s method: '
                      '%(funcName)s  row: %(lineno)d message: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_BASE_DIR, 'console.log'),
            'formatter': 'console'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_BASE_DIR, 'info.log'),
            'formatter': 'verbose',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_BASE_DIR, 'error.log'),
            'formatter': 'verbose',
        },
        'telegram_log': {
            'level': 'ERROR',
            # 'filters': ['require_debug_false'],
            'class': 'tele_order.telegram.log.AdminTelegramHandler',
            'bot_token': LOG_TO_TELEGRAM_BOT_TOKEN,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['telegram_log', 'error'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
