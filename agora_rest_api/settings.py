"""
Django settings for agora_rest_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import ldap

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_yx2*)2l9=s-!!kke!xj_p18td#ie^uci@^s0lv&!sor=)hr6a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '*'
]


# Application definition

INSTALLED_APPS = (
    'sslserver',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'agora_rest_api.user_service',
    'agora_rest_api.post_service',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'agora_rest_api.urls'

WSGI_APPLICATION = 'agora_rest_api.wsgi.application'

# REST FRAMEWORK CONFIG
REST_FRAMEWORK = {
    #place rest framework configurations here
    'PAGINATE_BY' : 10
}
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sustainability_app',
        'USER': 'sustainability',
        'PASSWORD' : 'Dh4Pks7.6',
        'HOST': '147.222.165.3',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

SERVER_ROOT = "147.222.165.3:/home/cpsc04/kylehandy"

#MEDIA_ROOT = SERVER_ROOT + '/agora_rest_api/media/'

MEDIA_ROOT = PROJECT_PATH + '/agora_rest_api/media/'

IMAGES_ROOT = MEDIA_ROOT + 'images/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

REPORT_THRESHOLD = 3

APPLE_USERNAME = 'adm!n'

APPLE_PASS = 'passw0rd'