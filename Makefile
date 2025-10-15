# Load .env file
include .env
export

.PHONY: help build up down restart logs clean rebuild

# ============================================
# HELP
# ============================================
help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================
# DOCKER BASICS
# ============================================
build: ## Construit les images Docker
	docker compose build

build-backend: ## Construit les image du backend
	docker compose build --no-cache backend

build-scrap: ## contruit l'image du scraping
	sudo docker compose build --no-cache scraping

up: ## Démarre tous les services
	docker compose up -d

down: ## Arrête tous les services
	docker compose down

restart: down up ## Redémarre tous les services

ps: ## Liste les services actifs
	docker compose ps

clean: ## Nettoie les volumes et containers
	docker compose down -v
	docker system prune -f

rebuild: clean build up ## Rebuild complet (attention: supprime les données)

# ============================================
# LOGS
# ============================================
logs: ## Affiche les logs de tous les services
	docker compose logs -f

logs-backend: ## Affiche les logs du backend
	docker compose logs backend | tail -50

logs-celery: ## Affiche les logs des workers Celery
	docker compose logs celery_worker celery_beat | tail -50

logs-scraping: ## Affiche les logs du scraping
	docker compose logs scraping | tail -50

logs-nginx: ## Affiche les logs Nginx
	docker compose logs nginx | tail -50

logs-rabbitmq: ## Affiche les logs RabbitMQ
	docker compose logs rabbitmq | tail -50

logs-db: ## Affiche les logs MySQL
	docker compose logs db | tail -50

# ============================================
# SHELLS
# ============================================
shell-backend: ## Ouvre un shell dans le container backend
	docker compose exec backend /bin/bash

shell-db: ## Ouvre un shell MySQL
	docker compose exec db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME)

shell-db-root: ## Ouvre un shell MySQL en root
	docker compose exec db mysql -uroot -p$(DB_ROOT_PASSWORD)

shell-scraping: ## Ouvre un shell dans le container scraping
	docker compose exec scraping /bin/bash

shell-php: ## Ouvre un shell dans le container PHP
	docker compose exec php /bin/bash

# ============================================
# DATABASE
# ============================================
# Charger les variables d'environnement
include .env
export

# Installation de la base de données
install-db:
	@echo "Installation de la base de données $(DB_NAME)..."
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS $(DB_NAME);"
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/schema/schema.sql
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/01_sports.sql
	@echo "Base de données installée avec succès"

check-db: ## Vérifie l'état de la base de données
	@echo "📊 Vérification de la base de données $(DB_NAME)..."
	docker compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "SELECT 'Sports' as Table_Name, COUNT(*) as Count FROM Sports UNION ALL SELECT 'Markets', COUNT(*) FROM MarketNames UNION ALL SELECT 'Leagues', COUNT(*) FROM Leagues UNION ALL SELECT 'Bookmakers', COUNT(*) FROM Bookmakers UNION ALL SELECT 'Teams', COUNT(*) FROM Teams UNION ALL SELECT 'Matches', COUNT(*) FROM Matches UNION ALL SELECT 'Odds', COUNT(*) FROM Odds;"

reset-db: ## Réinitialise complètement la base de données
	@echo "⚠️  ATTENTION: Cela va supprimer TOUTES les données de $(DB_NAME) !"
	@read -p "Êtes-vous sûr ? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "DROP DATABASE IF EXISTS $(DB_NAME);"
	$(MAKE) install-db

# ============================================
# DJANGO BACKEND
# ============================================
migrate: ## Exécute les migrations Django
	docker compose exec backend python manage.py migrate

makemigrations: ## Crée les migrations Django
	docker compose exec backend python manage.py makemigrations

collectstatic: ## Collecte les fichiers statiques Django
	docker compose exec backend python manage.py collectstatic --noinput

createsuperuser: ## Crée un superuser Django
	docker compose exec backend python manage.py createsuperuser

test-backend: ## Lance les tests Django
	docker compose exec backend python manage.py test

shell-django: ## Ouvre un shell Django
	docker compose exec backend python manage.py shell

# ============================================
# CONSUMER
# ============================================
start-consumer: ## Démarre le consumer manuellement
	docker compose exec backend python consumers/consumer_odds.py

