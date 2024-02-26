import configparser
import os
from pathlib import Path


conf = configparser.ConfigParser()

conf_path = '/home/maks/proj/ByteBard/.config'

if os.path.exists(conf_path):
    conf.read(conf_path)
else:
    conf.read('/app/.config')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = conf.get('server', 'secret_key')

DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

INSTALLED_APPS = [
    'daphne',
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',

    'taggit',
    'martor',
    'django_social_share',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'mysite.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': conf.get('database', 'host'),
        'PORT': conf.get('database', 'port'),
        'NAME': conf.get('database', 'name'),
        'USER': conf.get('database', 'user'),
        'PASSWORD': conf.get('database', 'password'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

MARTOR_THEME = 'bootstrap'

MARTOR_IMGUR_CLIENT_ID = conf.get('martor', 'imgur_client_id')
MARTOR_IMGUR_API_KEY = conf.get('martor', 'imgur_api_key')

CSRF_COOKIE_HTTPONLY = False
MARTOR_ENABLE_LABEL = False

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Etc/GMT-2'

USE_I18N = True


USE_TZ = True

STATIC_URL = 'blog/static/'
STATIC_ROOT = 'blog/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = conf.get('email', 'host')
EMAIL_HOST_USER = conf.get('email', 'host_user')
EMAIL_HOST_PASSWORD = conf.get('email', 'host_password')
EMAIL_PORT = conf.get('email', 'port')
EMAIL_USE_TLS = conf.get('email', 'use_tls')

# To write mail in console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
