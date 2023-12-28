#!/bin/bash
result=1
while [[ $result == 1 ]]; do
    mysql --user=root --password=root-password --host=database --execute "use django-demo"
    result=$?
    sleep 0.5
done

python /opt/django-demo/manage.py migrate
python /opt/django-demo/manage.py createsuperuser --noinput --username admin --email admin@localhost
python /opt/django-demo/manage.py runserver 0.0.0.0:8000