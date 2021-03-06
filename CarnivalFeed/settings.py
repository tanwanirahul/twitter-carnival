"""
Django settings for CarnivalFeed project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'chvc7*0+pif!(gnz31wdk2^o!sp=c43mzdtpui@5^fp@cj12r7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'album'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CarnivalFeed.urls'

WSGI_APPLICATION = 'CarnivalFeed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'album_application',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': 'password'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Makes trailing slash in the api URI optional
TASTYPIE_ALLOW_MISSING_SLASH = True

# We would only be supporting JSON and XMl.
TASTYPIE_DEFAULT_FORMATS = ['xml', 'json']

# Set the twitter OAuth credentials
TWITTER_CREDS = {
    "API_KEY": "CrRB0KEGc1PjMbqfSa7ZhcwET",
    "API_SECRET": "9K0R12WjiUo2Ind1I1VNd8FWDVnHurZyhigpY4ge0UQ8NOdYrQ",
    "ACCESS_TOKEN": "161699092-ascRpkNmq7Gtx1YdZqARsiHsM9bobyBEXVtn3YHW",
    "ACCESS_TOKEN_SECRET": "CsGNwEyfKXJvpTIfkwRgsvIDBsPghuHUkVO8WGP6nPPRD"
}

APP_LABEL = "album"

SEARCH_PARAM = "#carnival"

# Starting twitter id that will used as a base since
# which we will fetch all our updates.
START_MAX_ID = 485727141024509952

# Configure all settings related to smtp and email notifications.
SMTP_CONF = {
    "HOST": 'smtp.gmail.com',
    "PORT": 587,
    "SENDER": "rahul.tanwani@hashedin.com",
    "PASSWORD": "",
    "SUBJECT": "#carnival has {count} photos",
    "MESSAGE": "I'm awesome!",
    "FROM": "Eversnap Hashtag",
    "FROM_EMAIL": "Hashtag@EversnapApp.com",
    "TO": "tanwanirahul@gmail.com",
    "BCC": "davide@geteversnap.com"
}

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

STATICFILES_DIRS = (os.path.join(BASE_DIR, "album/static"),)

STATIC_ROOT = os.path.join(BASE_DIR, "static")

API_ROOT = "api"
API_VERSION = "v1"
