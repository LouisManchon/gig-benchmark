# Load .env file
include .env
export

.PHONY: help build up down restart logs clean

# ============================================
# HELP
# ============================================
help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================
# DOCKER
# ============================================
build: ## Construit les images
	docker compose build

up: ## Démarre tous les services
	docker compose up -d

down: ## Arrête tous les services
	docker compose down

restart: down up ## Redémarre

ps: ## Liste les services
	docker compose ps

clean: ## Nettoie volumes et containers
	docker compose down -v
	docker system prune -f

# ============================================
# LOGS
# ============================================
logs: ## Logs de tous les services
	docker compose logs -f

logs-backend: ## Logs backend
	docker compose logs backend -f

logs-scraping: ## Logs scraping
	docker compose logs scraping -f

logs-consumer: ## Logs consumer
	docker compose logs consumer_odds -f

logs-rabbitmq: ## Logs RabbitMQ
	docker compose logs rabbitmq -f

# ============================================
# SHELLS
# ============================================
shell-backend: ## Shell backend
	docker compose exec backend /bin/bash

shell-scraping: ## Shell scraping
	docker compose exec scraping /bin/bash

shell-db: ## Shell MySQL
	docker compose exec db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME)

# ============================================
# DATABASE
# ============================================
install-db: ## Installe la BDD
	@echo "Installation de $(DB_NAME)..."
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS $(DB_NAME);"
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/schema/schema.sql
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/01_sports.sql
	@echo "✅ BDD installée"

check-db: ## Vérifie la BDD
	docker compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "SELECT 'Sports' as Table_Name, COUNT(*) as Count FROM Sports UNION ALL SELECT 'Bookmakers', COUNT(*) FROM Bookmakers UNION ALL SELECT 'Matches', COUNT(*) FROM Matches UNION ALL SELECT 'Odds', COUNT(*) FROM Odds;"

# ============================================
# SCRAPING
# ============================================
scrape-ligue1: ## Lance scraping Ligue 1
	docker compose exec scraping python send_task.py football.ligue_1

# ============================================
# RABBITMQ
# ============================================
check-rabbitmq: ## Vérifie RabbitMQ
	@echo "🐰 RabbitMQ: http://localhost:15672"
	@echo "User: $(RABBITMQ_USER) | Pass: $(RABBITMQ_PASSWORD)"
	docker compose exec rabbitmq rabbitmqctl list_queues

rabbitmq-purge: ## Vide les queues
	docker compose exec rabbitmq rabbitmqctl purge_queue odds
	docker compose exec rabbitmq rabbitmqctl purge_queue scraping_tasks

# ============================================
# HEALTH CHECK
# ============================================
health: ## Health check complet
	@echo "🏥 Health Check..."
	@docker compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) -e "SELECT 'MySQL OK';" 2>/dev/null && echo "✅ MySQL" || echo "❌ MySQL"
	@docker compose exec rabbitmq rabbitmqctl status > /dev/null 2>&1 && echo "✅ RabbitMQ" || echo "❌ RabbitMQ"
	@curl -s http://localhost:$(BACKEND_PORT)/admin/ > /dev/null && echo "✅ Backend" || echo "❌ Backend"