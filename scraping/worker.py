"""
Worker principal pour le système de scraping multi-sports
Écoute RabbitMQ et dispatche vers les scrapers appropriés

Supporte tous les sports : Football, Basketball, Rugby, Tennis
"""
import os
import sys
import time
import json
import pika
import traceback
from typing import Dict, Callable

# Ajouter le path
sys.path.insert(0, '/app')

print("Chargement des scrapers...")

# ============================================================================
# FOOTBALL - Import des scrapers
# ============================================================================
scrapers_loaded = []
scrapers_failed = []

try:
    from src.football.ligue_1 import scrape_ligue_1
    scrapers_loaded.append('football.ligue_1')
except ImportError as e:
    scrapers_failed.append(('football.ligue_1', str(e)))
    scrape_ligue_1 = None

try:
    from src.football.premier_league import scrape_premier_league
    scrapers_loaded.append('football.premier_league')
except ImportError as e:
    scrapers_failed.append(('football.premier_league', str(e)))
    scrape_premier_league = None

try:
    from src.football.la_liga import scrape_la_liga
    scrapers_loaded.append('football.la_liga')
except ImportError as e:
    scrapers_failed.append(('football.la_liga', str(e)))
    scrape_la_liga = None

try:
    from src.football.serie_a import scrape_serie_a
    scrapers_loaded.append('football.serie_a')
except ImportError as e:
    scrapers_failed.append(('football.serie_a', str(e)))
    scrape_serie_a = None

try:
    from src.football.bundesliga import scrape_bundesliga
    scrapers_loaded.append('football.bundesliga')
except ImportError as e:
    scrapers_failed.append(('football.bundesliga', str(e)))
    scrape_bundesliga = None

try:
    from scraping.src.football.champions_league import scrape_champions_league
    scrapers_loaded.append('football.champions_league')
except ImportError as e:
    scrapers_failed.append(('football.champions_league', str(e)))
    scrape_champions_league = None

# ============================================================================
# BASKETBALL - Import des scrapers
# ============================================================================
try:
    from src.basketball.nba import scrape_nba
    scrapers_loaded.append('basketball.nba')
except ImportError as e:
    scrapers_failed.append(('basketball.nba', str(e)))
    scrape_nba = None

try:
    from src.basketball.euro_league import scrape_euroleague
    scrapers_loaded.append('basketball.euroleague')
except ImportError as e:
    scrapers_failed.append(('basketball.euroleague', str(e)))
    scrape_euroleague = None

# ============================================================================
# RUGBY - Import des scrapers
# ============================================================================
try:
    from src.rugby.top_14 import scrape_top14
    scrapers_loaded.append('rugby.top14')
except ImportError as e:
    scrapers_failed.append(('rugby.top14', str(e)))
    scrape_top14 = None

# ============================================================================
# TENNIS - Import des scrapers
# ============================================================================
try:
    from src.tennis.atp import scrape_atp
    scrapers_loaded.append('tennis.atp')
except ImportError as e:
    scrapers_failed.append(('tennis.atp', str(e)))
    scrape_atp = None

try:
    from src.tennis.wta import scrape_wta
    scrapers_loaded.append('tennis.wta')
except ImportError as e:
    scrapers_failed.append(('tennis.wta', str(e)))
    scrape_wta = None

# ============================================================================
# Configuration RabbitMQ
# ============================================================================
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'gig_user')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'gig_password')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'scraping_tasks')

# ============================================================================
# Registre des scrapers disponibles
# ============================================================================
SCRAPERS_REGISTRY: Dict[str, Callable] = {}

# Football
if scrape_ligue_1:
    SCRAPERS_REGISTRY['football.ligue_1'] = scrape_ligue_1
if scrape_premier_league:
    SCRAPERS_REGISTRY['football.premier_league'] = scrape_premier_league
if scrape_la_liga:
    SCRAPERS_REGISTRY['football.la_liga'] = scrape_la_liga
if scrape_serie_a:
    SCRAPERS_REGISTRY['football.serie_a'] = scrape_serie_a
if scrape_bundesliga:
    SCRAPERS_REGISTRY['football.bundesliga'] = scrape_bundesliga
if scrape_champions_league:
    SCRAPERS_REGISTRY['football.champions_league'] = scrape_champions_league

# Basketball
if scrape_nba:
    SCRAPERS_REGISTRY['basketball.nba'] = scrape_nba
if scrape_euroleague:
    SCRAPERS_REGISTRY['basketball.euroleague'] = scrape_euroleague

# Rugby
if scrape_top14:
    SCRAPERS_REGISTRY['rugby.top14'] = scrape_top14

# Tennis
if scrape_atp:
    SCRAPERS_REGISTRY['tennis.atp'] = scrape_atp
if scrape_wta:
    SCRAPERS_REGISTRY['tennis.wta'] = scrape_wta


