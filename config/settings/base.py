import environ
import json
import os

from datetime import timedelta

ROOT_DIR = environ.Path(__file__) - 3
BASE_DIR = ROOT_DIR
APPS_DIR = ROOT_DIR.path('apps')
DATOS_INICIALES = ROOT_DIR.path('_datos_iniciales')
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.exceptions import ImproperlyConfigured

with open(ROOT_DIR("secrets.json")) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Definir la variable de ambiente {0}".format(setting)
        raise ImproperlyConfigured(error_msg)

ALLOWED_HOSTS = get_secret('DOMINIOS_PROPIOS')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

AUTH_USER_MODEL = 'users.User'

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
#LOGIN_REDIRECT_URL = 'usuarios:login'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
#LOGIN_URL = 'usuarios:login'

SECRET_KEY = get_secret('SECRET_KEY')
DEBUG = get_secret('DEBUG')

LANGUAGE_CODE = 'es'
SITE_ID = 1
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = False
USE_TZ = False

DATE_INPUT_FORMATS = ["%Y-%m-%d",]
DATETIME_FORMAT = "Y-m-d h:i a"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': get_secret('DATABASE_DEFAULT'),
}

#DATABASE_ROUTERS = (
#    'django_tenants.routers.TenantSyncRouter',
#)

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
#ROOT_URLCONF = 'config.urls'
ROOT_URLCONF = 'config.urls'
#PUBLIC_SCHEMA_URLCONF = 'config.public_urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'treebeard',
]
LOCAL_APPS = [
    'apps.users',
    'apps.auth_user',
    'apps.directories',
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS +LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#DJANGO-REST-FRAMEWORK
# ------------------------------------------------------------------------------
# https://www.django-rest-framework.org/#installation
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path('templates')), ],
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

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('../staticfiles'))

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
    str(APPS_DIR.path('media')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_ROOT_TEST = f'{MEDIA_ROOT}/test/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}


# Settings for storage
ROOT_NAME_FOLDER = get_secret('ROOT_NAME_FOLDER')