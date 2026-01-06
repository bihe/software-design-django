# A multi-stage build docker file
# https://docs.docker.com/build/building/multi-stage/
#
# the first) stage is used to build the application
# the main advantage is, that NO build-tools need to be available locally
# everything is done "inside" the image
#
# there are a couple of images available: https://hub.docker.com/_/python/

FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config 

# Change the working directory to the `app` directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Disable development dependencies
ENV UV_NO_DEV=1

# WHY? https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --no-dev --group prod


# ---------------------------------------------------------------------------
# the second) stage is used for runtime/production
# we have now a different base-image which is smaller for production
FROM python:3.13-slim

WORKDIR /opt/django-app

ENV PATH="/opt/django-app/.venv/bin:$PATH"

# still we needs some additional stuff
# we need mariadb library (very, very similar to mysql) to access the db
# this is the runtime library dependency of mysqlclient
RUN apt-get update && apt-get install -y default-libmysqlclient-dev curl

# the path in the container where the app is located
RUN mkdir -p /opt/django-app

# it is a best practise to create a seperate user and not execute everything with root
RUN useradd -d /opt/django-app django-app-user

# change the ownership of the path to the created user
RUN chown django-app-user /opt/django-app

# from now on, every action in the Dockerfile is done using the given user
USER django-app-user

# copy our project to the application directory
COPY --chown=django-app-user . /opt/django-app

# Copy the environment with the dependencies from the build-stage
COPY --from=builder --chown=django-app-user /app/.venv /opt/django-app/.venv

# overwrite the settings.py file
COPY --chown=django-app-user ./swd_django_demo/settings_prod.py /opt/django-app/swd_django_demo/settings.py
# clean up the settings_prod file - not needed any more because we have copied it
RUN rm /opt/django-app/swd_django_demo/settings_prod.py

# move the gunicorn runner to a new location
COPY --chown=django-app-user ./swd_django_demo/run_gunicorn.py /opt/django-app/run_gunicorn.py
# clean up the run_guniconr file from the project-location, it was copied above
RUN rm /opt/django-app/swd_django_demo/run_gunicorn.py 

# need the entry point as well
# the entry point applies needed migrations (should not be ncessary because of the SQL dump)
COPY --from=builder --chown=django-app-user /app/containers/django-app/entrypoint.sh /opt/django-app/

# the app listens on the following port (via unicorn, not the django development server!)
EXPOSE 8000

# the entrypoint is a shell script which does migrations and launches the app via gunicorn
ENTRYPOINT ["/opt/django-app/entrypoint.sh"]
