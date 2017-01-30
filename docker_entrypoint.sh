#!/bin/sh
/usr/local/bin/python /pipeline/source/manage.py db upgrade && /usr/local/bin/python /pipeline/source/manage.py runserver -h 0.0.0.0
