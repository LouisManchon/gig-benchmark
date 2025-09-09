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
    'corsheaders',      # CORS pour autoriser le front Symfony (autre origine)
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

# DRF: Auth par défaut = Keycloak (Bearer JWT), tout est protégé
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oidc_auth.authentication.BearerTokenAuthentication',  # drf-oidc-auth
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# OpenID Connect (Keycloak) — ADAPTE ces valeurs à ton Keycloak
OIDC_AUTH = {
    # URL du realm (issuer), SANS suffixe /protocol/...
    'OIDC_ISSUER': 'https://keycloak.example.com/realms/mon-realm',

    # client_id que Keycloak associe à TON API Django (audience attendue)
    'OIDC_AUDIENCE': 'gig-django-api',

    # Endpoint JWKS pour récupérer les clés publiques (signature RS256)
    'OIDC_JWKS_ENDPOINT': 'https://keycloak.example.com/realms/mon-realm/protocol/openid-connect/certs',

    # Tolérance de dérive d’horloge (secondes)
    'OIDC_LEEWAY': 10,

    # Audiences acceptées (si tu veux être strict)
    'OIDC_ACCEPTED_TOKEN_AUDIENCE': ['gig-django-api'],
    'OIDC_REQUIRE_SIGNATURE': True,
}

# CORS: autorise le front Symfony (ports/domaine à adapter)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",     # ex: front Symfony en dev
    "http://127.0.0.1:8001",
]
# Autoriser le header Authorization pour Bearer <token> si tu customises les headers
CORS_ALLOW_HEADERS = list(default_headers) + ["authorization"]
