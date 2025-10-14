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
                'django.template.context_processors.debug',
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
    origin for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",") if origin
]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"
CORS_ALLOW_HEADERS = list(default_headers) + ["authorization"]
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "DELETE,GET,OPTIONS,PATCH,POST,PUT").split(",")

# ==== KEYCLOAK CONFIGURATION ====
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "GigBenchmarkRealm")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "gig-api")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET_KEY", "")
KEYCLOAK_PUBLIC_KEY = os.getenv("KEYCLOAK_CLIENT_PUBLIC_KEY", "").replace('\\n', '\n')
KEYCLOAK_ISSUER = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"

# ==== REST FRAMEWORK + JWT (CONFIGURÉ POUR KEYCLOAK) ====
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.keycloak_auth.KeycloakAuthentication',  # classe personnalisée
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
}

# ==== LOGS ====
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'keycloak_file': {
            'class': 'logging.handlers.RotatingFileHandler',  # ✅ Rotation automatique
            'filename': str(LOG_DIR / "keycloak_auth.log"),   # Chemin absolu
            'maxBytes': 1024 * 1024 * 5,  # 5 Mo par fichier
            'backupCount': 5,              # Garde 5 fichiers de backup
            'formatter': 'verbose',
            'level': 'DEBUG',
            'encoding': 'utf8',
        },
        'django_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / "django.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {  # ✅ Logs globaux de Django
            'handlers': ['console', 'django_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {  # ✅ Logs des requêtes (erreurs 4xx/5xx)
            'handlers': ['console', 'django_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'keycloak_auth': {  # ✅ Logs de la librairie django-keycloak-auth
            'handlers': ['console', 'keycloak_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'core.keycloak_auth': {  # ✅ Tes logs custom
            'handlers': ['console', 'keycloak_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
