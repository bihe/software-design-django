#!/bin/sh
python /opt/django-app/manage.py migrate
python /opt/django-app/manage.py createsuperuser --noinput --username admin --email admin@localhost
# star the django development server
# NOTE: this is not a best-practice approach
python /opt/django-app/manage.py runserver 0.0.0.0:8000

