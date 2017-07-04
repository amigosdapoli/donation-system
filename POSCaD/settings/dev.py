from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
	'NAME': 'poscad',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '',
    }
}
