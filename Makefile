include .env
export

.PHONY: help build up down restart logs clean

# ============================================
# HELP
# ============================================
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================
# DOCKER
# ============================================
build: ## Build images
	docker-compose build

build-scrap: ## Build scraping image
	docker-compose build scraping

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: down up ## Restart all services

ps: ## List services
	docker-compose ps

clean: ## Clean volumes and containers
	docker-compose down -v
	docker system prune -f
	@echo "Cleaning Python cache..."
	@find ./backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find ./backend -type f -name "*.pyc" -delete 2>/dev/null || true
	@find ./backend -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Python cache cleaned"

cache: ## Clear symfony cache
	docker-compose exec php php bin/console cache:clear

# ============================================
# MIGRATIONS
# ============================================
makemigrations: ## Create Django migrations
	docker-compose exec backend python manage.py makemigrations

migrate: ## Apply migrations
	docker-compose exec backend python manage.py migrate

migrate-fresh: ## Reset and recreate all migrations
	@echo "WARNING: This will delete all migration files and recreate them"
	@echo "This will also delete all data in the database!"
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "Removing old migration files..."
	@find backend/core/migrations -name "*.py" ! -name "__init__.py" -delete
	@echo "Stopping containers..."
	$(MAKE) down
	@echo "Removing database volume..."
	@docker volume rm gig-benchmark_db_data || true
	@echo "Starting services..."
	$(MAKE) up
	@echo "Waiting for database..."
	@sleep 30
	@echo "Creating new migrations..."
	@docker-compose exec backend python manage.py makemigrations
	@echo "Applying migrations..."
	@docker-compose exec backend python manage.py migrate
	@echo "Loading seeds..."
	$(MAKE) seed-all
	@echo "Migration reset complete!"

migrate-update: ## Update migrations (create and apply new ones)
	@echo "Creating new migrations..."
	@docker-compose exec backend python manage.py makemigrations
	@echo "Applying migrations..."
	@docker-compose exec backend python manage.py migrate
	@echo "Migrations updated successfully!"

migrate-fake: ## Mark migrations as applied
	docker-compose exec backend python manage.py migrate --fake

showmigrations: ## Show migrations
	docker-compose exec backend python manage.py showmigrations

# ============================================
# SEEDS
# ============================================
seed-all: ## Insert all reference data
	@echo "Inserting seeds..."
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/01_sports.sql
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/02_markets.sql
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/03_leagues.sql
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/04_bookmakers.sql
	@echo "Seeds inserted successfully"

seed-sports: ## Insert sports
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/01_sports.sql

seed-markets: ## Insert markets
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/02_markets.sql

seed-leagues: ## Insert leagues
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/03_leagues.sql

seed-bookmakers: ## Insert bookmakers
	docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME) < database/seeds/04_bookmakers.sql

# ============================================
# SEEDS MANAGEMENT
# ============================================
seed-status: ## Show seeds status
	@echo "Seeds status in database:"
	@echo "----------------------------------------"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT \
	    'Sports' as Seed, \
	    COUNT(*) as Count, \
	    CASE WHEN COUNT(*) > 0 THEN 'APPLIED' ELSE 'PENDING' END as Status \
	FROM Sports \
	UNION ALL \
	SELECT \
	    'Markets', \
	    COUNT(*), \
	    CASE WHEN COUNT(*) > 0 THEN 'APPLIED' ELSE 'PENDING' END \
	FROM MarketNames \
	UNION ALL \
	SELECT \
	    'Leagues', \
	    COUNT(*), \
	    CASE WHEN COUNT(*) > 0 THEN 'APPLIED' ELSE 'PENDING' END \
	FROM Leagues \
	UNION ALL \
	SELECT \
	    'Bookmakers', \
	    COUNT(*), \
	    CASE WHEN COUNT(*) > 0 THEN 'APPLIED' ELSE 'PENDING' END \
	FROM Bookmakers;" 2>/dev/null || echo "Error: Database not accessible"

