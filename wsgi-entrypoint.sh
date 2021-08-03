#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
rm -r django_static/*
cp -Rf static/* django_static


#############################
python manage.py run_telegram_order_bot &
exec gunicorn -c "./gunicorn_config.py" menushka.wsgi &
#exec daphne -b 0.0.0.0 -p 8000 menushka.asgi:application
# gunicorn menushka.wsgi --bind 0.0.0.0:8000 --workers 8 --threads 4
###############################################################################
# Options to DEBUG Django server
# Optional commands to replace above gunicorn command

# Option 1:
# run daphne with debug log level
# daphne menushka.asgi -b 0.0.0.0:8000

# Option 2:
# run development server
# DEBUG=True python manage.py runserver 0.0.0.0:8000