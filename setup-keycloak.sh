#!/bin/bash

# Télécharger Keycloak si absent
if [ ! -d "keycloak-21.1.1" ]; then
  echo "⬇️ Téléchargement de Keycloak..."
  wget -O /tmp/keycloak.zip https://github.com/keycloak/keycloak/releases/download/21.1.1/keycloak-21.1.1.zip
  unzip /tmp/keycloak.zip -d .
  rm -f /tmp/keycloak.zip
  chmod +x keycloak-21.1.1/bin/kc.sh
fi

# Lancer Keycloak en mode développement (méthode recommandée)
cd keycloak-21.1.1 || exit
export KEYCLOAK_ADMIN=adminfirstone
export KEYCLOAK_ADMIN_PASSWORD=824961
bin/kc.sh start-dev
