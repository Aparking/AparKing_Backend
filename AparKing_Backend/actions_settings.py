DEBUG = True
DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': 'aparking_db',
		'USER': 'aparking',
		'PASSWORD': 'aparking',
		'HOST': 'database',
		'PORT': '5432',
	}
}

GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'
GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so'
