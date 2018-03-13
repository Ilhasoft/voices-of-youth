#!/bin/bash
python manage.py migrate
gunicorn voicesofyouth.wsgi -c gunicorn.conf.py