from .base import *

DEBUG = False
CSRF_TRUSTED_ORIGINS = [
    'https://miscanchas.com',
    'https://www.miscanchas.com',
    'http://miscanchas.com',
    'https://www.miscanchas.com',
]
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '142.93.49.186',
    'miscanchas.com',
    '143.198.128.207',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'miscanchas2',
        'USER': 'matidb',
        'PASSWORD': 'miscanchas',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = "static-temp/"
