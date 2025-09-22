FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système pour MySQL et Django
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Créer les dossiers pour les statics/media (déjà présents dans votre arbo)
RUN mkdir -p /app/staticfiles && mkdir -p /app/media

EXPOSE ${BACKEND_PORT}
