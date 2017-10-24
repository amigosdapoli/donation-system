from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
	'NAME': os.getenv('RDS_DB_NAME', ''),
        'USER': os.getenv('RDS_USERNAME', ''),
        'PASSWORD': os.getenv('RDS_PASSWORD', ''),
        'HOST': os.getenv('RDS_HOSTNAME', ''),
        'PORT': os.getenv('RDS_PORT', ''),
    }
}