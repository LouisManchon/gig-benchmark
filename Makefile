.PHONY: help build up down restart logs clean rebuild

help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construit les images Docker
	docker compose build

up: ## Démarre tous les services
	docker compose up -d

down: ## Arrête tous les services
	docker compose down

restart: down up ## Redémarre tous les services

logs: ## Affiche les logs de tous les services
	docker compose logs -f

logs-backend: ## Affiche les logs du backend
	docker compose logs -f backend

logs-celery: ## Affiche les logs des workers Celery
	docker compose logs -f celery-worker celery-beat

logs-scraping: ## Affiche les logs du scraping
	docker compose logs -f scraping

logs-nginx: ## Affiche les logs Nginx
	docker compose logs -f nginx

logs-rabbitmq: ## Affiche les logs RabbitMQ
	docker compose logs -f rabbitmq

ps: ## Liste les services actifs
	docker compose ps

shell-backend: ## Ouvre un shell dans le container backend
	docker compose exec backend /bin/bash

shell-db: ## Ouvre un shell MySQL
	docker compose exec db mysql -u gig_user -p gig_benchmark

migrate: ## Exécute les migrations Django
	docker compose exec backend python manage.py migrate

makemigrations: ## Crée les migrations Django
	docker compose exec backend python manage.py makemigrations

collectstatic: ## Collecte les fichiers statiques Django
	docker compose exec backend python manage.py collectstatic --noinput

createsuperuser: ## Crée un superuser Django
	docker compose exec backend python manage.py createsuperuser

composer-install: ## Installe les dépendances Composer
	docker compose exec php composer install

clean: ## Nettoie les volumes et containers
	docker compose down -v
	docker system prune -f

rebuild: clean build up ## Rebuild complet (attention: supprime les données)

test-backend: ## Lance les tests Django
	docker compose exec backend python manage.py test

check-rabbitmq: ## Vérifie le statut de RabbitMQ
	@echo "RabbitMQ Management UI: http://localhost:15672"
	@echo "User: gig_user | Pass: gig_password"

check-services: ## Vérifie que tous les services sont up
	@echo "=== Vérification des services ==="
	@echo "Backend API: http://localhost:8000/api/"
	@echo "Django Admin: http://localhost:8000/admin/"
	@echo "Frontend: http://localhost:10014"
	@echo "RabbitMQ: http://localhost:15672"
	@docker compose ps

scraping-logs:
	@echo "Affichage des logs du scraping..."
	${DOCKER_COMPOSE} logs -f scraping

scraping-restart:
	@echo "Redémarrage du scraping..."
	${DOCKER_COMPOSE} restart scraping

.PHONY: scraping-test scraping-logs scraping-shell scraping-send-task

scraping-logs:
	@docker compose logs -f scraping

scraping-shell:
	@docker exec -it gig-benchmark-scraping bash

scraping-test:
	@docker exec gig-benchmark-scraping python -c "from src.football.ligue_1 import scrape_ligue_1; print('✅ Import OK')"

scraping-send-ligue1:
	@docker exec gig-benchmark-rabbitmq rabbitmqadmin publish routing_key=scraping_tasks payload='{"scraper":"football.ligue_1"}'
	@echo "📨 Tâche envoyée ! Voir les logs avec: make scraping-logs"