seed-check: ## Check if seeds are needed
	@echo "Checking seeds..."
	@SPORTS=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM Sports" 2>/dev/null); \
	MARKETS=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM MarketNames" 2>/dev/null); \
	LEAGUES=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM Leagues" 2>/dev/null); \
	BOOKMAKERS=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM Bookmakers" 2>/dev/null); \
	if [ "$$SPORTS" = "0" ] || [ "$$MARKETS" = "0" ] || [ "$$LEAGUES" = "0" ] || [ "$$BOOKMAKERS" = "0" ]; then \
		echo "Missing seeds detected. Run 'make seed-apply'"; \
		exit 1; \
	else \
		echo "All seeds are applied"; \
	fi

seed-apply: ## Apply all missing seeds
	@echo "Applying seeds..."
	@SPORTS=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM Sports" 2>/dev/null); \
	if [ "$$SPORTS" = "0" ]; then \
		echo "Applying: 01_sports.sql"; \
		docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/01_sports.sql; \
	else \
		echo "Skip: 01_sports.sql (already applied)"; \
	fi
	@MARKETS=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM MarketNames" 2>/dev/null); \
	if [ "$$MARKETS" = "0" ]; then \
		echo "Applying: 02_markets.sql"; \
		docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/02_markets.sql; \
	else \
		echo "Skip: 02_markets.sql (already applied)"; \
	fi
	@LEAGUES=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM Leagues" 2>/dev/null); \
	if [ "$$LEAGUES" = "0" ]; then \
		echo "Applying: 03_leagues.sql"; \
		docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/03_leagues.sql; \
	else \
		echo "Skip: 03_leagues.sql (already applied)"; \
	fi
	@BOOKMAKERS=$$(docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -sN -e "SELECT COUNT(*) FROM Bookmakers" 2>/dev/null); \
	if [ "$$BOOKMAKERS" = "0" ]; then \
		echo "Applying: 04_bookmakers.sql"; \
		docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/04_bookmakers.sql; \
	else \
		echo "Skip: 04_bookmakers.sql (already applied)"; \
	fi
	@echo "Seeds applied successfully"

seed-force: ## Force reapply all seeds
	@echo "WARNING: This operation will DELETE all reference data"
	@echo "Existing odds will be preserved"
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "Deleting reference data..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SET FOREIGN_KEY_CHECKS=0; \
	TRUNCATE TABLE Bookmakers; \
	TRUNCATE TABLE Leagues; \
	TRUNCATE TABLE MarketNames; \
	TRUNCATE TABLE Sports; \
	SET FOREIGN_KEY_CHECKS=1;"
	@echo "Reapplying seeds..."
	$(MAKE) seed-all

seed-refresh: ## Update seeds without deleting
	@echo "Updating seeds..."
	@echo "Sports..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/01_sports.sql
	@echo "Markets..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/02_markets.sql
	@echo "Leagues..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/03_leagues.sql
	@echo "Bookmakers..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/seeds/04_bookmakers.sql
	@echo "Seeds updated successfully"

seed-validate: ## Validate seeds integrity
	@echo "Validating seeds integrity..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT 'Verification des Sports' as Test; \
	SELECT CASE WHEN COUNT(*) >= 4 THEN 'PASS' ELSE 'FAIL' END as Status, \
	       COUNT(*) as Expected_Min_4 \
	FROM Sports; \
	SELECT 'Verification des Markets' as Test; \
	SELECT CASE WHEN COUNT(*) >= 20 THEN 'PASS' ELSE 'FAIL' END as Status, \
	       COUNT(*) as Expected_Min_20 \
	FROM MarketNames; \
	SELECT 'Verification des Leagues' as Test; \
	SELECT CASE WHEN COUNT(*) >= 20 THEN 'PASS' ELSE 'FAIL' END as Status, \
	       COUNT(*) as Expected_Min_20 \
	FROM Leagues; \
	SELECT 'Verification des Bookmakers' as Test; \
	SELECT CASE WHEN COUNT(*) >= 15 THEN 'PASS' ELSE 'FAIL' END as Status, \
	       COUNT(*) as Expected_Min_15 \
	FROM Bookmakers;"
	
# ============================================
# LOGS
# ============================================
logs: ## Logs from all services
	docker-compose logs -f

logs-backend: ## Backend logs
	docker-compose logs backend -f

