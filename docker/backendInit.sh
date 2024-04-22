#!/bin/sh

# Espera hasta que la base de datos esté disponible
while ! nc -z database 5432; do
    echo 'Waiting for PostgreSQL database to become available...'
    sleep 5
done
echo 'Database is available.'

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
