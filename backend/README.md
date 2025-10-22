# 🐍 EXPLICATIONS - Backend Django GIG

Guide complet pour comprendre l'architecture et le fonctionnement du backend.

---

## Vue d'ensemble

Le backend Django sert de **pont entre le scraper et la base de données**.

**Rôle principal :**
1. **Écouter** les messages du scraper (via RabbitMQ)
2. **Parser** les données scrapées
3. **Stocker** les cotes en base de données MySQL
4. **Exposer** une interface admin pour visualiser
5. **Fournir des services** pour déclencher le scraping

---

## Architecture complète

```
┌────────────────────────────────────────────────────────┐
│                    BACKEND DJANGO                       │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐        ┌──────────────┐             │
│  │   Scraper    │───────→│  RabbitMQ    │             │
│  │ (external)   │ publish│  queue: odds │             │
│  └──────────────┘        └──────┬───────┘             │
│                                  │                      │
│                                  │ consume              │
│                                  ↓                      │
│                          ┌───────────────┐             │
│                          │   Consumer    │             │
│                          │consumer_odds.py             │
│                          └───────┬───────┘             │
│                                  │                      │
│                                  │ parse & save         │
│                                  ↓                      │
│                          ┌───────────────┐             │
│                          │  Django ORM   │             │
│                          │   (Models)    │             │
│                          └───────┬───────┘             │
│                                  │                      │
│                                  ↓                      │
│                          ┌───────────────┐             │
│                          │  MySQL DB     │             │
│                          │     GIG       │             │
│                          └───────────────┘             │
│                                  ↑                      │
│                                  │                      │
│                          ┌───────┴───────┐             │
│                          │  Django Admin │             │
│                          │ (Visualisation)│             │
│                          └───────────────┘             │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## Structure des fichiers

```
backend/
│
├── config/                        # Configuration Django
│   └── settings/                  
│       ├── __init__.py           
│       ├── celery.py             # Config Celery/RabbitMQ
│       ├── urls.py               # Routes de l'app
│       └── wsgi.py               # Point d'entrée WSGI
│
├── consumers/                     # Consumer RabbitMQ
│   └── consumer_odds.py          # Lit les messages et stocke en DB
│
├── core/                          # App principale
│   │
│   ├── rabbitmq_config/          # Config RabbitMQ
│   │   ├── __init__.py
│   │   └── rabbitmq_config.py   # Connexion RabbitMQ
│   │
│   ├── services/                 # Services métier
│   │   ├── __init__.py
│   │   └── scraping_service.py  # Service pour déclencher le scraping
│   │
│   ├── views/                    # Vues/API Django
│   │   ├── __init__.py
│   │   └── scraping_views.py    # Vues pour déclencher le scraping
│   │
│   ├── __init__.py
│   ├── admin.py                  # Interface admin Django
│   ├── models.py                 # Définition des tables (ORM)
│   ├── tests.py                  # Tests unitaires
│   └── urls.py                   # Routes de core
│
├── media/                         # Fichiers uploadés
├── static/                        # Fichiers statiques (CSS, JS)
├── staticfiles/                   # Fichiers statiques collectés
│
├── .gitignore                    
├── Dockerfile                     # Image Docker
├── entrypoint.sh                  # Script de démarrage Docker
├── gunicorn.conf.py               # Config Gunicorn (production)
├── manage.py                      # Point d'entrée Django
├── README.md                      
└── requirements.txt               # Dépendances Python
```

---

##  Composants principaux

### 1️ `config/settings/` - Configuration Django

**Fichiers :**

#### A. `celery.py` - Configuration Celery/RabbitMQ

```python
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('gig_benchmark')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
```

**Rôle :** Configure Celery pour communiquer avec RabbitMQ.

#### B. `urls.py` - Routes principales

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Routes de l'API
]
```

**Rôle :** Définit les URLs de l'application.

