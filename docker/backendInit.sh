#!/bin/sh

while ! nc -z database 5432; do
    echo 'Waiting for PostgreSQL database to become available...'
    sleep 5;
done;
echo 'Migrations complete. Starting backend...';

python manage.py loaddata Populate.json
python manage.py runserver 0.0.0.0:3000