test-consumer: ## Test le consumer avec un message fictif
	@echo "🧪 Test du consumer..."
	@echo '{"match": "PSG - OM", "bookmaker": "Betclic", "cotes": {"cote_1": 1.85, "cote_N": 3.40, "cote_2": 4.20}, "trj": 91.5, "league": "Ligue 1", "sport": "football"}' | docker compose exec -T rabbitmq rabbitmqadmin publish routing_key=odds payload=-
	@echo "✅ Message envoyé ! Vérifier les logs avec: make logs-backend"

# ============================================
# FRONTEND PHP
# ============================================
composer-install: ## Installe les dépendances Composer
	docker compose exec php composer install

# ============================================
# RABBITMQ
# ============================================
check-rabbitmq: ## Vérifie le statut de RabbitMQ
	@echo "RabbitMQ Management UI: http://localhost:15672"
	@echo "User: $(RABBITMQ_USER) | Pass: $(RABBITMQ_PASSWORD)"
	docker compose exec rabbitmq rabbitmqctl list_queues

rabbitmq-purge: ## Vide toutes les queues RabbitMQ
	docker compose exec rabbitmq rabbitmqctl purge_queue odds
	docker compose exec rabbitmq rabbitmqctl purge_queue scraping_tasks

# ============================================
# SCRAPING
# ============================================
scraping-logs: ## Affiche les logs du scraping
	docker compose logs -f scraping

scraping-restart: ## Redémarre le scraping
	docker compose restart scraping

scraping-test: ## Test le scraper
	docker compose exec scraping python -c "from src.football.ligue_1 import scrape_ligue_1; print('✅ Import OK')"

scraping-send-ligue1: ## Envoie une tâche de scraping Ligue 1
	docker compose exec rabbitmq rabbitmqadmin publish routing_key=scraping_tasks payload='{"scraper":"football.ligue_1"}'
	@echo "📨 Tâche envoyée ! Voir les logs avec: make scraping-logs"

# ============================================
# VERIFICATION GLOBALE
# ============================================
check-services: ## Vérifie que tous les services sont up
	@echo "=== Vérification des services ==="
	@echo "Backend API: http://localhost:$(BACKEND_PORT)/api/"
	@echo "Django Admin: http://localhost:$(BACKEND_PORT)/admin/"
	@echo "Frontend PHP: http://localhost:$(NGINX_PORT)"
	@echo "RabbitMQ: http://localhost:15672"
	@echo ""
	@docker compose ps

health-check: ## Health check complet
	@echo "🏥 Health Check complet..."
	@echo ""
	@echo "1️⃣  Vérification MySQL..."
	@docker compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) -e "SELECT 'MySQL OK' as Status;" 2>/dev/null && echo "✅ MySQL OK" || echo "❌ MySQL FAIL"
	@echo ""
	@echo "2️⃣  Vérification RabbitMQ..."
	@docker compose exec rabbitmq rabbitmqctl status > /dev/null 2>&1 && echo "✅ RabbitMQ OK" || echo "❌ RabbitMQ FAIL"
	@echo ""
	@echo "3️⃣  Vérification Backend..."
	@curl -s http://localhost:$(BACKEND_PORT)/admin/ > /dev/null && echo "✅ Backend OK" || echo "❌ Backend FAIL"
	@echo ""
	@echo "4️⃣  Vérification Frontend..."
	@curl -s http://localhost:$(NGINX_PORT)/ > /dev/null && echo "✅ Frontend OK" || echo "❌ Frontend FAIL"

# ============================================
# INSTALLATION COMPLETE
# ============================================
install: build up install-db migrate createsuperuser composer-install ## Installation complète du projet
	@echo ""
	@echo "✅ Installation terminée !"
	@echo ""
	@echo "📝 Prochaines étapes:"
	@echo "  1. Vérifier les services: make check-services"
	@echo "  2. Accéder à l'admin: http://localhost:$(BACKEND_PORT)/admin"
	@echo "  3. Démarrer le consumer: make start-consumer"
	@echo "  4. Lancer un scraping: make scraping-send-ligue1"