#### C. Configuration de la DB (dans `__init__.py` ou fichier séparé)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'GIG'),
        'USER': os.environ.get('DB_USER', 'gig_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'gig_password'),
        'HOST': os.environ.get('DB_HOST', 'mysql'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

---

### 2️ `core/models.py` - Models Django (ORM)

**Rôle :** Définir les tables de la base de données en Python

**Tables définies :**
- `Sport` (Football, Basketball, Tennis, Rugby)
- `MarketName` (1X2, Over/Under, etc.)
- `League` (Ligue 1, Premier League, NBA, etc.)
- `Team` (PSG, OM, Lyon, etc.)
- `Bookmaker` (Betclic, Winamax, PMU, etc.)
- `Match` (PSG vs OM, date, statut)
- `Odd` (cotes avec TRJ par match/bookmaker)

**Exemple de code :**

```python
class Odd(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    market = models.ForeignKey(MarketName, on_delete=models.CASCADE)
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE)
    outcome = models.CharField(max_length=50)  # '1', 'X', '2'
    odd_value = models.DecimalField(max_digits=6, decimal_places=2)
    trj = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # TRJ par match
    scraped_at = models.DateTimeField()
    
    class Meta:
        db_table = 'Odds'
```

**Utilisation :**

```python
# Créer une cote
Odd.objects.create(
    match=match_obj,
    bookmaker=betclic,
    outcome='1',
    odd_value=1.85,
    trj=91.5,
    scraped_at=now()
)

# Lire toutes les cotes d'un match
match.odds.all()

# Filtrer par bookmaker
Odd.objects.filter(bookmaker__name='Betclic')
```

---

### 3️ `core/admin.py` - Interface d'administration

**Rôle :** Interface web pour visualiser/modifier les données

```python
from django.contrib import admin
from .models import Sport, League, Team, Match, Bookmaker, Odd

@admin.register(Odd)
class OddAdmin(admin.ModelAdmin):
    list_display = ['get_match', 'bookmaker', 'outcome', 'odd_value', 'trj', 'scraped_at']
    list_filter = ['bookmaker', 'scraped_at']
    
    def get_match(self, obj):
        return f"{obj.match.home_team.name} vs {obj.match.away_team.name}"
```

**Accès :** `http://localhost:8000/admin`

---

### 4️ `core/rabbitmq_config/rabbitmq_config.py` - Config RabbitMQ

**Rôle :** Configuration centralisée de RabbitMQ

```python
import pika
import os

def get_rabbitmq_connection():
    """Get RabbitMQ connection"""
    credentials = pika.PlainCredentials(
        os.environ.get('RABBITMQ_USER', 'gig_user'),
        os.environ.get('RABBITMQ_PASSWORD', 'gig_password_2025')
    )
    
    parameters = pika.ConnectionParameters(
        host=os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
        port=int(os.environ.get('RABBITMQ_PORT', 5672)),
        credentials=credentials
    )
    
    return pika.BlockingConnection(parameters)
```

**Utilisation :**

```python
from core.rabbitmq_config.rabbitmq_config import get_rabbitmq_connection

connection = get_rabbitmq_connection()
channel = connection.channel()
channel.queue_declare(queue='odds')
```

---

### 5️ `core/services/scraping_service.py` - Service de scraping

**Rôle :** Déclencher le scraping depuis l'API Django

```python
import pika
import json
from core.rabbitmq_config.rabbitmq_config import get_rabbitmq_connection

class ScrapingService:
    """Service to trigger scraping tasks"""
    
    @staticmethod
    def trigger_ligue1_scraping():
        """Trigger Ligue 1 scraping by publishing to RabbitMQ"""
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare queue
        channel.queue_declare(queue='scraping_tasks', durable=True)
        
        # Publish message
        message = {
            'task': 'scrape_ligue1',
            'sport': 'football',
            'league': 'Ligue 1'
        }
        
        channel.basic_publish(
            exchange='',
            routing_key='scraping_tasks',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
        connection.close()
        return {'success': True, 'message': 'Scraping task triggered'}
```

---

### 6️ `core/views/scraping_views.py` - Vues API

**Rôle :** Endpoints API pour déclencher le scraping

```python
from django.http import JsonResponse
from django.views import View
from core.services.scraping_service import ScrapingService

class TriggerScrapingView(View):
    """API endpoint to trigger scraping"""
    
    def post(self, request):
        """Trigger scraping for Ligue 1"""
        result = ScrapingService.trigger_ligue1_scraping()
        return JsonResponse(result)
```

**Routes (`core/urls.py`) :**

```python
from django.urls import path
from core.views.scraping_views import TriggerScrapingView

urlpatterns = [
    path('scrape/ligue1/', TriggerScrapingView.as_view(), name='scrape_ligue1'),
]
```

**Utilisation :**

```bash
# Déclencher le scraping via API
curl -X POST http://localhost:8000/api/scrape/ligue1/
```

---

### 7️ `consumers/consumer_odds.py` - Consumer RabbitMQ

**Rôle :** **LE PLUS IMPORTANT** - Lit les messages du scraper et stocke en DB

**Flux complet :**

```
1. Scraper publie un message dans queue "odds"
   ↓
   {
     "match": "PSG - OM",
     "bookmaker": "Betclic",
     "cotes": {"cote_1": 1.85, "cote_N": 3.40, "cote_2": 4.20},
     "trj": 91.5,
     "league": "Ligue 1",
     "sport": "football"
   }
   ↓
2. Consumer écoute la queue
   ↓
3. Callback function called
   ↓
4. Parse le message
   - Récupère Sport (FOOT)
   - Récupère/crée League (Ligue 1)
   - Parse "PSG - OM" → 2 équipes
   - Récupère/crée PSG et OM
   - Récupère/crée Match
   - Récupère Bookmaker
   ↓
5. Crée 3 Odds (une par outcome: 1, X, 2) avec le TRJ
   ↓
6. Données en DB !
```

**Code clé :**

```python
def callback(ch, method, properties, body):
    """Process each message"""
    message = json.loads(body)
    
    # Extract data
    match_str = message.get('match')      # "PSG - OM"
    bookmaker = message.get('bookmaker')  # "Betclic"
    cotes = message.get('cotes')
    trj = message.get('trj')              # 91.5
    
    # Create teams, match, and odds in DB
    # ... (voir le code complet dans le fichier consumer_odds.py)
    
    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)
```

**Démarrer le consumer :**

```bash
cd backend
python consumers/consumer_odds.py
```

---

## Workflow complet

```
┌────────────────────────────────────────────────────────┐
│ 1. API Call (optionnel)                                │
│    POST /api/scrape/ligue1/                            │
│    → ScrapingService.trigger_ligue1_scraping()         │
│    → Publish message to RabbitMQ queue "scraping_tasks"│
└─────────────────────┬──────────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────────┐
│ 2. Scraper (externe, dans /scraping)                   │
│    - Lit la queue "scraping_tasks" (optionnel)         │
│    - Ou se lance manuellement                          │
│    - Scrappe coteur.com                                │
│    - Publie dans queue "odds"                          │
└─────────────────────┬──────────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────────┐
│ 3. RabbitMQ queue "odds"                               │
│    - Messages en attente                               │
└─────────────────────┬──────────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────────┐
│ 4. Consumer (consumers/consumer_odds.py)               │
│    - Lit les messages                                  │
│    - Parse JSON                                        │
│    - Utilise Django ORM                                │
└─────────────────────┬──────────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────────┐
│ 5. MySQL DB                                            │
│    - Tables: Sports, Leagues, Teams, Matches, Odds     │
│    - Données persistées avec TRJ                       │
└─────────────────────┬──────────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────────┐
│ 6. Django Admin                                        │
│    http://localhost:8000/admin                         │
│    - Visualise matchs, cotes, TRJ                      │
└────────────────────────────────────────────────────────┘
```

---

## Commandes utiles

### Installation

```bash
# Installer les dépendances
cd backend
pip install -r requirements.txt

# Créer les tables en DB
python manage.py migrate --fake-initial

# Créer un superuser pour l'admin
python manage.py createsuperuser
```

### Développement

```bash
# Lancer le serveur Django
python manage.py runserver
# → http://localhost:8000

# Lancer le consumer (terminal 2)
python consumers/consumer_odds.py
# → Écoute la queue 'odds'

# Shell Django (tester l'ORM)
python manage.py shell
```

### Tests

```bash
# Lancer les tests
python manage.py test

# Test d'un fichier spécifique
python manage.py test core.tests
```

---

##  Debugging

### Le consumer ne reçoit pas de messages

```bash
# Vérifier RabbitMQ
docker ps | grep rabbitmq

# Voir les queues
docker exec -it gig-benchmark-rabbitmq-1 rabbitmqctl list_queues

# Voir les connexions
docker exec -it gig-benchmark-rabbitmq-1 rabbitmqctl list_connections
```

### Erreur "Bookmaker not found"

**Vérifier le mapping dans `consumer_odds.py` :**

```python
def get_bookmaker_code(bookmaker_name):
    mapping = {
        'Betclic': 'BETCLIC',
        'Winamax': 'WINAMAX',
        'PMU': 'PMU',
        # ... ajouter tous les bookmakers
    }
```

### Logs du consumer

```bash
# Ajouter des logs dans consumer_odds.py
print(f" Message reçu: {message}")
print(f" {odds_count} cotes sauvegardées")
```

---

## Prochaines étapes

### Court terme
- [ ] Extraire la vraie date du match depuis coteur.com
- [ ] Ajouter des logs structurés (logging module)
- [ ] Tests unitaires pour le consumer

### Moyen terme
- [ ] API REST complète (Django REST Framework)
- [ ] Endpoint : "meilleures cotes pour un match"
- [ ] Celery Beat pour automatiser le scraping

### Long terme
- [ ] Calcul de "value bets"
- [ ] Alertes en temps réel

---

## 📚 Ressources

- [Django Documentation](https://docs.djangoproject.com/)
- [Celery + Django](https://docs.celeryproject.org/en/stable/django/)
- [RabbitMQ + Python](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)

---

**Version :** 2.0 (basé sur ta vraie arborescence)  
**Dernière mise à jour :** Octobre 2025  
**Auteur :** GIG Team