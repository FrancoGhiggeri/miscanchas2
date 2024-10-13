from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '142.93.49.186',
    'miscanchas.com'
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

STATIC_ROOT = os.path.join(BASE_DIR, "static")
