"""
Django settings for river_city_pro_wash project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

# import django_heroku
import logging
import os

# Use python-dotenv to manage environment variables
# https://github.com/theskumar/python-dotenv
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_SECONDS = 518400
# SESSION_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv("SECRET_KEY")    # heroku
SECRET_KEY = os.environ["SECRET_KEY"]   # aws


# SECURITY WARNING: don't run with debug turned on in production! -- If you set
# this to FALSE, make sure you have an appropriate allowed site listed in the
# ALLOWED_HOSTS[] array below.

# DEBUG = False
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

# SECURE_SSL_REDIRECT = True
ALLOWED_HOSTS = [
  '*',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web_app.apps.WebAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'river_city_pro_wash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'river_city_pro_wash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Dockerfile database
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'postgres',
#     'USER': 'postgres',
#     'HOST': 'db',
#     'PORT': '5432',
#   }
# }

# Local database
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': os.getenv("POSTGRES_NAME"),
#     'USER': os.getenv("POSTGRES_USER"),
#     'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
#     'HOST': '127.0.0.1',
#     'PORT': '5432',
#   }
# }

# Un-comment this if you want to run python manage.py check --deploy to 2x check
# that security settings are in place before deployment
# DATABASES = {
  # Emptiness goes here
# }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'web_app/static/web_app'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Email settings for Gmail
# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = os.getenv("EMAIL_PORT")
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True

# Activate Django-Heroku
# django_heroku.settings(locals())

# Logging
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'verbose': {
      'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
      'datefmt' : "%d/%b/%Y %H:%M:%S"
    },
    'simple': {
      'format': '%(levelname)s %(message)s'
    },
  },
  'handlers': {
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': 'project.log',
      'formatter': 'verbose'
    },
  },
  'loggers': {
    'django': {
      'handlers':['file'],
      'propagate': True,
      'level':'DEBUG',
    },
    'MYAPP': {
      'handlers': ['file'],
      'level': 'DEBUG',
    },
  }
}