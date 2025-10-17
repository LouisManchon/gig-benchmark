#!/bin/sh

# Attend que RabbitMQ et la base de données soient prêts
while ! nc -z rabbitmq 5672; do
  sleep 1
done

while ! nc -z db 3306; do
  sleep 1
done

# Lance le scraper
exec python src/scraper.py