logs-scraping: ## Scraping logs
	docker-compose logs scraping -f

logs-consumer: ## Consumer logs
	docker-compose logs consumer_odds -f

logs-celery-worker: ## Celery worker logs
	docker-compose logs celery_worker --tail=50 -f

logs-celery-beat: ## Celery beat logs
	docker-compose logs celery_beat --tail=50 -f

logs-celery: ## Celery worker and beat logs
	docker-compose logs celery_worker celery_beat -f

logs-rabbitmq: ## RabbitMQ logs
	docker-compose logs rabbitmq -f

logs-all: ## Logs from all services
	docker-compose logs -f --tail=50

logs-front-symfony:
	sudo docker-compose exec php tail -50 /var/www/html/var/log/dev.log

logs-front-php:
	sudo docker-compose logs php --tail=30
# ============================================
# SHELLS
# ============================================
shell-backend: ## Backend shell
	docker-compose exec backend /bin/bash

shell-scraping: ## Scraping shell
	docker-compose exec scraping /bin/bash

shell-db: ## MySQL shell
	docker-compose exec db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME)

shell-db-root: ## MySQL shell root
	docker-compose exec db mysql -uroot -p$(DB_ROOT_PASSWORD) $(DB_NAME)

shell-python: ## Python Django shell
	docker-compose exec backend python manage.py shell

# ============================================
# DATABASE - SETUP
# ============================================
install-db: ## Install complete database
	@echo "Installing database..."
	@echo "Checking if database container is running..."
	@docker-compose ps db | grep -q "Up" || (echo "Error: Database container is not running. Please run 'make up' first." && exit 1)
	@echo "Waiting for database to be ready..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		if docker-compose exec -T db mysqladmin ping -h localhost -u$(DB_USER) -p$(DB_PASSWORD) 2>/dev/null | grep -q "mysqld is alive"; then \
			echo "Database is ready!"; \
			break; \
		else \
			echo "Waiting for database... ($$i/10)"; \
			sleep 3; \
		fi; \
	done
	@echo "Creating database and granting privileges..."
	@docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS $(DB_NAME);" 2>/dev/null || true
	@docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "GRANT ALL PRIVILEGES ON $(DB_NAME).* TO '$(DB_USER)'@'%';" 2>/dev/null || true
	@docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "FLUSH PRIVILEGES;" 2>/dev/null || true
	@echo "Applying migrations..."
	@docker-compose ps backend | grep -q "Up" || (echo "Error: Backend container is not running. Please run 'make up' first." && exit 1)
	@echo "Note: Migrations are already applied by backend container on startup"
	@echo "If you need to create new migrations, use 'make makemigrations'"
	@echo "Loading seeds..."
	$(MAKE) seed-all
	@echo "Database installed successfully"

reset-db: ## Reset database
	@echo "WARNING: Deleting all data!"
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose down
	docker volume rm gig-benchmark_db_data || true
	docker-compose up -d db
	@echo "Waiting for database..."
	@sleep 20
	docker-compose up -d
	@sleep 10
	$(MAKE) install-db

check-db: ## Check database
	docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT 'Sports' as Table_Name, COUNT(*) as Count FROM Sports \
	UNION ALL SELECT 'Bookmakers', COUNT(*) FROM Bookmakers \
	UNION ALL SELECT 'Matches', COUNT(*) FROM Matches \
	UNION ALL SELECT 'Odds', COUNT(*) FROM Odds;"

# ============================================
# DATABASE - STATS
# ============================================
db-stats: ## General statistics
	@echo "Database statistics"
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT 'Sports' as Table_Name, COUNT(*) as Count FROM Sports \
	UNION ALL SELECT 'Ligues', COUNT(*) FROM Leagues \
	UNION ALL SELECT 'Equipes', COUNT(*) FROM Teams \
	UNION ALL SELECT 'Matchs', COUNT(*) FROM Matches \
	UNION ALL SELECT 'Bookmakers', COUNT(*) FROM Bookmakers \
	UNION ALL SELECT 'Cotes', COUNT(*) FROM Odds;"

