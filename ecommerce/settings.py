import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

# Load the .env file
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# Load environment variables
SECRET_KEY = env('SECRET_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')

DEBUG = False

# password DB
DB_PASSWORD_YO = env('DB_PASSWORD_YO')

ALLOWED_HOSTS = ['https://urbanaurajewelry.com', 'urbanaurajewelry.com', 'e-commerce-production-3e1c.up.railway.app',
                 'https://e-commerce-production-3e1c.up.railway.app',
                 '2201-2806-2f0-7081-e0b5-3955-aa0d-d525-e40d.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = ['https://urbanaurajewelry.com', 'https://e-commerce-production-3e1c'
                        '.up.railway.app', 'https://2201-2806-2f0-7081-e0b5-3955-aa0d'
                        '-d525-e40d.ngrok-free.app']

# Application definition

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'cart',
    'payment',
    'whitenoise.runserver_nostatic',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': os.environ['DB_PASSWORD_YO'],
        'HOST': 'junction.proxy.rlwy.net',
        'PORT': '20646',

    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = ['static/']

# White noise static stuff
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Add PayPal settings
# Set sandbox to True
PAYPAL_TEST = True

PAYPAL_RECEIVER_EMAIL = 'huandongbusiness@qq.com'

STRIPE_PUBLIC_KEY = "pk_test_51Qc9VtBbLu4XKMtilV67WcRMA4TFTdEpBO0dI" \
                    "8QN2ofcOcIQK9L6oqq7hUmNzq5C8rJRO3amOkCHuN9KSJ3ectXv00FRqSVNGK"
