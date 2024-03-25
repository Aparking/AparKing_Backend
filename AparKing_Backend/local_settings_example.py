DEBUG = True
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'aparking_db',
		'USER': 'aparking',
		'PASSWORD': 'aparking',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}

# MacOS
# GDAL_LIBRARY_PATH = '/opt/homebrew/Cellar/gdal/3.8.4/lib/libgdal.dylib'
# GEOS_LIBRARY_PATH = '/opt/homebrew/Cellar/geos/3.12.1/lib/libgeos_c.dylib'