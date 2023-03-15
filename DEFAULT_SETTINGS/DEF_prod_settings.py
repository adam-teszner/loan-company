import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

'''
This file should be placed in the same folder as settings.py
'''



DEBUG = False

#dbs

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'), 
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': '5432',
    }
}

# static

STATIC_ROOT = 'your/path/static'
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_URL = 'media/'
MEDIA_ROOT = 'your/path/media'

# logs

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER