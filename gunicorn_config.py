command = '/srv/www/env/bin/gunicorn'
pythonpath = '/srv/www/tele_order'
bind = '0.0.0.0:8000'
workers = 8
user = 'root'
limit_request_fields = 32000
limit_request_fields_size = 0
raw_env = ["DJANGO_SETTINGS_MODULE=menushka.dev_settings"]