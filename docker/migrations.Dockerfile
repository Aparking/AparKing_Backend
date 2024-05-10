FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED 1

# gdal para GeoDjango y libpq-dev para psycopg2
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    binutils \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    libpq-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/migrationsInit.sh .
RUN chmod +x migrationsInit.sh

WORKDIR $APP_HOME

CMD ["sh", "docker/migrationsInit.sh"]
