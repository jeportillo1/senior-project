from .base import * # noqa: F401
import os
import socket

ipv4 = socket.gethostbyname(socket.gethostname())

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#site url for browser test
SITE_URL = 'http://127.0.0.1:8000/'

# ALLOWED_HOSTS = ['*'] # allow all hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', ipv4] # allow all hosts

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {

        # MYSQL server
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DEV_DB_NAME'),
        'USER': os.environ.get('DEV_DB_USER'),
        'PASSWORD': os.environ.get('DEV_DB_PASS'),
        'HOST': os.environ.get('DEV_DB_HOST'),
        'PORT': os.environ.get('DEV_DB_PORT'),
        'TEST': {'NAME' : os.environ.get('TEST_NAME', 'test_django')},
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
