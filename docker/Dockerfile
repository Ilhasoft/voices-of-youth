###############################################################################
# Build stage
# Creation date: 06/02/2018
# Author: eltonplima
###############################################################################
FROM ubuntu:18.04

LABEL maintainer="eltonplima@gmail.com"

ENV HOME /home/app
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR $HOME
RUN useradd webapp && \
chown webapp.webapp -R $HOME && \
chmod a+s -R $HOME && \
apt-get update && \
apt-get dist-upgrade -y && \
apt-get install -y python3-pip gdal-bin libgdal-dev git && \
pip3 install -U pip pipenv setuptools gunicorn

COPY . .
RUN pipenv install --system
RUN chmod +x docker/entrypoint.sh
RUN python3 manage.py collectstatic --noinput

ENTRYPOINT ["gunicorn", "voicesofyouth.wsgi", "-c", "gunicorn.conf.py"]
EXPOSE 8000
