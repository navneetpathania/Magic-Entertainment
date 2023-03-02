"""
Django settings for magic project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6qhr*^^(4*en*s60od9xzftp4rbrinn%!e&+p+_6l0xx#k0q=d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'user',
    'basepage',
    'subscriptions',
    'djstripe',
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

ROOT_URLCONF = 'magic.urls'

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

WSGI_APPLICATION = 'magic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
MEDIA_ROOT = os.path.join(BASE_DIR,'Media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS  =True
# EMAIL_HOST_USER = os.environ.get("EMAIL")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS")
EMAIL_HOST_USER = 'navneetpathania210@gmail.com'
EMAIL_HOST_PASSWORD = 'yhkiqzlgqwlympvc'


# payment gateway
STRIPE_TEST_PUBLIC_KEY   = 'pk_test_51MZTIYAxauMCkZX5vQxHvQOCM27gWyQ4TVCcYZHiPaIWboC1LV2idza1JB5rysopTJ3a1uemD2VWIiTgcBWjPn9m00sDSuagLo'
STRIPE_TEST_SECRET_KEY  = 'sk_test_51MZTIYAxauMCkZX5KYrLEAKj9xInrKUN2kY0DiH11QMdeW6cS6TwaoERB33Vf8yrOut6PPql6jpHxw18Bjz4p8SD004tsCapAM'
# STRIPE_PLAN_MONTHLY_ID = 'price_1MbXxwAxauMCkZX5cJ4srOhb'
# STRIPE_PLAN_ANNUAL_ID ='price_1MbXxwAxauMCkZX51U2IRxxT'
DJSTRIPE_WEBHOOK_SECRET = "whsec_50c6c42bcab0e104a523b72cb1b5205922a12ee7c5704b466b44c657e7a12bea"
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"