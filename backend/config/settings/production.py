from .base import *


# CORS settings

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'corsheaders',  # ✅ Ajoute ça
    'core',
    'services',  # ✅ Ajoute l'app services pour les commandes de scraping
    # ... autres apps
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ Ajoute ça EN PREMIER
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Configuration CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:10014",
    "http://nginx",
]

CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Pour le développement seulement, à restreindre en prod

# ✅ Autorise les credentials
CORS_ALLOW_CREDENTIALS = True

# ✅ Désactive CSRF pour les API (si tu utilises REST Framework)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# ✅ Ajoute les hosts autorisés
ALLOWED_HOSTS = ['*']  # ⚠️ Pour le dev, à restreindre en prod

# Database depuis les variables d'environnement Docker


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'gig_benchmark'),
        'USER': os.getenv('DB_USER', 'gig_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'gig_password'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Sécurité production
SECURE_SSL_REDIRECT = False  # Nginx gère le SSL
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False