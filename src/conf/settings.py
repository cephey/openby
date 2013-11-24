#coding:utf-8
import os
from ConfigParser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

config = RawConfigParser()
config.read(os.path.join(BASE_DIR, 'settings.ini'))

########## Версия проекта ##########
CONF = 'development'
# Доступные варианты:
#   development
#   production
####################################

SECRET_KEY = 'cu8@$=0%-$n0r8$!u5!(efeziykiqdjvc1q!%s*-93v*zi^t*^'

DEBUG = config.get(CONF, 'DEBUG')
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sekizai',
    'pages',
    'registration',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'conf.urls'
WSGI_APPLICATION = 'conf.wsgi.application'
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'sekizai.context_processors.sekizai',
    'context_processors.brand',
)


DATABASES = {
    'default': {
        'ENGINE': config.get(CONF, 'DATABASE_ENGINE'),
        'NAME': config.get(CONF, 'DATABASE_NAME'),
        'USER': config.get(CONF, 'DATABASE_USER'),
        'PASSWORD': config.get(CONF, 'DATABASE_PASSWORD'),
        'HOST': config.get(CONF, 'DATABASE_HOST'),
        'PORT': config.get(CONF, 'DATABASE_PORT'),
    }
}

EMAIL_BACKEND = config.get(CONF, 'EMAIL_BACKEND')
EMAIL_HOST = config.get(CONF, 'EMAIL_HOST')
EMAIL_PORT = config.get(CONF, 'EMAIL_PORT')
EMAIL_HOST_USER = config.get(CONF, 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get(CONF, 'EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config.get(CONF, 'EMAIL_USE_TLS')

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'collected_static'),
)

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/var/run/redis/redis.sock'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/var/run/redis/redis.sock:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient'
        },
    }
}

TCT = config.get(CONF, 'CUSTOM_TEMPLATE_CACHE_TIME')

COMPANY_NAME = 'OPENBY'
