from pathlib import Path
import json
from corsheaders.defaults import default_headers
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ==== LOGS DIRECTORY ====
LOG_DIR = BASE_DIR / "logs"  # ✅ Définition de LOG_DIR
LOG_DIR.mkdir(exist_ok=True)  # ✅ Création du dossier si inexistant

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
    'rest_framework_simplejwt.token_blacklist',
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
    'core.middlewares.AnonymousUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gig_benchmark.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Si tu as un dossier `templates/` à la racine
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  # ⚠️ CRUCIAL POUR KEYCLOAK
                'django.contrib.messages.context_processors.messages',
            ],
            # évite les erreurs de chargement de templates manquant
            'string_if_invalid': 'INVALID_TEMPLATE_VAR: %s',  # ⬅️ Debugging facile
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
        'OPTIONS': json.loads(os.getenv("DB_OPTIONS", '{"charset": "utf8mb4"}')),  # ✅ Sécurisé
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
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8001,http://127.0.0.1:8001").split(",")
    if origin.strip()
]

CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"
CORS_ALLOW_HEADERS = list(default_headers) + ["authorization", "x-csrftoken"]
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "DELETE,GET,OPTIONS,PATCH,POST,PUT").split(",")
CORS_EXPOSE_HEADERS = ["Authorization"]  # ✅ Nouveau: expose le header au frontend

# ==== KEYCLOAK CONFIGURATION ====
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "GigBenchmarkRealm")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "gig-api")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET_KEY", "")


# Chemin vers la clé PEM (fichier externe sécurisé)
KEYCLOAK_PEM_PATH = Path(__file__).resolve().parent / 'keycloak_public_key.pem'

# Charge la clé depuis le fichier (méthode infaillible)
try:
    with open(KEYCLOAK_PEM_PATH, 'r') as f:
        KEYCLOAK_PUBLIC_KEY = f.read().strip()
except FileNotFoundError:
    raise FileNotFoundError(
        f"❌ Fichier de clé Keycloak manquant : {KEYCLOAK_PEM_PATH}. "
        "Créez le fichier 'keycloak_public_key.pem' dans le dossier 'gig_benchmark/'."
    )

# Vérifie que la clé est valide
if not KEYCLOAK_PUBLIC_KEY.startswith("-----BEGIN PUBLIC KEY-----"):
    raise ValueError(
        f"❌ Format de clé invalide dans {KEYCLOAK_PEM_PATH}. "
        "Assurez-vous que le fichier contient une clé PEM valide."
    )


KEYCLOAK_ISSUER = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"

# ==== REST FRAMEWORK ====
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.keycloak_auth.KeycloakAuthentication',  # ✅ Ton backend custom
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # ✅ Par défaut, tout est protégé
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
            'in': 'header',
            'description': 'Enter your Keycloak JWT in the format: **Bearer &lt;token&gt;**',
        }
    },
    'SECURITY_REQUIREMENTS': [
        {'Bearer': []}  # ✅ Applique Bearer à toutes les routes par défaut
    ],
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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / "keycloak_auth.log"),  # ✅ LOG_DIR est maintenant défini
            'maxBytes': 1024 * 1024 * 5,  # 5 Mo
            'backupCount': 5,
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
        'django': {
            'handlers': ['console', 'django_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'django_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'core.keycloak_auth': {  # ✅ Tes logs custom pour Keycloak
            'handlers': ['console', 'keycloak_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
