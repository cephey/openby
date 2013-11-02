"""
Settings file with settings required to run unittests on the app
This file shouldn't be used for anything besides running unittests on registration
usage:
from root directory for django project, call:
python manage.py test registration --settings=registration.settings.settings
"""
from os.path import abspath, basename, dirname, join, normpath

DJANGO_ROOT = dirname(abspath(__file__))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)

# If using a custom user, uncomment the next line and replace myapp.MyUser with customer user
#AUTH_USER_MODEL = 'myapp.MyUser'

# This isn't terribly important because it is just required to run the tests
SECRET_KEY="thiskeyisntverysecretandshouldntbeusedforanythingbesidestestingtheregistrationapp"

DEBUG = True

SITE_ID = 1
ROOT_URLCONF = 'registration.urls'

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'registration',)


"""
Test settings and globals which allows us to run our test
suite locally.
"""
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'registration/templates')),
)

