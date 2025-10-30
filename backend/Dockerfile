FROM python:3.9-slim

# Variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    gcc \
    g++ \
    pkg-config \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier et installer les requirements Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Copier et rendre exécutable l'entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Créer les dossiers nécessaires
RUN mkdir -p /app/staticfiles /app/media

# Exposer le port
EXPOSE 8000

# Définir l'entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Commande par défaut (peut être surchargée dans docker-compose)
CMD ["gunicorn", "--config", "gunicorn.conf.py"]
