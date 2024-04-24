# Usar la última versión de Ubuntu LTS
FROM ubuntu:22.04

# Evitar que la instalación de paquetes requiera interacción del usuario
ENV DEBIAN_FRONTEND=noninteractive

# Establecer el directorio de trabajo en el contenedor
ENV APP_HOME /app
WORKDIR $APP_HOME

# Establecer variable de entorno para Python
ENV PYTHONUNBUFFERED 1

# Actualizar el índice de paquetes e instalar dependencias de sistema necesarias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    python3.10 \
    python3-pip \
    redis-server \
    netcat-traditional \
    binutils \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    libpq-dev \
    build-essential \
    git

# Enlazar python3 a python (si es necesario)
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

# Añadir la clave GPG del repositorio de PostgreSQL
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Añadir el repositorio de PostgreSQL
RUN add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main"

# Instalar PostgreSQL y PostGIS
RUN apt-get update && apt-get install -y \
    postgresql-14 \
    postgresql-contrib-14 \
    postgis \
    postgresql-14-postgis-3

# Limpiar el cache de apt para reducir tamaño de la imagen
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Añadir y dar permisos al script de inicio
COPY docker/backendInit.sh .
RUN chmod +x backendInit.sh

# Configurar el comando por defecto para ejecutar el script de inicio
CMD ["sh", "docker/backendInit.sh"]