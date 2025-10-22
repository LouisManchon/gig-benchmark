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
	docker-compose build

build-scrap: ## Construit image du scraping
	docker-compose build scraping

up: ## Démarre tous les services
	docker-compose up -d

down: ## Arrête tous les services
	docker-compose down

restart: down up ## Redémarre

ps: ## Liste les services
	docker-compose ps

clean: ## Nettoie volumes et containers
	docker-compose down -v
	docker system prune -f

cache: # vide cache symfony
	docker-compose exec php php bin/console cache:clear

# ============================================
# LOGS
# ============================================
logs: ## Logs de tous les services
	docker-compose logs -f

logs-backend: ## Logs backend
	docker-compose logs backend -f

logs-scraping: ## Logs scraping
	docker-compose logs scraping -f

logs-consumer: ## Logs consumer
	docker-compose logs consumer_odds -f

logs-rabbitmq: ## Logs RabbitMQ
	docker-compose logs rabbitmq -f

# ============================================
# SHELLS
# ============================================
shell-backend: ## Shell backend
	docker-compose exec backend /bin/bash

shell-scraping: ## Shell scraping
	docker-compose exec scraping /bin/bash

shell-db: ## Shell MySQL interactif
	docker-compose exec db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME)

# ============================================
# DATABASE - SETUP
# ============================================
install-db: ## Installe la BDD complète
	@echo "📦 Installation de $(DB_NAME)..."
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS $(DB_NAME);"
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/schema/schema.sql
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/01_sports.sql
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/02_markets.sql
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/03_leagues.sql
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/04_bookmakers.sql
	@echo "✅ BDD installée avec succès"

reset-db: ## Réinitialise la BDD (⚠️ supprime tout)
	@echo "⚠️  ATTENTION: Suppression de toutes les données !"
	@read -p "Continuer ? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "DROP DATABASE IF EXISTS $(DB_NAME);"
	$(MAKE) install-db

check-db: ## Vérifie la BDD
	docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "SELECT 'Sports' as Table_Name, COUNT(*) as Count FROM Sports UNION ALL SELECT 'Bookmakers', COUNT(*) FROM Bookmakers UNION ALL SELECT 'Matches', COUNT(*) FROM Matches UNION ALL SELECT 'Odds', COUNT(*) FROM Odds;"

# ============================================
# DATABASE - STATS & QUERIES
# ============================================
db-stats: ## 📊 Statistiques générales de la BDD
	@echo "📊 STATISTIQUES GÉNÉRALES"
	@echo "========================="
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    'Sports' as Table_Name, COUNT(*) as Count FROM Sports \
	UNION ALL SELECT 'Ligues', COUNT(*) FROM Leagues \
	UNION ALL SELECT 'Equipes', COUNT(*) FROM Teams \
	UNION ALL SELECT 'Matchs', COUNT(*) FROM Matches \
	UNION ALL SELECT 'Bookmakers', COUNT(*) FROM Bookmakers \
	UNION ALL SELECT 'Cotes', COUNT(*) FROM Odds;"

db-matches: ## 🎮 Liste tous les matchs
	@echo "🎮 MATCHS"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    m.id, \
	    l.name as Ligue, \
	    CONCAT(ht.name, ' - ', at.name) as Rencontre, \
	    DATE_FORMAT(m.match_date, '%Y-%m-%d %H:%i') as Date, \
	    m.status as Statut, \
	    COUNT(DISTINCT o.bookmaker_id) as Nb_Bookmakers \
	FROM Matches m \
	JOIN Leagues l ON m.league_id = l.id \
	JOIN Teams ht ON m.home_team_id = ht.id \
	JOIN Teams at ON m.away_team_id = at.id \
	LEFT JOIN Odds o ON m.id = o.match_id \
	GROUP BY m.id \
	ORDER BY m.match_date;"

db-bookmakers: ## 📚 Liste les bookmakers avec stats
	@echo "📚 BOOKMAKERS"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    b.name as Bookmaker, \
	    COUNT(DISTINCT o.match_id) as Nb_Matchs, \
	    COUNT(o.id) as Nb_Cotes, \
	    ROUND(AVG(o.trj), 2) as TRJ_Moyen, \
	    ROUND(MAX(o.trj), 2) as Meilleur_TRJ \
	FROM Bookmakers b \
	LEFT JOIN Odds o ON b.id = o.bookmaker_id \
	GROUP BY b.id \
	ORDER BY TRJ_Moyen DESC;"

db-odds: ## 💰 Dernières cotes (20 lignes)
	@echo "💰 DERNIÈRES COTES"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    CONCAT(ht.name, ' - ', at.name) as Rencontre, \
	    b.name as Bookmaker, \
	    o.outcome as Issue, \
	    o.odd_value as Cote, \
	    o.trj as TRJ, \
	    DATE_FORMAT(o.scraped_at, '%d/%m %H:%i') as Date \
	FROM Odds o \
	JOIN Matches m ON o.match_id = m.id \
	JOIN Teams ht ON m.home_team_id = ht.id \
	JOIN Teams at ON m.away_team_id = at.id \
	JOIN Bookmakers b ON o.bookmaker_id = b.id \
	ORDER BY o.scraped_at DESC \
	LIMIT 20;"