db-matches: ## List all matches
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT m.id, l.name as Ligue, CONCAT(ht.name, ' - ', at.name) as Rencontre, \
	DATE_FORMAT(m.match_date, '%Y-%m-%d %H:%i') as Date, m.status as Statut, \
	COUNT(DISTINCT o.bookmaker_id) as Nb_Bookmakers \
	FROM Matches m \
	JOIN Leagues l ON m.league_id = l.id \
	JOIN Teams ht ON m.home_team_id = ht.id \
	JOIN Teams at ON m.away_team_id = at.id \
	LEFT JOIN Odds o ON m.id = o.match_id \
	GROUP BY m.id ORDER BY m.match_date;"

db-bookmakers: ## List bookmakers with stats
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT b.name as Bookmaker, COUNT(DISTINCT o.match_id) as Nb_Matchs, \
	COUNT(o.id) as Nb_Cotes, ROUND(AVG(o.trj), 2) as TRJ_Moyen, \
	ROUND(MAX(o.trj), 2) as Meilleur_TRJ \
	FROM Bookmakers b LEFT JOIN Odds o ON b.id = o.bookmaker_id \
	GROUP BY b.id ORDER BY TRJ_Moyen DESC;"

db-odds: ## Latest odds
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT CONCAT(ht.name, ' - ', at.name) as Rencontre, b.name as Bookmaker, \
	o.outcome as Issue, o.odd_value as Cote, o.trj as TRJ, \
	DATE_FORMAT(o.scraped_at, '%d/%m %H:%i') as Date \
	FROM Odds o \
	JOIN Matches m ON o.match_id = m.id \
	JOIN Teams ht ON m.home_team_id = ht.id \
	JOIN Teams at ON m.away_team_id = at.id \
	JOIN Bookmakers b ON o.bookmaker_id = b.id \
	ORDER BY o.scraped_at DESC LIMIT 20;"

db-best-trj: ## Best TRJ per match
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "\
	SELECT CONCAT(ht.name, ' - ', at.name) as Rencontre, b.name as Bookmaker, \
	ROUND(AVG(o.trj), 2) as TRJ_Moyen, \
	GROUP_CONCAT(CONCAT(o.outcome, ':', o.odd_value) ORDER BY o.outcome SEPARATOR ' | ') as Cotes \
	FROM Odds o \
	JOIN Matches m ON o.match_id = m.id \
	JOIN Teams ht ON m.home_team_id = ht.id \
	JOIN Teams at ON m.away_team_id = at.id \
	JOIN Bookmakers b ON o.bookmaker_id = b.id \
	GROUP BY m.id, b.id \
	HAVING COUNT(o.id) = 3 \
	ORDER BY TRJ_Moyen DESC LIMIT 10;"

db-clean-odds: ## Delete all odds
	@echo "Deleting all odds..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "TRUNCATE TABLE Odds;"
	@echo "Odds deleted"

db-query: ## Execute SQL query (usage: make db-query SQL="SELECT * FROM Sports")
	@if [ -z "$(SQL)" ]; then echo "Usage: make db-query SQL=\"SELECT * FROM Sports\""; exit 1; fi
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "$(SQL)"

# ============================================
# SCRAPING - MANUAL (212 available scrapers)
# ============================================

# --- FOOTBALL (105 competitions) ---
scrape-ligue1: ## Launch scraping Ligue 1
	docker-compose exec backend python manage.py scrape football.ligue_1

scrape-ligue2: ## Launch scraping Ligue 2
	docker-compose exec backend python manage.py scrape football.ligue_2

scrape-coupe-france: ## Launch scraping Coupe de France
	docker-compose exec backend python manage.py scrape football.coupe_de_france

scrape-serie-a: ## Launch scraping Serie A
	docker-compose exec backend python manage.py scrape football.serie_a

scrape-premier-league: ## Launch scraping Premier League
	docker-compose exec backend python manage.py scrape football.premier_league

scrape-la-liga: ## Launch scraping La Liga
	docker-compose exec backend python manage.py scrape football.la_liga

scrape-bundesliga: ## Launch scraping Bundesliga
	docker-compose exec backend python manage.py scrape football.bundesliga

scrape-champions-league: ## Launch scraping Champions League
	docker-compose exec backend python manage.py scrape football.champions_league

