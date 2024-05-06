#!/bin/bash

# Definir el directorio de trabajo de la aplicación
APP_HOME="/app"
mkdir -p $APP_HOME
cd $APP_HOME

# Determinar la distribución del sistema
DISTRIB_ID=$(lsb_release -si)

# Actualizar el sistema
sudo apt-get update

# Comandos específicos de distribución
if [ "$DISTRIB_ID" = "Ubuntu" ]; then
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository ppa:ubuntugis/ppa
elif [ "$DISTRIB_ID" = "Debian" ]; then
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
fi

sudo apt-get update

# Instalar dependencias necesarias para ambas distribuciones
sudo apt-get install -y \
    gdal-bin \
    python3-gdal \
    wget \
    gnupg \
    python3 \
    python3-pip \
    redis-server \
    netcat-traditional \
    binutils \
    libgdal-dev \
    libproj-dev \
    libpq-dev \
    build-essential \
    git \
    postgresql-14-postgis-3

# Limpiar el caché de apt
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

python3 -m venv ./venv
source venv/bin/activate

# Instalar las dependencias de Python
pip3 install --no-cache-dir -r requirements.txt

# Configurar PostgreSQL y Redis
sudo service postgresql start
sudo su - postgres -c "psql -c \"CREATE USER aparking WITH PASSWORD 'aparking';\""
sudo su - postgres -c "psql -c \"CREATE DATABASE aparking_db OWNER aparking;\""
sudo su - postgres -c "psql -d aparking_db -c \"CREATE EXTENSION postgis;\""

# Esperar hasta que PostgreSQL esté disponible
echo 'Waiting for PostgreSQL database to become available...'
while ! nc -z localhost 5432; do
    sleep 1
done
echo 'Database is available.'

# Desactivar Transparent Huge Pages para Redis
echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled

# Iniciar Redis sin contraseña
sudo redis-server --port 6379 --protected-mode no &

# Esperar hasta que Redis esté disponible
echo 'Waiting for Redis to become available...'
while ! nc -z localhost 6379; do
    sleep 1
done
echo 'Redis is available.'

# Ejecutar migraciones y otros comandos de inicio de Django
python3 manage.py makemigrations
python3 manage.py migrate --noinput
python3 importCSV.py

# Cargar datos desde populate.json
echo 'Loading data...'
python3 manage.py loaddata Populate.json

# Iniciar el servidor de Django en modo producción recomendado
echo 'Starting backend...'
#gunicorn --bind 0.0.0.0:3000 myproject.wsgi:application &
daphne -b 0.0.0.0 -p $PORT AparKing_Backend.asgi:application
#python3 manage.py runserver 0.0.0.0:3000 &