#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
echo "server running at port 8000"
echo "Author = QuatumSoftlutions"
python manage.py runserver 0.0.0.0:8000
