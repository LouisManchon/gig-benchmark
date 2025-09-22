#!/bin/sh

# Attendre que la base de données soit prête
while ! nc -z db 3306; do
  sleep 1
done

# Appliquer les migrations
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Démarrer Gunicorn
exec gunicorn --config gunicorn.conf.py