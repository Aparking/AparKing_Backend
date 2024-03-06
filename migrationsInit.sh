#!/bin/bash
python manage.py migrate --noinput
# python manage.py flush --noinput # This will delete all data in the database
# python manage.py loaddata initial_data.json # This will load the initial data
python importCSV.py
