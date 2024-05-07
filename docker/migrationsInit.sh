#!/bin/sh

# Wait for the database to become available
while ! nc -z database 5432; do
    echo 'Waiting for PostgreSQL database to become available...'
    sleep 5;
done;
echo 'PostgreSQL is available. Proceeding with migrations...';

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py loaddata Populate.json
python importCSV.py