scrape-europa-league: ## Launch scraping Europa League
	docker-compose exec backend python manage.py scrape football.ligue_europa

scrape-conference-league: ## Launch scraping Conference League
	docker-compose exec backend python manage.py scrape football.uefa_conference_league

# --- TENNIS (89 tournaments) ---
scrape-atp-miami: ## Launch scraping ATP Miami
	docker-compose exec backend python manage.py scrape tennis.atp_miami

scrape-wta-miami: ## Launch scraping WTA Miami
	docker-compose exec backend python manage.py scrape tennis.wta_miami

scrape-roland-garros: ## Launch scraping Roland Garros (H+F)
	docker-compose exec backend python manage.py scrape tennis.roland_garros_m
	docker-compose exec backend python manage.py scrape tennis.roland_garros_w

scrape-wimbledon: ## Launch scraping Wimbledon (H+F)
	docker-compose exec backend python manage.py scrape tennis.atp_wimbledon
	docker-compose exec backend python manage.py scrape tennis.wta_wimbledon

scrape-us-open: ## Launch scraping US Open (H+F)
	docker-compose exec backend python manage.py scrape tennis.atp_us_open
	docker-compose exec backend python manage.py scrape tennis.wta_us_open

# --- BASKETBALL (15 leagues) ---
scrape-nba: ## Launch scraping NBA
	docker-compose exec backend python manage.py scrape basketball.nba

scrape-euroleague: ## Launch scraping Euroleague
	docker-compose exec backend python manage.py scrape basketball.euroligue

scrape-betclic-elite: ## Launch scraping Betclic Elite
	docker-compose exec backend python manage.py scrape basketball.betclic_elite

# --- RUGBY (3 competitions) ---
scrape-top14: ## Launch scraping Top 14
	docker-compose exec backend python manage.py scrape rugby.top_14

scrape-pro-d2: ## Launch scraping Pro D2
	docker-compose exec backend python manage.py scrape rugby.pro_d2

# --- SCRAPING BY SPORT ---
scrape-all-football: ## Launch scraping all 105 football competitions
	@echo "Scraping all football competitions (105 total)..."
	@for file in $$(find scraping/src/football -name "*.py" ! -name "__init__.py" ! -name "_scraper_utils.py" | sed 's|scraping/src/football/||' | sed 's|.py||' | sort); do \
		echo "Scraping football.$$file..."; \
		docker-compose exec backend python manage.py scrape football.$$file; \
		sleep 2; \
	done

scrape-all-tennis: ## Launch scraping all 89 tennis tournaments
	@echo "Scraping all tennis tournaments (89 total)..."
	@for file in $$(find scraping/src/tennis -name "*.py" ! -name "__init__.py" ! -name "_scraper_utils.py" | sed 's|scraping/src/tennis/||' | sed 's|.py||' | sort); do \
		echo "Scraping tennis.$$file..."; \
		docker-compose exec backend python manage.py scrape tennis.$$file; \
		sleep 2; \
	done

scrape-all-basketball: ## Launch scraping all 15 basketball leagues
	@echo "Scraping all basketball leagues (15 total)..."
	@for file in $$(find scraping/src/basketball -name "*.py" ! -name "__init__.py" ! -name "_scraper_utils.py" | sed 's|scraping/src/basketball/||' | sed 's|.py||' | sort); do \
		echo "Scraping basketball.$$file..."; \
		docker-compose exec backend python manage.py scrape basketball.$$file; \
		sleep 2; \
	done

scrape-all-rugby: ## Launch scraping all 3 rugby competitions
	@echo "Scraping all rugby competitions (3 total)..."
	@for file in $$(find scraping/src/rugby -name "*.py" ! -name "__init__.py" ! -name "_scraper_utils.py" | sed 's|scraping/src/rugby/||' | sed 's|.py||' | sort); do \
		echo "Scraping rugby.$$file..."; \
		docker-compose exec backend python manage.py scrape rugby.$$file; \
		sleep 2; \
	done

scrape-all: ## Launch scraping of ALL 212 competitions
	@echo "WARNING: This will launch 212 scrapers (may take several hours)"
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	$(MAKE) scrape-all-football
	$(MAKE) scrape-all-tennis
	$(MAKE) scrape-all-basketball
	$(MAKE) scrape-all-rugby

