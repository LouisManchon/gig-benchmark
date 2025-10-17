#!/bin/sh

# Attend que le backend soit prêt (optionnel)
while ! nc -z backend 8000; do
  sleep 1
done

# Vérifie que le dossier de logs existe et est accessible
mkdir -p /var/www/html/var/logs
chown -R www-data:www-data /var/www/html/var

# Démarre PHP-FPM
exec "$@"
