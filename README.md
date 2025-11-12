# 🎯 GIG-Benchmark

**GIG-Benchmark** is a comprehensive sports betting odds comparison platform that automatically scrapes, processes, and displays betting odds from multiple bookmakers across various sports leagues.

The platform uses a distributed microservices architecture with automated web scraping, message queue processing, and a modern web interface to provide real-time odds comparison and arbitrage opportunity detection.

You can see our landing page for visual presentation : https://dougd0ug.github.io/gig-benchmark-project/

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Services Overview](#-services-overview)
- [Data Flow](#-data-flow)
- [Development](#-development)
- [Supported Leagues](#-supported-leagues)
- [Contributing](#-contributing)

---

## ✨ Features

- **Automated Web Scraping**: Selenium-based scraping workers for multiple betting sites
- **Multi-League Support**: Football leagues including Ligue 1, Premier League, Bundesliga, A-League, and more
- **Real-Time Processing**: RabbitMQ message queue for asynchronous task processing
- **Arbitrage Detection**: Automatic calculation of Total Return on Investment (TRJ/ROI)
- **REST API**: Django-based API for data access and management
- **Modern Frontend**: Symfony-based web interface with dynamic odds display
- **Microservices Architecture**: 9 Docker services working together seamlessly
- **Scalable Design**: Message-driven architecture for horizontal scaling

---

## 🏗️ Architecture

The platform consists of **9 Docker services** orchestrated with Docker Compose:

```
┌─────────────────────────────────────────────────────────────┐
│                     GIG-BENCHMARK PLATFORM                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Nginx   │  │   PHP    │  │ Backend  │  │  MySQL   │     │
│  │  :10014  │◄─┤ Symfony  │◄─┤  Django  │◄─┤  :3307   │     │
│  └──────────┘  └──────────┘  │  :8000   │  └──────────┘     │
│                               └────┬─────┘                  │
│                                    │                        │
│  ┌──────────┐  ┌──────────┐  ┌───▼─────┐  ┌──────────┐      │
│  │ Selenium │◄─┤ Scraping │◄─┤RabbitMQ │◄─┤ Consumer │      │
│  │  :4444   │  │  Worker  │  │ :5672   │  │   Odds   │      │
│  └──────────┘  └──────────┘  └─────────┘  └──────────┘      │
│                                    ▲                        │
│                               ┌────┴─────┐                  │
│                               │  Celery  │                  │
│                               │ Worker + │                  │
│                               │   Beat   │                  │
│                               └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

Before installing the project, ensure you have:

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **Git**
- At least **4GB of RAM** available for containers
- **Ports available**: 3307, 4444, 5672, 8000, 10014, 15672

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/gig-benchmark.git
cd gig-benchmark
```

### 2. Configure environment variables

Create a `.env` file at the project root, ask us for the content.

### 3. Build and start all services

```bash
# Build all Docker images
docker compose build

# Start all services in detached mode
docker compose up -d

# Wait for services to initialize (about 30 seconds)
sleep 30

# Verify all services are running
docker compose ps
```

### 4. Initialize the database

Django migrations are automatically run on backend startup, but you can verify:

```bash
# Check migration status
docker compose exec backend python manage.py showmigrations

# Create a superuser for Django admin (optional)
docker compose exec backend python manage.py createsuperuser
```

### 5. Access the platform

- **Frontend**: http://localhost:10014
- **Django Admin**: http://localhost:8000/admin
- **RabbitMQ Management**: http://localhost:15672 (admin/admin)
- **Selenium VNC**: http://localhost:7900 (for debugging)

---

## 🎮 Usage

### Triggering a Scraping Task

You can trigger scraping from the frontend interface or manually via command line:

```bash
# Method 1: Using the scraping service directly
docker compose exec scraping python send_task.py football.ligue_1

# Method 2: Check available scrapers
docker compose exec scraping python -c "from registry import SCRAPERS; print(list(SCRAPERS.keys()))"
```

### Monitoring the Process

```bash
# View scraping worker logs
docker compose logs scraping -f

# View consumer odds logs
docker compose logs consumer_odds -f

# View RabbitMQ queue status
docker compose exec rabbitmq rabbitmqctl list_queues

# View backend logs
docker compose logs backend -f
```

### Checking Results

```bash
# Access MySQL database
docker compose exec db mysql -u gig_user -p gig_benchmark

# Check stored matches
mysql> SELECT * FROM core_match LIMIT 10;

# Check stored odds
mysql> SELECT * FROM core_odd LIMIT 10;
```

---

## 📂 Project Structure

```
gig-benchmark/
├── backend/                    # Django REST API
│   ├── config/                 # Django configuration
│   ├── core/                   # Main application (models, views, serializers)
│   ├── consumers/              # RabbitMQ consumers
│   │   └── consumer_odds.py    # Odds consumer (reads 'odds' queue)
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Symfony web interface
│   ├── src/                    # PHP controllers and services
│   ├── templates/              # Twig templates
│   ├── public/                 # Public assets
│   │   ├── js/                 # JavaScript files
│   │   │   ├── sidebar.js      # Scraping triggers and filters
│   │   │   ├── login.js        # Authentication
│   │   │   ├── navbar-auth.js  # Navigation
│   │   │   └── odds-loader.js  # Dynamic odds loading
│   │   └── css/                # Stylesheets
│   ├── composer.json
│   └── Dockerfile
│
├── scraping/                   # Web scraping workers
│   ├── src/
│   │   ├── football/           # Football league scrapers
│   │   │   ├── ligue_1.py      # French Ligue 1
│   │   │   ├── premier_league.py
│   │   │   ├── bundesliga.py
│   │   │   ├── a_league.py     # Australian A-League
│   │   │   └── _scraper_utils.py # Shared utilities
│   │   └── registry.py         # Scraper registry
│   ├── worker.py               # Main worker (listens to 'scraping_tasks')
│   ├── send_task.py            # Task sender utility
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/                   # Database initialization
│   └── schema.sql              # (Deprecated - using Django migrations)
│
├── docker-compose.yml          # Docker services orchestration
├── nginx.conf                  # Nginx configuration
├── .env                        # Environment variables
├── .gitignore
└── README.md                   # This file
```

---

## 🐳 Services Overview

### 1. **MySQL Database** (`db`)
- **Image**: `mysql:8.0`
- **Port**: `3307:3306`
- **Role**: Stores all application data (matches, odds, bookmakers, users)
- **Volume**: Persistent storage via `db_data` volume

### 2. **RabbitMQ** (`rabbitmq`)
- **Image**: `rabbitmq:3.12-management-alpine`
- **Ports**: `5672` (AMQP), `15672` (Management UI)
- **Role**: Message broker for asynchronous task processing
- **Queues**:
  - `scraping_tasks`: Receives scraping requests
  - `odds`: Receives scraped odds data

### 3. **Django Backend** (`backend`)
- **Port**: `8000`
- **Role**: REST API, admin interface, database management
- **Tech**: Django + Gunicorn (4 workers)
- **Endpoints**:
  - `/admin/` - Django admin
  - `/api/` - REST API endpoints

### 4. **Celery Worker** (`celery_worker`)
- **Role**: Processes asynchronous background tasks
- **Concurrency**: 4 workers
- **Use cases**: Scheduled tasks, batch processing

### 5. **Celery Beat** (`celery_beat`)
- **Role**: Task scheduler (cron-like)
- **Use cases**: Periodic scraping, data cleanup, maintenance tasks

### 6. **Consumer Odds** (`consumer_odds`)
- **Role**: Consumes messages from `odds` queue and stores them in MySQL
- **File**: `backend/consumers/consumer_odds.py`
- **Process**:
  1. Listens to `odds` queue
  2. Parses odds data
  3. Creates/updates Match, Odd, and Bookmaker records

### 7. **Selenium** (`selenium`)
- **Image**: `selenium/standalone-chrome`
- **Port**: `4444` (WebDriver), `7900` (VNC)
- **Role**: Headless Chrome browser for web scraping
- **Memory**: 3GB shared memory
- **Config**: Max 1 session, 5-minute timeout

### 8. **Scraping Worker** (`scraping`)
- **Role**: Web scraping orchestrator
- **Process**:
  1. Listens to `scraping_tasks` queue
  2. Loads appropriate scraper from registry
  3. Connects to Selenium for browser automation
  4. Scrapes betting sites (e.g., coteur.com)
  5. Sends results to `odds` queue

### 9. **Nginx + PHP-FPM** (`nginx` + `php`)
- **Port**: `10014`
- **Role**: Serves Symfony frontend application
- **Tech**: Nginx as reverse proxy + PHP 8.3-FPM

---

## 🔄 Data Flow

Here's how a complete scraping cycle works:

```
┌────────────────────────────────────────────────────────────┐
│ 1. TRIGGER                                                 │
│    User clicks "Scrape" → Frontend sends request           │
│    OR: python send_task.py football.ligue_1                │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 2. RABBITMQ - Queue "scraping_tasks"                       │
│    Message: {"scraper": "football.ligue_1"}                │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 3. SCRAPING WORKER                                         │
│    - Consumes message from "scraping_tasks"                │
│    - Loads scraper: scraping/src/football/ligue_1.py       │
│    - Connects to Selenium (port 4444)                      │
│    - Opens headless Chrome                                 │
│    - Navigates to betting site                             │
│    - Extracts match data and odds                          │
│    - For each match/bookmaker:                             │
│      → Publishes message to "odds" queue                   │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 4. RABBITMQ - Queue "odds"                                 │
│    Multiple messages: {match, bookmaker, odds, trj}        │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 5. CONSUMER ODDS                                           │
│    - Consumes messages from "odds" queue                   │
│    - Parses JSON data                                      │
│    - Creates/updates database records:                     │
│      • Match (team names, date, league)                    │
│      • Bookmaker (name, URL)                               │
│      • Odd (1, N, 2, TRJ)                                  │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 6. MYSQL DATABASE                                          │
│    Data stored and ready for display                       │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 7. FRONTEND DISPLAY                                        │
│    - User visits http://localhost:10014                    │
│    - Frontend queries Django API                           │
│    - Odds displayed with TRJ calculation                   │
│    - Arbitrage opportunities highlighted                   │
└────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Development

### Running Individual Services

```bash
# Start only the database
docker compose up -d db

# Start backend and dependencies
docker compose up -d backend

# Restart a specific service
docker compose restart scraping

# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes all data)
docker compose down -v
```

### Viewing Logs

```bash
# Follow logs for all services
docker compose logs -f

# Follow logs for specific service
docker compose logs -f scraping

# Show last 100 lines
docker compose logs --tail=100 backend
```

### Accessing Service Shells

```bash
# Django shell
docker compose exec backend python manage.py shell

# MySQL shell
docker compose exec db mysql -u gig_user -p

# Scraping worker bash
docker compose exec scraping bash

# PHP container bash
docker compose exec php bash
```

### Adding a New Scraper

1. Create a new scraper file in `scraping/src/football/`:

```python
# scraping/src/football/new_league.py
from ._scraper_utils import publish_odds, setup_driver
import pika

def scrape_new_league():
    """Scrape odds for New League"""
    return scrape_league(
        league_name="New League",
        league_url="https://www.coteur.com/NewLeague",
        display_name="NewLeague"
    )
```

2. Register it in `scraping/src/worker.py`:

```python
SCRAPERS = {
    'football.new_league': 'src.football.new_league.scrape_new_league',
    # ... other scrapers
}
```

3. Update frontend in `frontend/public/js/sidebar.js` to add the league button.

---

## ⚽ Supported Leagues

Currently supported football leagues:

- **Ligue 1** (France) - `football.ligue_1`
- **Premier League** (England) - `football.premier_league`
- **Bundesliga** (Germany) - `football.bundesliga`
- **A-League** (Australia) - `football.a_league`
- **Serie A** (Italy) - `football.serie_a`
- **La Liga** (Spain) - `football.la_liga`

And others more.
---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Ensure all services still work: `docker compose up`
5. Commit your changes: `git commit -m "Add new feature"`
6. Push to the branch: `git push origin feature/new-feature`
7. Create a Pull Request

---

## 🐛 Known Issues

- Scraping may fail if betting sites change their HTML structure
- Large scraping jobs may require increasing Selenium memory limit

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Django, Symfony, Selenium, RabbitMQ, and Docker**

Dorine Lemée, Simon Paulin and Louis and Manchon.
