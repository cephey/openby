# coding: utf-8
import os
from ConfigParser import RawConfigParser

PROJECT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

config = RawConfigParser()
config.read(os.path.join(PROJECT_DIR, 'settings.ini'))

########## Версия проекта ##########
CONF = 'development'
# Доступные варианты:
#   development
#   production
####################################

DEBUG = config.get(CONF, 'DEBUG')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Andrey Ptitsyn', 'andrey.ptitsyn86@gmail.com'),
)

MANAGERS = ADMINS

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

ALLOWED_HOSTS = ['*']
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'collected_static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'iig(ve!k3pus-1e+49nuu8vb1ol3$gq$ygr3oq6vm2e$=^oztv'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'conf.urls'

WSGI_APPLICATION = 'conf.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'sekizai.context_processors.sekizai',
    'context_processors.brand',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'sekizai',
    'pages',
    'registration',
    'djangular',
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

# редирект после авторизации в случае 
# если секции 'next' в url нет
LOGIN_REDIRECT_URL = '/profile/'
# количество дней в течении которых 
# можно активировать аккаунт
ACCOUNT_ACTIVATION_DAYS = 2

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
