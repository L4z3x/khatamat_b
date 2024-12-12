

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

from firebase_admin import credentials, initialize_app  

cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

FIREBASE_APP = initialize_app(cred)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY","django-insecure-v+9uuo2f##*2g)%)haaia7ut*-d4ei9(!ju%p@&yme&15z#d(o")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [host for host in os.environ.get("ALLOWED_HOSTS", "*").split(',')]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWS_CREDENTIALS = True

SITE_ID = 2

PRODUCTION = os.environ.get("PRODUCTION", False)

INSTALLED_APPS = [ 
    'daphne',
    'channels',
    'channels_auth_token_middlewares',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    'django.contrib.sites',
    'allauth',
    'dj_rest_auth.registration',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    'api',
    'notification',
    'community',
    'khatma',
    'fcm_django',
]

# google credentials
GOOGLE_OAUTH_CALLBACK_URL = os.environ.get("GOOGLE_OAUTH_CALLBACK_URL","http://localhost:8000/auth/google/callback/")

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP":{
                "client_id": os.environ.get("GOOGLE_OAUTH_CLIENT_ID",None),
                "secret": os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET",None),
                "key": "",
                },
        "SCOPE": ["profile", "email","openid"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

REST_FRAMEWORK={
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 10
}

REST_USE_JWT = True

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access_token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    'JWT_AUTH_REFRESH_COOKIE_PATH': '/auth/token/get-refresh/',
    'TOKEN_MODEL': None,
    'JWT_AUTH_HTTPONLY':False,  # enable this to allow javascript to access the cookie (refresh token)
    '''
    
    there is a problem with the httponly flag,
    it will associate every request with that cookie
    and that will raise an error in simplejwt, so we need to disable it for now  
    we must not send access_tokens (cookie) in requests to the allowAny endpoints e.g. login
    https://forum.djangoproject.com/t/solved-allowany-override-does-not-work-on-apiview/9754
    
    '''    
    'JWT_AUTH_SECURE': not DEBUG, # False for development
    'JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED': not DEBUG, # False for developement
    'USER_DETAILS_SERIALIZER': 'api.serializers.UserSerializer',

}

SPECTACULAR_SETTINGS={
    '''
     In production, we should secure the docs endpoint by changing the permission class
    from AllowAny to IsAdminUser (cutom permission for site admins). This ensures that only admin users can access the documentation. 
    '''
    
    "TITLE":"khatamat",
    "DESCRIPTION":"khatamat API documentation",
    'OPERATION_ID_GENERATOR': 'drf_spectacular.utils.simple_operation_id_generator',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'], # change to IsAdminUser in prod
    'SERVE_URLCONF': 'khatamat_b.urls',    
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100), # TODO: change to 15 minutes in production
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
    'ROTATE_REFRESH_TOKENS': True, # automatically rotate refresh tokens
    'BLACKLIST_AFTER_ROTATION': True, # old refresh tokens will be blacklisted
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

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
    'allauth.account.middleware.AccountMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB",'khatamat') ,
        'USER': os.environ.get("POSTGRES_USER",None) ,
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD",None),
        'HOST': os.environ.get("POSTGRES_HOST",'localhost') ,
        'PORT': os.environ.get("POSTGRES_PORT", '5432') ,
    }
}
    
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("REDIS_CHANNEL_HOST","redis") , os.environ.get("REDIS_CHANNEL_PORT",'6379') )],
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# allauth settings

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = "email"

# Email settings
EMAIL_USER = os.environ.get("EMAIL_USER", None)
APP_PASSWORD = os.environ.get("APP_PASSWORD", None)



if PRODUCTION == False:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"  # Development
    EMAIL_FILE_PATH = "/app/email_output" # Path to email logs
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # Production
    EMAIL_HOST = "smtp.gmail.com" 
    EMAIL_PORT = 587    
    EMAIL_USE_TLS = True 
    EMAIL_USE_SSL = False 
    EMAIL_HOST_USER = EMAIL_USER
    EMAIL_HOST_PASSWORD = APP_PASSWORD
    DEFAULT_FROM_EMAIL = EMAIL_USER