# --- SCRAPING CUSTOM ---
scrape: ## Scrape specific competition (usage: make scrape LEAGUE=football.ligue_1)
	@if [ -z "$(LEAGUE)" ]; then echo "Usage: make scrape LEAGUE=football.ligue_1"; exit 1; fi
	docker-compose exec backend python manage.py scrape $(LEAGUE)

scrape-list: ## List all available scrapers (212 total)
	@echo "Available scrapers (212 total):"
	@echo ""
	@echo "FOOTBALL (105):"
	@echo "  football.ligue_1, football.ligue_2, football.premier_league, football.la_liga,"
	@echo "  football.serie_a, football.bundesliga, football.champions_league, ..."
	@echo ""
	@echo "TENNIS (89):"
	@echo "  tennis.atp_miami, tennis.wta_miami, tennis.roland_garros_m, tennis.atp_wimbledon, ..."
	@echo ""
	@echo "BASKETBALL (15):"
	@echo "  basketball.nba, basketball.euroligue, basketball.betclic_elite, ..."
	@echo ""
	@echo "RUGBY (3):"
	@echo "  rugby.top_14, rugby.pro_d2, rugby.test_match"
	@echo ""
	@echo "Usage: make scrape LEAGUE=<scraper_key>"

# ============================================
# RABBITMQ
# ============================================
check-rabbitmq: ## Check RabbitMQ
	@echo "RabbitMQ Management: http://localhost:15672"
	@echo "User: $(RABBITMQ_USER) | Pass: $(RABBITMQ_PASSWORD)"
	@docker-compose exec rabbitmq rabbitmqctl list_queues

rabbitmq-purge: ## Purge queues
	docker-compose exec rabbitmq rabbitmqctl purge_queue odds
	docker-compose exec rabbitmq rabbitmqctl purge_queue scraping_tasks

# ============================================
# HEALTH CHECK
# ============================================
health: ## Complete health check
	@echo "Health check..."
	@docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) -e "SELECT 'MySQL OK';" 2>/dev/null && echo "MySQL: OK" || echo "MySQL: ERROR"
	@docker-compose exec rabbitmq rabbitmqctl status > /dev/null 2>&1 && echo "RabbitMQ: OK" || echo "RabbitMQ: ERROR"
	@curl -s http://localhost:$(BACKEND_PORT)/api/scraping/health > /dev/null && echo "Backend: OK" || echo "Backend: ERROR"

# ============================================
# COMPLETE WORKFLOW
# ============================================
install: ## Complete project installation (for first time setup)
	@echo "============================================"
	@echo "GIG BENCHMARK - INSTALLATION"
	@echo "============================================"
	@echo "1/6 - Building Docker images..."
	$(MAKE) build
	@echo ""
	@echo "2/6 - Starting services..."
	$(MAKE) up || (echo "First start failed, retrying..." && sleep 5 && $(MAKE) up)
	@echo ""
	@echo "3/6 - Waiting for services to be ready..."
	@sleep 10
	@echo "Checking database health..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		if docker-compose exec -T db mysqladmin ping -h localhost -u$(DB_USER) -p$(DB_PASSWORD) 2>/dev/null | grep -q "mysqld is alive"; then \
			echo "Database is ready!"; \
			break; \
		else \
			echo "Waiting for database... ($$i/10)"; \
			sleep 3; \
		fi; \
	done
	@echo "Checking backend health..."
	@for i in 1 2 3 4 5; do \
		if docker-compose ps backend | grep -q "Up"; then \
			echo "Backend is ready!"; \
			break; \
		else \
			echo "Waiting for backend... ($$i/5)"; \
			sleep 3; \
		fi; \
	done
	@echo ""
	@echo "4/6 - Setting up database..."
	@docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS $(DB_NAME);" 2>/dev/null || true
	@docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "GRANT ALL PRIVILEGES ON $(DB_NAME).* TO '$(DB_USER)'@'%';" 2>/dev/null || true
	@docker-compose exec -T db mysql -uroot -p$(DB_ROOT_PASSWORD) -e "FLUSH PRIVILEGES;" 2>/dev/null || true
	@echo ""
	@echo "5/6 - Creating and applying migrations..."
	@echo "Note: Migrations are already applied by backend container on startup"
	@echo "Waiting for migrations to complete..."
	@sleep 5
	@echo "Verifying migration status..."
	@docker-compose exec backend python manage.py showmigrations || true
	@echo ""
	@echo "6/6 - Loading reference data (sports, leagues, bookmakers, markets)..."
	@echo "Waiting for tables to be ready..."
	@for i in 1 2 3 4 5; do \
		if docker-compose exec -T db mysql -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) -e "SHOW TABLES LIKE 'Sports';" 2>/dev/null | grep -q "Sports"; then \
			echo "Tables are ready!"; \
			break; \
		else \
			echo "Waiting for tables... ($$i/5)"; \
			sleep 3; \
		fi; \
	done
	$(MAKE) seed-all
	@echo ""
	@echo "============================================"
	@echo "INSTALLATION COMPLETE!"
	@echo "============================================"
	@echo "Services available:"
	@echo "  - Backend API: http://localhost:$(BACKEND_PORT)"
	@echo "  - Frontend: http://localhost:10014"
	@echo "  - RabbitMQ Management: http://localhost:15672"
	@echo "  - PhpMyAdmin (if enabled): http://localhost:8080"
	@echo ""
	@echo "Useful commands:"
	@echo "  make status          - Show system status"
	@echo "  make health          - Health check"
	@echo "  make scrape-ligue1   - Test scraping"
	@echo "  make help            - Show all commands"
	@echo "============================================"

