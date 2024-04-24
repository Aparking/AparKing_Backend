FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED 1

# Instalar PostgreSQL, PostGIS y otras dependencias
RUN apt-get update && apt-get install -y \
    redis-server \
    netcat-traditional \
    binutils \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    libpq-dev \
    build-essential \
    git \
    postgresql \
    postgresql-contrib \
    postgis \
    postgresql-13-postgis-3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY docker/backendInit.sh .
RUN chmod +x backendInit.sh

CMD ["sh", "docker/backendInit.sh"]