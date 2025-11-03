# Installation GIG BENCHMARK

Guide d'installation rapide pour le projet GIG BENCHMARK - Système de scraping et analyse de cotes sportives.

## Prérequis

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Make
- Git

## Installation rapide (Première installation)

Pour installer le projet complet en une seule commande :

```bash
make install
```

Cette commande va :
1. Construire toutes les images Docker
2. Démarrer tous les services (MySQL, RabbitMQ, Backend Django, Celery, Nginx, etc.)
3. Créer et appliquer les migrations de base de données
4. Charger les données de référence (sports, ligues, bookmakers, marchés)

**Temps estimé : 3-5 minutes**

## Services disponibles après installation

- **Backend API** : http://localhost:8000
- **Frontend Symfony** : http://localhost:10014
- **RabbitMQ Management** : http://localhost:15672 (user: gig_user, pass: gig_password)
- **MySQL** : localhost:3307 (user: gig_user, pass: gig_password, db: gig_benchmark)

## Vérification de l'installation

```bash
# Vérifier le statut des services
make status

# Vérifier la santé des services
make health

# Voir les logs
make logs
```

## Test de scraping

Pour tester que le scraping fonctionne :

```bash
# Scraper la Ligue 1
make scrape-ligue1

# Voir les statistiques de la base de données
make db-stats

# Voir les meilleures cotes (TRJ)
make db-best-trj
```

## Commandes utiles

### Gestion des services

```bash
make up              # Démarrer les services
make down            # Arrêter les services
make restart         # Redémarrer les services
make ps              # Voir le statut des conteneurs
make logs            # Voir tous les logs
make logs-backend    # Voir les logs du backend
make logs-scraping   # Voir les logs du scraping
```

### Migrations

```bash
make makemigrations     # Créer de nouvelles migrations
make migrate            # Appliquer les migrations
make migrate-update     # Créer ET appliquer les migrations
make showmigrations     # Afficher l'état des migrations
make migrate-fresh      # Reset complet des migrations (DANGER: supprime les données)
```

### Base de données

```bash
make db-stats           # Statistiques de la base
make db-matches         # Liste des matchs
make db-bookmakers      # Statistiques des bookmakers
make db-odds            # Dernières cotes
make db-best-trj        # Meilleurs TRJ par match
make seed-status        # Statut des seeds
make seed-apply         # Appliquer les seeds manquants
```

### Scraping

```bash
make scrape-ligue1              # Scraper Ligue 1
make scrape-premier-league      # Scraper Premier League
make scrape-champions-league    # Scraper Champions League
make scrape-nba                 # Scraper NBA
make scrape-top14               # Scraper Top 14 (Rugby)

# Scraper par sport
make scrape-all-football        # Tous les championnats de football (105)
make scrape-all-basketball      # Tous les championnats de basketball (15)
make scrape-all-tennis          # Tous les tournois de tennis (89)
make scrape-all-rugby           # Tous les championnats de rugby (3)

# Scraping personnalisé
make scrape LEAGUE=football.ligue_1
make scrape LEAGUE=basketball.nba

# Liste de tous les scrapers disponibles
make scrape-list
```

### Scraping automatique

```bash
make auto-scrape-enable     # Activer le scraping automatique (toutes les 6h)
make auto-scrape-disable    # Désactiver le scraping automatique
make auto-scrape-status     # Voir le statut
make auto-scrape-test       # Lancer un scraping immédiatement
make auto-scrape-logs       # Voir les logs
```

### Shells

```bash
make shell-backend      # Shell dans le conteneur backend
make shell-scraping     # Shell dans le conteneur scraping
make shell-db           # Shell MySQL
make shell-python       # Shell Python/Django
```

## Réinstallation complète

Si vous voulez tout réinstaller de zéro (supprime TOUTES les données) :

```bash
make reinstall
```

Cette commande va :
1. Supprimer tous les conteneurs et volumes
2. Supprimer toutes les données
3. Relancer une installation complète

## Résolution de problèmes

### Les conteneurs redémarrent en boucle

```bash
# Voir les logs pour identifier le problème
make logs-backend
make logs-scraping

# Souvent lié aux migrations
make migrate-fresh
```

### Problèmes de migration

```bash
# Afficher l'état des migrations
make showmigrations

# Réinitialiser les migrations
make migrate-fresh
```

### Base de données corrompue

```bash
# Réinitialiser complètement
make reinstall
```

### Les seeds ne sont pas chargés

```bash
# Vérifier le statut
make seed-status

# Appliquer les seeds manquants
make seed-apply

# Forcer la réapplication
make seed-force
```

## Structure du projet

```
gig-benchmark/
├── backend/              # Backend Django (API REST)
│   ├── core/            # Application principale
│   │   ├── models.py    # Modèles de données
│   │   ├── views.py     # Vues API
│   │   └── tasks.py     # Tâches Celery
│   └── config/          # Configuration Django
├── scraping/            # Service de scraping
│   ├── src/
│   │   ├── football/    # 105 scrapers football
│   │   ├── basketball/  # 15 scrapers basketball
│   │   ├── tennis/      # 89 scrapers tennis
│   │   └── rugby/       # 3 scrapers rugby
│   └── worker.py        # Worker RabbitMQ
├── database/            # Fichiers SQL
│   └── seeds/          # Données de référence
├── frontend/            # Frontend Symfony
└── docker-compose.yml   # Configuration Docker

Total : 212 scrapers disponibles
```

## Architecture

Le système utilise :
- **Django** : API REST et gestion de données
- **MySQL** : Base de données
- **RabbitMQ** : Queue de messages pour le scraping
- **Celery** : Tâches asynchrones et scraping automatique
- **Selenium** : Scraping des sites web
- **Symfony** : Interface frontend
- **Nginx** : Reverse proxy

## Données de référence

Les seeds contiennent :
- **4 sports** : Football, Basketball, Tennis, Rugby
- **212 ligues/compétitions**
- **20+ marchés de paris** (1X2, Over/Under, etc.)
- **15+ bookmakers** (Betclic, Winamax, Unibet, etc.)

## Support

Pour toute question ou problème :
1. Vérifier les logs : `make logs`
2. Vérifier la santé : `make health`
3. Consulter ce guide
4. Contacter l'équipe de développement

## Aide

Pour voir toutes les commandes disponibles :

```bash
make help
```
