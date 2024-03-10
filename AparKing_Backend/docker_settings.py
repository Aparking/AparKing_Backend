import os

DEBUG = True
DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': 'aparking_db',
		'USER': 'aparking',
		'PASSWORD': 'aparking',
		'HOST': os.environ.get('DB_HOST', 'database'),
		'PORT': '5432',
	}
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH', '/usr/lib/x86_64-linux-gnu/libgdal.so')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH', '/usr/lib/x86_64-linux-gnu/libgeos_c.so')