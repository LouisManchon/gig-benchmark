#!/bin/bash

# =============================================
# Fichier: database/install_db.sh
# Description: Installation automatique de la DB
# Usage: bash database/install_db.sh
# =============================================

set -e  # Arrête le script en cas d'erreur

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Installation GIG Database           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Configuration
DB_NAME="GIG"
DB_USER="gig_user"
DB_PASS="gig_password"
DB_HOST="mysql"  # Nom du service Docker
DB_CONTAINER="gig-benchmark-mysql-1"  # Nom du conteneur Docker

# Fonction pour exécuter une commande SQL
execute_sql() {
    local file=$1
    local description=$2
    
    echo -e "${YELLOW}▶${NC} ${description}..."
    
    if docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS < "$file" 2>/dev/null; then
        echo -e "${GREEN}✔${NC} ${description} - ${GREEN}OK${NC}"
    else
        echo -e "${RED}✖${NC} ${description} - ${RED}ERREUR${NC}"
        exit 1
    fi
    echo ""
}

# Vérifier que Docker est lancé
echo -e "${YELLOW}▶${NC} Vérification de Docker..."
if ! docker ps | grep -q $DB_CONTAINER; then
    echo -e "${RED}✖${NC} Le conteneur MySQL n'est pas démarré"
    echo -e "${YELLOW}ℹ${NC}  Lancer: docker-compose up -d mysql"
    exit 1
fi
echo -e "${GREEN}✔${NC} MySQL est démarré"
echo ""

# Étape 1 : Créer le schéma
execute_sql "database/schema/schema.sql" "Création du schéma"

# Étape 2 : Insérer les sports
execute_sql "database/seeds/01_sports.sql" "Insertion des sports"

# Étape 3 : Insérer les marchés
execute_sql "database/seeds/02_markets.sql" "Insertion des marchés"

# Étape 4 : Insérer les ligues
execute_sql "database/seeds/03_leagues.sql" "Insertion des ligues"

# Étape 5 : Insérer les bookmakers
execute_sql "database/seeds/04_bookmakers.sql" "Insertion des bookmakers"

# Résumé final
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${GREEN}✔ Installation terminée avec succès !${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""
echo "📊 Statistiques de la DB:"
docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS $DB_NAME -e "
SELECT 
    'Sports' as Table_Name, COUNT(*) as Rows FROM Sports
UNION ALL
SELECT 
    'Markets', COUNT(*) FROM MarketNames
UNION ALL
SELECT 
    'Leagues', COUNT(*) FROM Leagues
UNION ALL
SELECT 
    'Bookmakers', COUNT(*) FROM Bookmakers;
" 2>/dev/null

echo ""
echo -e "${YELLOW}Prochaines étapes:${NC}"
echo "  1. cd backend"
echo "  2. python manage.py migrate --fake-initial"
echo "  3. python manage.py createsuperuser"
echo ""