init: ## Complete project initialization (alias for install)
	$(MAKE) install

reinstall: ## Reinstall from scratch (delete all data)
	@echo "WARNING: This will delete ALL data (database, volumes, etc.)"
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "Cleaning all containers and volumes..."
	$(MAKE) clean
	@echo ""
	@echo "Starting fresh installation..."
	@echo ""
	$(MAKE) install

demo: ## Complete demo
	@echo "Complete demo"
	@echo "1. Launching scraping..."
	$(MAKE) scrape-ligue1
	@sleep 30
	@echo "2. Statistics:"
	$(MAKE) db-stats
	@echo "3. Best TRJ:"
	$(MAKE) db-best-trj

status: ## Show complete status
	@echo "Services status:"
	$(MAKE) ps
	@echo ""
	@echo "Database statistics:"
	$(MAKE) db-stats
	@echo ""
	@echo "Health check:"
	$(MAKE) health
# ============================================
# AUTO SCRAPING
# ============================================
auto-scrape-status: ## Auto scraping status
	@echo "Active periodic tasks:"
	@docker-compose exec backend python manage.py shell -c "from django_celery_beat.models import PeriodicTask; [print(f'{t.name}: enabled={t.enabled}') for t in PeriodicTask.objects.all()]"

auto-scrape-enable: ## Enable auto scraping
	@echo "Enabling auto scraping..."
	@docker-compose exec backend python manage.py shell -c "from django_celery_beat.models import PeriodicTask; t=PeriodicTask.objects.get(name='Scraping automatique toutes les 6h'); t.enabled=True; t.save(); print('ACTIVE')"
	@docker-compose restart celery_beat > /dev/null 2>&1

auto-scrape-disable: ## Disable auto scraping
	@echo "Disabling auto scraping..."
	@docker-compose exec backend python manage.py shell -c "from django_celery_beat.models import PeriodicTask; t=PeriodicTask.objects.get(name='Scraping automatique toutes les 6h'); t.enabled=False; t.save(); print('DESACTIVE')"
	@docker-compose restart celery_beat > /dev/null 2>&1

auto-scrape-test: ## Launch auto scraping immediately
	@echo "Launching scraping..."
	@docker-compose exec backend python manage.py shell -c "from core.tasks import auto_scrape_all_leagues; r=auto_scrape_all_leagues.delay(); print(f'Task ID: {r.id}')"
	@echo "Follow: sudo make logs-celery-worker"

auto-scrape-logs: ## Auto scraping logs
	@docker-compose logs celery_worker celery_beat --tail=50 -f