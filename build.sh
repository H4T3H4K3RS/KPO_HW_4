#!/bin/bash
echo ====CREATING MIGRATIONS [START]====
python manage.py makemigrations
echo ====CREATING MIGRATIONS [END]====

echo ====MIGRATING [START]====
python manage.py migrate
echo ====MIGRATING [END]====

echo ====RUNNING TESTS [START]====
python manage.py test
echo ====RUNNING TESTS [END]====

echo ====RUNNING SERVER [START]====
python manage.py runserver 0.0.0.0:8000 --noreload
