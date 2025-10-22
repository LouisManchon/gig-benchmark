<<<<<<< HEAD
# 🎨 Frontend Symfony

Ce dépôt contient la partie **frontend** du projet, développée avec le framework **Symfony**.  
Il gère l’affichage, les routes publiques, et la communication avec l’API backend.

---

## 🚀 Prérequis

Avant de lancer le projet, assure-toi d’avoir installé :

- [PHP >= 8.3](https://www.php.net/downloads.php)

```bash
sudo apt update
sudo apt install php php-cli php-xml php-mbstring php-intl php-curl php-zip unzip git -y
sudo apt install composer -y
````
- [Symfony CLI](https://symfony.com/download)

```bash
wget https://get.symfony.com/cli/installer -O - | bash
sudo mv ~/.symfony*/bin/symfony /usr/local/bin/symfony
```

- Doctrine (si on veut lier la base de données directement dans Symfony)
```bash
composer require symfony/orm-pack
composer require symfony/doctrine-fixtures --dev
=======
# Lancer le consumer

sudo docker compose up -d consumer_odds

# Attendre 5 secondes

sleep 5

# Vérifier qu'il tourne

sudo docker compose ps

# Voir les logs

sudo docker compose logs consumer_odds -f

>>>>>>> 0c970882da97718f173367570fd5e4309b9c825d
```

---

<<<<<<< HEAD
## ⚙️ Installation du projet

Clone le dépôt et installe les dépendances PHP et JS :

```bash
git clone [https://github.com/gig-benchmark.git](https://github.com/LouisManchon/gig-benchmark/tree/dorine/front)

# Installation des dépendances PHP
composer install

# Installation des dépendances frontend
npm install

```

## 🧑‍💻 Lancer le serveur de développement

Démarre le serveur Symfony :

``` bash
symfony serve
```

Par défaut, le site est accessible sur http://localhost:8000

## Structure du projet 

```bash
.
├── assets/              # Code JS/CSS source
├── config/              # Configuration Symfony
├── public/              # Fichiers publics (build, index.php, images, etc.)
├── src/                 # Code PHP (contrôleurs, services, etc.)
├── templates/           # Vues Twig
├── translations/        # Fichiers de traduction
├── .env                 # Configuration d'environnement
└── webpack.config.js    # Configuration Webpack Encore

```

=======
# 📚 RÉSUMÉ COMPLET DE L'ARCHITECTURE

## 🏗️ **STRUCTURE DU PROJET**
```

gig-benchmark/
├── backend/ → API Django + Base de données
├── frontend/ → Interface PHP/Symfony
├── scraping/ → Worker de scraping
├── database/ → Schéma SQL
├── docker-compose.yml → Configuration Docker
└── .env → Variables d'environnement

```

---

## 🔄 **LES 9 SERVICES DOCKER**

### **1️⃣ MySQL (`db`)**
- **Rôle** : Base de données
- **Port** : `3307:3306`
- **Données** : Matchs, cotes, bookmakers

### **2️⃣ RabbitMQ (`rabbitmq`)**
- **Rôle** : File de messages (broker)
- **Ports** :
  - `5672` : Connexion AMQP
  - `15672` : Interface web
- **Queues** :
  - `scraping_tasks` : Demandes de scraping
  - `odds` : Cotes scrapées

### **3️⃣ Backend Django (`backend`)**
- **Rôle** : API REST + Admin
- **Port** : `8000`
- **Fichiers** : `backend/`

### **4️⃣ Celery Worker (`celery_worker`)**
- **Rôle** : Tâches asynchrones
- **Fichiers** : `backend/`

### **5️⃣ Celery Beat (`celery_beat`)**
- **Rôle** : Planificateur de tâches
- **Fichiers** : `backend/`

### **6️⃣ 🆕 Consumer Odds (`consumer_odds`)**
- **Rôle** : **Écoute queue `odds` → Stocke en BDD**
- **Fichier** : `backend/consumers/consumer_odds.py`
- **Queue écoutée** : `odds`

### **7️⃣ Selenium (`selenium`)**
- **Rôle** : Navigateur Chrome headless
- **Port** : `4444` (WebDriver)

### **8️⃣ Scraping Worker (`scraping`)**
- **Rôle** : **Scrape les sites → Envoie à RabbitMQ**
- **Fichiers** : `scraping/src/football/ligue_1.py`
- **Queue écoutée** : `scraping_tasks`
- **Queue d'envoi** : `odds`

### **9️⃣ Nginx + PHP (`nginx` + `php`)**
- **Rôle** : Frontend Symfony
- **Port** : `10014`

---

## 🔄 **FLUX DE DONNÉES COMPLET**
```

┌─────────────────────────────────────────────────────┐
│ 1. DÉCLENCHEMENT │
│ python send_task.py football.ligue_1 │
└──────────────────┬──────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ 2. RABBITMQ - Queue "scraping_tasks" │
│ Message: {"scraper": "football.ligue_1"} │
└──────────────────┬──────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ 3. SCRAPING WORKER │
│ - Lit queue "scraping_tasks" │
│ - Lance scraping/src/football/ligue_1.py │
│ - Se connecte à Selenium (port 4444) │
│ - Scrape coteur.com │
│ - Pour chaque match/bookmaker: │
│ Envoie message à queue "odds" │
└──────────────────┬──────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ 4. RABBITMQ - Queue "odds" │
│ 63 messages: {match, bookmaker, cotes, trj} │
└──────────────────┬──────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ 5. CONSUMER ODDS ⚠️ (À LANCER) │
│ - Lit queue "odds" │
│ - Parse les données │
│ - Stocke en MySQL │
│ • Table: Match │
│ • Table: Odd │
│ • Table: Bookmaker │
└──────────────────┬──────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ 6. MYSQL (db) │
│ Données stockées et prêtes à afficher │
└─────────────────────────────────────────────────────┘

```

---

## 📂 **FICHIERS CLÉS**

| Fichier | Rôle |
|---------|------|
| `scraping/worker.py` | Worker principal qui écoute `scraping_tasks` |
| `scraping/src/football/ligue_1.py` | Scraper Ligue 1 |
| `scraping/send_task.py` | Envoie une demande de scraping |
| `backend/consumers/consumer_odds.py` | ⚠️ Consomme queue `odds` → BDD |
| `backend/core/models.py` | Modèles Django (Match, Odd, etc.) |
| `docker-compose.yml` | Configuration de tous les services |

---

## ✅ **CE QUI FONCTIONNE**
```

✅ Scraping → RabbitMQ
✅ 63 messages dans queue "odds"
✅ TRJ calculé (83-92%)

```

## ❌ **CE QUI MANQUE**
```

❌ Consumer odds PAS lancé
❌ Données PAS en BDD
>>>>>>> 0c970882da97718f173367570fd5e4309b9c825d
