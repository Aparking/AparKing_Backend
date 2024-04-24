#!/bin/sh

# Iniciar PostgreSQL
service postgresql start

# Configurar usuario y base de datos
su - postgres -c "psql -c \"CREATE USER aparking WITH PASSWORD 'aparking';\""
su - postgres -c "psql -c \"CREATE DATABASE aparking_db OWNER aparking;\""
su - postgres -c "psql -d aparking_db -c \"CREATE EXTENSION postgis;\""

# Espera hasta que la base de datos esté disponible
while ! nc -z localhost 5432; do
    echo 'Waiting for PostgreSQL database to become available...'
    sleep 1
done
echo 'Database is available.'

python manage.py makemigrations
python manage.py migrate --noinput
python importCSV.py

# Inicia el servidor Django en el fondo temporalmente
echo 'Starting backend...'
python manage.py runserver 0.0.0.0:3000 &

# Almacena el ID del proceso
SERVER_PID=$!

sleep 10

# Carga los datos
echo 'Loading data...'
python manage.py loaddata Populate.json

# Trae el servidor de nuevo al primer plano
wait $SERVER_PID
