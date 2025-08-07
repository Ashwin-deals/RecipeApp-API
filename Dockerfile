# A docker file to build a docker image for the app. 

FROM python:3.9-alpine3.13
LABEL maintainer="ashwin"
 
# Environment variable inside a container. The output will show immediately in the console.
ENV PYTHONUNBUFFERED 1

# Copying into the tmp directory
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# A working directory 
WORKDIR /app 

# Communication channel number
EXPOSE 8000

# When I use it through this docker compose file it overrides to true. In case if any other docker compose file 
# it shows false
ARG DEV=false    

# This runs a command on the Alpine image 
RUN apk add --no-cache postgresql-client && \
    apk add --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    python -m venv /py && \
    /py/bin/pip install pip==21.2.4 && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    # Removing after compiling into the project
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add virtual environment path to system PATH
ENV PATH="/py/bin:$PATH"

# Before the user, everything will be run as a root user.
USER django-user
