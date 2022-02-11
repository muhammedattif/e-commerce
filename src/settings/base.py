"""
Django settings for E-Commerce project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import environ
from pathlib import Path
import os
from datetime import timedelta
env = environ.Env()
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'users.backends.CaseInsensitiveModelBackend'
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Allowed hosts
ALLOWED_HOSTS = [env('ALLOWED_HOST')]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django.contrib.sites',
    'rest_framework',
    'django_rest_passwordreset',
    'rest_framework.authtoken',
    'djoser',
    'nested_inline',
    # for scanning from virus
    'django_clamd',
    # this is for CRONJOBS
    'django_crontab',
    # CORS
    'corsheaders',

    #PLUGINS
    'ckeditor',
    'ckeditor_uploader',
    'drf_yasg',
    'django_filters',
    'djmoney',
    #APPS
    'users',
    'vendor',
    'products',
    'payment',
    'categories',
    'orders',
    'gifts'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    #CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]


ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'src.wsgi.application'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}

# Djoser Authentication
SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
   'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
   'REFRESH_TOKEN_LIFETIME': timedelta(hours=5),
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'SERIALIZERS': {
    },
    'EMAIL': {
        'password_reset': 'users.email.PasswordResetEmail',
        'activation': 'users.email.ActivationEmail'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Directory where users uploads are gonna be stored
PROFILE_IMAGES_URL = 'profile_images'

# CK Editor settings
CKEDITOR_UPLOAD_PATH = "products_uploads/"


TAX_AMOUNT = 14.0 # Number in percentage

#Email BACKEND

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_TIMEOUT = env('EMAIL_TIMEOUT') #Time in seconds

# REST_FRAMEWORK Rest Password
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomStringTokenGenerator",
    "OPTIONS": {
        "min_length": 20,
        "max_length": 30
    }
}
DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 1 # Time in hours

FRONT_END_DOMAIN = env('FRONT_END_DOMAIN')
