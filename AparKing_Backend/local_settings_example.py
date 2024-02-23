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