db-best-trj: ## 🏆 Meilleurs TRJ par match
	@echo "🏆 MEILLEURS TRJ PAR MATCH"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    CONCAT(ht.name, ' - ', at.name) as Rencontre, \
	    b.name as Bookmaker, \
	    ROUND(AVG(o.trj), 2) as TRJ_Moyen, \
	    GROUP_CONCAT(CONCAT(o.outcome, ':', o.odd_value) ORDER BY o.outcome SEPARATOR ' | ') as Cotes \
	FROM Odds o \
	JOIN Matches m ON o.match_id = m.id \
	JOIN Teams ht ON m.home_team_id = ht.id \
	JOIN Teams at ON m.away_team_id = at.id \
	JOIN Bookmakers b ON o.bookmaker_id = b.id \
	GROUP BY m.id, b.id \
	HAVING COUNT(o.id) = 3 \
	ORDER BY TRJ_Moyen DESC \
	LIMIT 10;"

db-teams: ## 👥 Liste les équipes par ligue
	@echo "👥 EQUIPES PAR LIGUE"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    l.name as Ligue, \
	    GROUP_CONCAT(t.name ORDER BY t.name SEPARATOR ', ') as Equipes \
	FROM Teams t \
	JOIN Leagues l ON t.league_id = l.id \
	GROUP BY l.id;"

db-match: ## 🔍 Détails d'un match (usage: make db-match ID=1)
	@if [ -z "$(ID)" ]; then \
		echo "❌ Usage: make db-match ID=1"; \
		exit 1; \
	fi
	@echo "🔍 MATCH #$(ID)"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    b.name as Bookmaker, \
	    MAX(CASE WHEN o.outcome = '1' THEN o.odd_value END) as Cote_1, \
	    MAX(CASE WHEN o.outcome = 'X' THEN o.odd_value END) as Cote_X, \
	    MAX(CASE WHEN o.outcome = '2' THEN o.odd_value END) as Cote_2, \
	    ROUND(AVG(o.trj), 2) as TRJ \
	FROM Odds o \
	JOIN Bookmakers b ON o.bookmaker_id = b.id \
	WHERE o.match_id = $(ID) \
	GROUP BY b.id \
	ORDER BY TRJ DESC;"

db-query: ## 💻 Exécute une requête SQL (usage: make db-query SQL="SELECT * FROM Sports")
	@if [ -z "$(SQL)" ]; then \
		echo "❌ Usage: make db-query SQL=\"SELECT * FROM Sports\""; \
		exit 1; \
	fi
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "$(SQL)"

db-clean-odds: ## 🧹 Supprime toutes les cotes (garde les matchs)
	@echo "⚠️  Suppression de toutes les cotes..."
	@docker compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "TRUNCATE TABLE Odds;"
	@echo "✅ Cotes supprimées"

# ============================================
# SCRAPING
# ============================================

scrape-ligue1: ## 🕷️ Lance scraping Ligue 1
	docker-compose exec scraping python send_task.py football.ligue_1

scrape-serie_a: ## 🕷️ Lance scraping Serie A
	docker-compose exec scraping python send_task.py football.serie_a

scrape-premier_league: ## 🕷️ Lance scraping Premier League
	docker-compose exec scraping python send_task.py football.premier_league

scrape-liga: ## 🕷️ Lance scraping liga
	docker-compose exec scraping python send_task.py football.la_liga

scrape-champions-league: ## 🕷️ Lance scraping champions League
	docker-compose exec scraping python send_task.py football.champions_league
# ============================================
# RABBITMQ
# ============================================
check-rabbitmq: ## 🐰 Vérifie RabbitMQ
	@echo "🐰 RabbitMQ: http://localhost:15672"
	@echo "User: $(RABBITMQ_USER) | Pass: $(RABBITMQ_PASSWORD)"
	@docker-compose exec rabbitmq rabbitmqctl list_queues

rabbitmq-purge: ## 🧹 Vide les queues
	docker-compose exec rabbitmq rabbitmqctl purge_queue odds
	docker-compose exec rabbitmq rabbitmqctl purge_queue scraping_tasks

# ============================================
# HEALTH CHECK
# ============================================
health: ## 🏥 Health check complet
	@echo "🏥 Health Check..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) -e "SELECT 'MySQL OK';" 2>/dev/null && echo "✅ MySQL" || echo "❌ MySQL"
	@docker-compose exec rabbitmq rabbitmqctl status > /dev/null 2>&1 && echo "✅ RabbitMQ" || echo "❌ RabbitMQ"
	@curl -s http://localhost:$(BACKEND_PORT)/admin/ > /dev/null && echo "✅ Backend" || echo "❌ Backend"

# ============================================
# WORKFLOW COMPLET
# ============================================
demo: ## Démo complète (scrape + stats)
	@echo "DÉMO COMPLÈTE"
	@echo "================"
	@echo ""
	@echo "1️Lancement du scraping..."
	$(MAKE) scrape-ligue1
	$(MAKE) scrape-serie_a
	@echo ""
	@sleep 10
	@echo "2 Statistiques:"
	$(MAKE) db-stats
	@echo ""
	@echo "3 Meilleurs TRJ:"
	$(MAKE) db-best-trj