from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS +=[
    # this for debugging SQL
    'debug_toolbar',
]

MIDDLEWARE += [
    # For debugging
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# This for degugging
INTERNAL_IPS = [
    env('ALLOWED_HOST'),
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + env('DATABASE_ENGINE'),
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': int(env("DATABASE_PORT"))
    }
}


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
'DELETE',
'GET',
'OPTIONS',
'PATCH',
'POST',
'PUT',
]

CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]
