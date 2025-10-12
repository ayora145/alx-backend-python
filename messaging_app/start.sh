#!/bin/bash
set -e

echo "Waiting for database..."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000