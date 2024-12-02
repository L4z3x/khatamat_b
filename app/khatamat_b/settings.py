

from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import django
import os 

# fix issue with rest_framework_jwt using smart_text
from django.utils.encoding import smart_str  
django.utils.encoding.smart_text = smart_str

# fix issue with rest_framework_jwt using ugettecxt
from django.utils.translation import gettext
django.utils.translation.ugettext = gettext
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY") or 'django-insecure-v+9uuo2f##*2g)%)haaia7ut*-d4ei9(!ju%p@&yme&15z#d(o'

DEBUG = os.environ.get("DEBUG") or True

ALLOWED_HOSTS = [host for host in os.environ.get("ALLOWED_HOSTS", "*").split(',')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'daphne',
    'channels',
    'channels_auth_token_middlewares',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Ensure this is included
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'corsheaders',
    'api',
    'notification',
    'community',
    'khatma',
]

REST_FRAMEWORK={
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 10
}

SPECTACULAR_SETTINGS={
    "TITLE":"GHARIB",
    'OPERATION_ID_GENERATOR': 'drf_spectacular.utils.simple_operation_id_generator',
    'SERVE_INCLUDE_SCHEMA': False,
}

SIMPLE_JWT={
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWS_CREDENTIALS = True

CORS_ALLOWED_ORIGINS=[
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'khatamat_b.urls'

# WSGI_APPLICATION = 'khatamat_b.wsgi.application'


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

ASGI_APPLICATION = 'khatamat_b.asgi.application'

AUTH_USER_MODEL  = 'api.MyUser'

POSTGRES_DB = os.environ.get("POSTGRES_DB") or 'khatamat'
POSTGRES_USER = os.environ.get("POSTGRES_USER") or ''
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or ''
POSTGRES_HOST = os.environ.get("POSTGRES_HOST") or 'localhost'
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", '5432') or '5432'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}
    
REDIS_CHANNEL_PORT = os.environ.get("REDIS_CHANNEL_PORT") or '6379'
REDIS_CHANNEL_HOST = os.environ.get("REDIS_CHANNEL_HOST")  or "redis"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_CHANNEL_HOST, REDIS_CHANNEL_PORT)],
        },
    },
}

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "files")
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "amqp://guest:guest@rabbitmq:5672/")

CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")