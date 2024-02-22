DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_tu_database',
        'USER': 'tu_usuario_de_postgres',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',  # O la dirección IP del servidor de base de datos si está en otro servidor
        'PORT': '5432',  # El puerto predeterminado es 5432
    }
}
