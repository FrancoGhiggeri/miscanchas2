# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^x+ez^cjn%xv@tj9o8!%)68v8e(ub@e*eh8s0n^a0r!_dc_==$'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #'floppyforms',
    'canchas',
    'custom_user',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    'dj_pagination',
    'django_filters',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


SITE_ID = 1

ROOT_URLCONF = 'miscanchas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'allauth.socialaccount.context_processors.socialaccount'
            ],
        },
    },
]

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'kr_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'},
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }}

SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


AUTH_PROFILE_MODULE = 'canchas.UserProfile'


ACCOUNT_ADAPTER = 'canchas.adapter.AccountAdapterCustom'
ACCOUNT_EMAIL_VERIFICATION = 'none'

WSGI_APPLICATION = 'miscanchas.wsgi.application'



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/


LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Cordoba'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_INPUT_FORMATS = ('%H:%M',)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = 'create_profile'
ACCOUNT_LOGOUT_REDIRECT_URL = '/' 
SOCIALACCOUNT_LOGIN_ON_GET=True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'custom_user.EmailUser'
# Configuro para que se pueda usar en simultaneo facebook con el custom user
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# EMAIL_USE_SSL = True
# EMAIL_HOST = 'mail.miscanchas.com'
# EMAIL_HOST_USER = 'no-reply@miscanchas.com'
# EMAIL_HOST_PASSWORD = 'FCM3uLHur99L'
# EMAIL_PORT = 465

EMAIL_HOST = 'mail.socialbits.net'
EMAIL_HOST_USER = 'no-reply@socialbits.net'
EMAIL_HOST_PASSWORD = '?I6q*hN~01bf'
EMAIL_PORT =  26

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = 'emails/' # change this to a proper location



DEFAULT_FROM_EMAIL = 'no-reply@miscanchas.com'

REDACTOR_OPTIONS = {'lang': 'es'}
REDACTOR_UPLOAD = 'uploads/'


MP_CLIENT_ID = '5587780729862654'       # set it in your local_settings.py
MP_CLIENT_SECRET = '3HgbDBUjASx5DiD1Rhy6zF46GAqs6e5A'
MP_SANDBOX_MODE = True

DATE_FORMAT = 'd-m-Y'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

