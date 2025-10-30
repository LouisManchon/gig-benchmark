#!/bin/bash
set -e

echo "🔄 En attente de MySQL..."
while ! nc -z db 3306; do
  sleep 1
done
echo "✅ MySQL est prêt"

echo "🔄 Application des migrations..."
python manage.py migrate --noinput

echo "🔄 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "🚀 Démarrage de Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
