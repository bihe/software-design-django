FROM python:3.13-slim
WORKDIR /opt/django-app

COPY . /opt/django-app/
COPY ./containers/simple/entrypoint.sh /opt/django-app/
RUN pip install -r /opt/django-app/requirements.txt

ENV DJANGO_SUPERUSER_PASSWORD=admin

EXPOSE 8000

# NOTE: this is not a best practice approach because 
# the container will run as root which is a security risk
# https://medium.com/@ayoubseddiki132/why-running-docker-containers-as-root-is-a-security-nightmare-and-how-to-fix-it-83a60509d9bf

# the entrypoint is a shell script which does migrations and launches the app via gunicorn
ENTRYPOINT ["/opt/django-app/entrypoint.sh"]
