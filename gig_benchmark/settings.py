# settings.py
from pathlib import Path
from corsheaders.defaults import default_headers
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ==== DJANGO SECRETS ====
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ==== APPLICATIONS ====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',

    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_yasg',
]

# ==== MIDDLEWARE ====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gig_benchmark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gig_benchmark.wsgi.application'

# ==== DATABASE ====
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.mysql"),
        'NAME': os.getenv("DB_NAME", "GIG"),
        'USER': os.getenv("DB_USER", "giguser"),
        'PASSWORD': os.getenv("DB_PASSWORD", "1234"),
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': os.getenv("DB_PORT", "3306"),
        'OPTIONS': eval(os.getenv("DB_OPTIONS", "{}")),
    }
}

# ==== PASSWORD VALIDATORS ====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==== CORS ====
CORS_ALLOWED_ORIGINS = [
    origin for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if origin
]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"
CORS_ALLOW_HEADERS = list(default_headers) + ["authorization"]
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "DELETE,GET,OPTIONS,PATCH,POST,PUT").split(",")

# ==== REST FRAMEWORK + JWT ====
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'core.keycloak_auth.KeycloakAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME", 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME", 1440))),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': os.getenv("JWT_ALGORITHM", "HS256"),
    'SIGNING_KEY': os.getenv("JWT_SECRET_KEY", SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# ==== SWAGGER ====
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'LOGIN_URL': '/api/auth/login/',
    'LOGOUT_URL': '/api/auth/logout/',
}

# ==== KEYCLOAK (optionnel) ====
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
KEYCLOAK_CLIENT_SECRET_KEY = os.getenv("KEYCLOAK_CLIENT_SECRET_KEY", "")
KEYCLOAK_CLIENT_PUBLIC_KEY = os.getenv("KEYCLOAK_CLIENT_PUBLIC_KEY", "")
