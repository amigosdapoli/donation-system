from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
	'NAME': 'admin',
        'USER': 'admin',
        'HOST': 'postgres',
        'PORT': '',
    }
}
