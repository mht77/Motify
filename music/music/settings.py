import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET', 'django-insecure-57+*+^84c3ubxcklo3s7w+#*19rh9768ow@wx%35_mzmgr!qyx')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    os.environ.get('URL', '127.0.0.1'),
    os.environ.get('WEB', 'localhost:3000'),
    os.environ.get('Socket', '127.0.0.1'),
]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'grpc_services',
    'artist',
    'song',
    'user_player'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music.urls'

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

WSGI_APPLICATION = 'music.wsgi.application'

ASGI_APPLICATION = 'music.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f'redis://:{os.environ.get("REDIS_PASS", "Mohammad@99")}'
                      f'@{os.environ.get("REDIS", "localhost")}:6379/0'],
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://:{os.environ.get("REDIS_PASS", "Mohammad@99")}'
                    f'@{os.environ.get("REDIS", "localhost")}:6379',
        'TIMEOUT': 86400
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME', "music"),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', "postgres123motify"),
        'USER': os.environ.get('POSTGRES_USER', "postgres"),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': 5432
    }
}

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    os.environ.get('WEB', 'http://localhost')
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    os.environ.get('URL', 'http://localhost:3000'),
    os.environ.get('CSRF_WHITELIST', 'http://127.0.0.1:3000'),
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

JWT_ACCESS_EXPIRATION_DELTA = 5
JWT_REFRESH_EXPIRATION_DELTA = 86400

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AZURE_STORAGE_NAME = os.environ.get('AZURE_STORAGE_NAME', 'motifyfiles')

AZURE_STORAGE_CONTAINER = 'songs'

if os.environ.get('Storage') == 'Azure':
    MEDIA_URL = f"https://{AZURE_STORAGE_NAME}.blob.core.windows.net/"
    DEFAULT_FILE_STORAGE = 'music.azure_storage.AzureStorage'
    MEDIA_ROOT = MEDIA_URL + AZURE_STORAGE_CONTAINER
else:
    MEDIA_URL = 'media/'
    # noinspection PyUnresolvedReferences
    MEDIA_ROOT = '../../data/songs/'

GRPC_PORT = os.environ.get('GRPC_PORT', '50062')

GRPC_ADDRESS = os.environ.get('GRPC_ADDRESS', '[::]')

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
