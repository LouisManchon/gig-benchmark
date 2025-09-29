# settings.py
from pathlib import Path
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

# ATTENTION: en prod, lis ce secret depuis les variables d'environnement
SECRET_KEY = 'django-insecure-d5i7cby6gm21g53c7=fpcdps==1sn&j$zhj1#xk&8&%!gba%0%'

DEBUG = True
ALLOWED_HOSTS = []  # en prod: ["api.mondomaine.com"]

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',             # ton app métier (modèles/logiciel benchmark)

    'rest_framework',   # API Django REST Framework
    'django_filters',
    'corsheaders',      # CORS pour autoriser le front Symfony (autre origine)
    'drf_yasg'          # Documentation Swagger
]

# Middleware (CORS doit être très tôt)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # gère le préflight et les en-têtes CORS
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

# Base de données MySQL (conforme à ton besoin)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'GIG',
        'USER': 'giguser',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validators (par défaut)
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

# Fichiers statiques
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF: Auth par défaut = JWT, tout est protégé
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Utilise uniquement l'authentification JWT
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # (Optionnel en dev pour l'API browsable)
        # 'rest_framework.authentication.SessionAuthentication',
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

# Configuration des origines autorisées pour les requêtes CORS
# Permet au frontend de communiquer avec le backend malgré les restrictions de sécurité
CORS_ALLOWED_ORIGINS = [
    # Origine du frontend Symfony en développement
    "http://localhost:8001",
    # Alias local pour le frontend en développement
    "http://127.0.0.1:8001",

    # Origine du backend Django en développement
    # Utile pour les requêtes internes entre services
    "http://localhost:8000",
    # Alias local pour le backend en développement
    "http://127.0.0.1:8000",
]

CORS_ALLOW_HEADERS = list(default_headers) + ["authorization"]

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
