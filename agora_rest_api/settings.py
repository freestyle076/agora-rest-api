"""
Django settings for agora_rest_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import datetime 
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
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
    'mod_wsgi.server',
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
#Variable storing the last time the cleanup procedure was run
MOST_RECENT_CLEANUP = datetime.date.today() - datetime.timedelta(days=1)

# Number of days Before a Post is Deleted
OLD_POST_CUTTOFF_LENGTH = 31 
# Number of reports that a post will get deleted for
MAX_REPORT_THRESHOLD = 3 


SERVER_ROOT = "147.222.165.3:/home/cpsc04/khandy"

RESOURCE_ROOT = PROJECT_PATH + '/agora_rest_api/resources/'

#Designates location of Image files on server
IMAGES_ROOT = RESOURCE_ROOT + 'images/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


APPLE_USERNAME = 'apple_adm!n'
APPLE_PASS = 'apple_passw0rd'


#Paging Count designates the number of posts that will be sent to the app 
#after each new request for more posts

PAGING_COUNT = 10

TIME_ZONE = 'US/Pacific'


#Categories - This designates what type of post our categories fall into 

item_categories = ['Electronics','Household','Recreation','Clothing']
book_categories = ['Books']
rideshare_categories = ['Ride Shares']
datelocation_categories = ['Services','Events']
