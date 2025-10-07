from .base import *

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