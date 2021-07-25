from .base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geoloc',
        'USER': 'geoloc',
        'PASSWORD': 'geoloc',
        'HOST': 'db',
        'PORT': '5432'
    }
}
