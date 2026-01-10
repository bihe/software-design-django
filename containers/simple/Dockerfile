FROM python:3.13-slim
WORKDIR /opt/django-app

COPY . /opt/django-app/
COPY ./containers/simple/entrypoint.sh /opt/django-app/
RUN pip install -r /opt/django-app/requirements.txt

ENV DJANGO_SUPERUSER_PASSWORD=admin

EXPOSE 8000

# the entrypoint is a shell script which does migrations and launches the app via gunicorn
ENTRYPOINT ["/opt/django-app/entrypoint.sh"]