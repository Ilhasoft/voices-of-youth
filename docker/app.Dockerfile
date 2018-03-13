###############################################################################
# Build stage
# Creation date: 06/02/2018
# Author: eltonplima
###############################################################################
# FROM python:3.6-alpine as builder

# WORKDIR /home/app
# RUN apk update && apk upgrade && apk add alpine-sdk postgresql-dev libffi-dev \
# libxml2-dev py-virtualenv libxslt-dev jpeg-dev && \
# apk add gdal gdal-dev --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ && \
# pip install virtualenv && virtualenv -p python3.6 env
# COPY . .
# RUN ./pip install -r requirements.txt && ./pip install -U psycopg2

###############################################################################
# Deploy stage
###############################################################################
FROM python:3.6-alpine

WORKDIR /home/app
RUN apk update && apk add alpine-sdk postgresql-dev libffi-dev \
libxml2-dev libxslt-dev jpeg-dev && \
apk add gdal gdal-dev --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/
RUN apk add libpq libxml2 libxslt libmagic nodejs jpeg
RUN curl -o- -L https://yarnpkg.com/install.sh | sh
ENV PATH /root/.yarn/bin:$PATH
RUN apk add gdal --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/
RUN pip install gunicorn
COPY . .
RUN yarn install
RUN pip install -r development.txt && pip install -U psycopg2
RUN python manage.py collectstatic --noinput
RUN apk del alpine-sdk postgresql-dev libffi-dev libxml2-dev libxslt-dev jpeg-dev gdal-dev
RUN ls -l docker
RUN chmod +x ./docker/entrypoint.sh
EXPOSE 8000
ENTRYPOINT $WORKDIR/docker/entrypoint.sh
