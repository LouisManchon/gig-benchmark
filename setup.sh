#!/bin/bash

chmod 644 .env
chmod 644 -R backend/
chmod 644 -R frontend/
chmod 644 -R scraping/

docker-compose up -d --build

echo "Running <3"
