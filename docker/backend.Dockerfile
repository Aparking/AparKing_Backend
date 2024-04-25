# Usar la última versión de Ubuntu LTS
FROM ubuntu:22.04

# Evitar que la instalación de paquetes requiera interacción del usuario
ENV DEBIAN_FRONTEND=noninteractive

# Establecer el directorio de trabajo en el contenedor
ENV APP_HOME /app
WORKDIR $APP_HOME

# Establecer variable de entorno para Python
ENV PYTHONUNBUFFERED 1

# Instalar software-properties-common antes de añadir el repositorio
RUN apt-get update && \
    apt-get install -y software-properties-common

# Añadir el repositorio de Ubuntugis y actualizar el índice de paquetes
RUN add-apt-repository ppa:ubuntugis/ppa && \
    apt-get update

# Actualizar el índice de paquetes e instalar dependencias de sistema necesarias
RUN apt-get install -y \
    gdal-bin \
    python3-gdal \
    python3-venv \
    wget \
    gnupg \
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
    git \
    postgresql-14-postgis-3

# Limpiar el cache de apt para reducir tamaño de la imagen
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Añadir y dar permisos al script de inicio
COPY docker/backendInit.sh .
RUN chmod +x backendInit.sh

# Configurar el comando por defecto para ejecutar el script de inicio
CMD ["sh", "docker/backendInit.sh"]