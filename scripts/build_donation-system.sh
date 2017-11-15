#!/bin/sh
#
set -e # stops execution on error
python manage.py syncdb --noinput
python manage.py migrate
python manage.py test
