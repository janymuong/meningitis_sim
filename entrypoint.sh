#!/bin/sh
set -e

python manage.py migrate

# start Django server
exec python manage.py runserver 0.0.0.0:8000