def connect_rabbitmq(max_retries=10, retry_delay=5):
    """Connexion à RabbitMQ avec retry"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Tentative de connexion à RabbitMQ ({attempt}/{max_retries})...")
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=5672,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            print("Connecté à RabbitMQ")
            return connection
        except Exception as e:
            print(f"Erreur connexion RabbitMQ (tentative {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Nouvelle tentative dans {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print("Échec de connexion après toutes les tentatives")
                raise


def callback(ch, method, properties, body):
    """
    Callback appelé quand un message arrive dans la queue
    
    Format attendu du message JSON:
    {
        "scraper": "football.ligue_1",
        "params": {
            "url": "...",
            "options": {...}
        }
    }
    """
    try:
        # Décoder le message
        message = json.loads(body.decode('utf-8'))
        scraper_name = message.get('scraper')
        params = message.get('params', {})
        
        print(f"\n{'='*60}")
        print(f"NOUVELLE TÂCHE REÇUE")
        print(f"{'='*60}")
        print(f"Scraper: {scraper_name}")
        print(f"Params: {params}")
        print(f"Heure: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Vérifier que le scraper existe
        if scraper_name not in SCRAPERS_REGISTRY:
            print(f"ERREUR: Scraper inconnu '{scraper_name}'")
            print(f"\nScrapers disponibles:")
            for sport, scrapers in get_scrapers_by_sport().items():
                print(f"   {sport}:")
                for s in scrapers:
                    print(f"      - {s}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return
        
        # Récupérer et exécuter le scraper
        scraper_func = SCRAPERS_REGISTRY[scraper_name]
        print(f"Démarrage du scraper: {scraper_name}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        result = scraper_func(**params)
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print(f"SCRAPING TERMINÉ")
        print(f"{'='*60}")
        print(f"Durée: {elapsed_time:.2f}s")
        print(f"Résultat: {result}")
        print(f"{'='*60}\n")
        
        # Acquitter le message (succès)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except json.JSONDecodeError as e:
        print(f"Erreur de parsing JSON: {e}")
        print(f"Body reçu: {body}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERREUR DURANT LE SCRAPING")
        print(f"{'='*60}")
        print(f"Message: {e}")
        print(f"Stacktrace:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        # Rejeter le message sans requeue pour éviter les boucles infinies
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def get_scrapers_by_sport():
    """Retourne les scrapers organisés par sport"""
    sports = {
        'Football': [],
        'Basketball': [],
        'Rugby': [],
        'Tennis': []
    }
    
    for scraper in SCRAPERS_REGISTRY.keys():
        if scraper.startswith('football.'):
            sports['Football'].append(scraper)
        elif scraper.startswith('basketball.'):
            sports['Basketball'].append(scraper)
        elif scraper.startswith('rugby.'):
            sports['Rugby'].append(scraper)
        elif scraper.startswith('tennis.'):
            sports['Tennis'].append(scraper)
    
    return sports


def print_startup_banner():
    """Affiche la bannière de démarrage"""
    print("\n" + "="*60)
    print("WORKER DE SCRAPING MULTI-SPORTS - GIG BENCHMARK")
    print("="*60)
    print(f"RabbitMQ Host: {RABBITMQ_HOST}")
    print(f"RabbitMQ User: {RABBITMQ_USER}")
    print(f"Queue: {RABBITMQ_QUEUE}")
    print("="*60)
    
    # Afficher les scrapers chargés par sport
    print(f"\nSCRAPERS CHARGÉS ({len(scrapers_loaded)}):")
    sports = get_scrapers_by_sport()
    for sport, scrapers in sports.items():
        if scrapers:
            print(f"\n{sport} ({len(scrapers)}):")
            for scraper in scrapers:
                print(f"   ✓ {scraper}")
    
    # Afficher les scrapers qui ont échoué
    if scrapers_failed:
        print(f"\nSCRAPERS NON CHARGÉS ({len(scrapers_failed)}):")
        for scraper, error in scrapers_failed:
            print(f"{scraper}")
            print(f"Raison: {error}")
    
    print("\n" + "="*60)
    print("COMMENT ENVOYER UNE TÂCHE:")
    print("="*60)
    print("Depuis Python:")
    print("  import pika, json")
    print("  conn = pika.BlockingConnection(...)")
    print("  ch = conn.channel()")
    print("  ch.basic_publish('', 'scraping_tasks',")
    print("    json.dumps({'scraper': 'football.ligue_1'}))")
    print("\nDepuis Django:")
    print("  python manage.py scrape football.ligue_1")
    print("\nDepuis le conteneur scraping:")
    print("  python send_task.py football.ligue_1")
    print("="*60 + "\n")


def main():
    """Fonction principale du worker"""
    print_startup_banner()
    
    # Connexion à RabbitMQ
    connection = connect_rabbitmq()
    channel = connection.channel()
    
    # Déclarer la queue (durable = survit aux redémarrages)
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    
    # Configurer la consommation
    # prefetch_count=1 : Un seul message à la fois (évite la surcharge)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=False  # Acquittement manuel
    )
    
    print("EN ATTENTE DE TÂCHES...")
    print("Le worker est prêt à traiter les demandes de scraping")
    print("="*60 + "\n")
    
    try:
        # Démarrer la consommation (boucle infinie)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur")
        channel.stop_consuming()
    except Exception as e:
        print(f"\nErreur fatale: {e}")
        traceback.print_exc()
    finally:
        connection.close()
        print("\nWorker arrêté proprement")


if __name__ == "__main__":
    main()