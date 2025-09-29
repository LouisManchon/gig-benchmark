# Variables
DOCKER_COMPOSE = docker compose
DB_SERVICE = db
DB_USER = root
DB_PASSWORD = $(shell grep DB_ROOT_PASSWORD .env | cut -d '=' -f2)
DB_NAME = gig_benchmark

.PHONY: build up down ps logs db-reset db-shell db-show-tables db-show-data

build:
	@echo "Construction des images Docker..."
	${DOCKER_COMPOSE} build

up:
	@echo "Démarrage de tous les services..."
	${DOCKER_COMPOSE} up -d

down:
	@echo "Arrêt de tous les services..."
	${DOCKER_COMPOSE} down

ps:
	@echo "Affichage des conteneurs en cours d'exécution..."
	${DOCKER_COMPOSE} ps

logs:
	@echo "Affichage des logs de tous les services..."
	${DOCKER_COMPOSE} logs -f

db:
	@echo "Connexion à la base de données..."
	${DOCKER_COMPOSE} exec -it ${DB_SERVICE} mysql -u${DB_USER} -p${DB_PASSWORD} ${DB_NAME}

