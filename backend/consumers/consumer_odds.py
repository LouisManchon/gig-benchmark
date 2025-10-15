"""
Celery Consumer to store scraped odds in database
Listens to RabbitMQ 'odds' queue and inserts data into MySQL

This consumer is designed to read messages from YOUR scraper format:
{
    "match": "PSG - OM",
    "bookmaker": "Betclic",
    "cotes": {
        "cote_1": 1.85,
        "cote_N": 3.40,
        "cote_2": 4.20
    },
    "trj": 91.5,
    "league": "Ligue 1",
    "sport": "football"
}
"""
import os
import django
import json
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from celery import Celery
from core.models import Sport, League, Team, Match, MarketName, Odd, Bookmaker
from django.utils import timezone
import pika

# Celery Configuration
app = Celery('gig_consumer')
app.config_from_object('django.conf:settings', namespace='CELERY')

# RabbitMQ Configuration
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '5672')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'gig_user')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'gig_password_2025')


def get_bookmaker_code(bookmaker_name):
    """
    Convert bookmaker name to code
    Mapping based on coteur.com names
    """
    mapping = {
        'PMU': 'PMU',
        'ParionsSport': 'PARIONSSPORT',
        'ZEbet': 'ZEBET',
        'Winamax': 'WINAMAX',
        'Betclic': 'BETCLIC',
        'Betsson': 'BETSSON',
        'Bwin': 'BWIN',
        'Unibet': 'UNIBET',
        'OlyBet': 'OLYBET',
        'FeelingBet': 'FEELINGBET',
        'Genybet': 'GENYBET',
        'Vbet': 'VBET',
        'Bet365': 'BET365',
        'NetBet': 'NETBET',
        'Pinnacle': 'PINNACLE',
    }
    return mapping.get(bookmaker_name, bookmaker_name.upper())


def parse_team_names(match_str):
    """
    Parse team names from match string
    Examples:
        "PSG - OM" -> ("PSG", "OM")
        "Lyon - Monaco" -> ("Lyon", "Monaco")
    """
    try:
        teams = match_str.split(' - ')
        if len(teams) == 2:
            return teams[0].strip(), teams[1].strip()
        else:
            print(f"Invalid match format: {match_str}")
            return None, None
    except Exception as e:
        print(f"Error parsing teams: {e}")
        return None, None


def get_sport_code(sport_name):
    """
    Convert sport name to code
    """
    mapping = {
        'football': 'FOOT',
        'basketball': 'BASK',
        'tennis': 'TENN',
        'rugby': 'RUGB',
    }
    return mapping.get(sport_name.lower(), 'FOOT')


def callback(ch, method, properties, body):
    """
    Callback function for RabbitMQ messages
    Called for each message received from 'odds' queue
    """
    try:
        # Parse message
        message = json.loads(body)
        print(f"\nReceived message: {message.get('match')} - {message.get('bookmaker')}")
        
        # Extract data from YOUR scraper format
        match_str = message.get('match')
        bookmaker_name = message.get('bookmaker')
        cotes = message.get('cotes', {})
        trj = message.get('trj')
        league_name = message.get('league', 'Ligue 1')
        sport_name = message.get('sport', 'football')
        
        # Validate required fields
        if not match_str or not bookmaker_name or not cotes:
            print(f"Missing required fields in message")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 1. Get or create Sport
        sport_code = get_sport_code(sport_name)
        try:
            sport = Sport.objects.get(code=sport_code)
        except Sport.DoesNotExist:
            print(f"Sport {sport_code} not found in database")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 2. Get or create League
        league, created = League.objects.get_or_create(
            sport=sport,
            name=league_name,
            defaults={'country': 'France'}  # Default country
        )
        if created:
            print(f"New league created: {league.name}")
        
        # 3. Parse teams
        home_team_name, away_team_name = parse_team_names(match_str)
        if not home_team_name or not away_team_name:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 4. Get or create teams
        home_team, _ = Team.objects.get_or_create(
            league=league,
            name=home_team_name
        )
        
        away_team, _ = Team.objects.get_or_create(
            league=league,
            name=away_team_name
        )
        
        # 5. Get or create match (default date: tomorrow at 20:00)
        # TODO: Extract real date from coteur.com
        tomorrow = datetime.now() + timedelta(days=1)
        match_date = tomorrow.replace(hour=20, minute=0, second=0, microsecond=0)
        match_date = timezone.make_aware(match_date)
        
        match, created = Match.objects.get_or_create(
            league=league,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date,
            defaults={'status': 'scheduled'}
        )
        
        if created:
            print(f"New match: {home_team.name} vs {away_team.name}")
        
        # 6. Get market (default: 1X2)
        try:
            market = MarketName.objects.get(sport=sport, code='1X2')
        except MarketName.DoesNotExist:
            print(f"Market 1X2 not found for {sport.code}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 7. Get bookmaker
        bookmaker_code = get_bookmaker_code(bookmaker_name)
        try:
            bookmaker = Bookmaker.objects.get(code=bookmaker_code)
        except Bookmaker.DoesNotExist:
            print(f"Bookmaker {bookmaker_code} not found")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 8. Store odds (one for each outcome: 1, X, 2)
        scraped_at = timezone.now()
        odds_count = 0
        
        outcomes = {
            'cote_1': '1',
            'cote_N': 'X',
            'cote_2': '2'
        }
        
        for cote_key, outcome in outcomes.items():
            if cote_key in cotes:
                Odd.objects.create(
                    match=match,
                    market=market,
                    bookmaker=bookmaker,
                    outcome=outcome,
                    odd_value=cotes[cote_key],
                    trj=trj,
                    scraped_at=scraped_at
                )
                odds_count += 1
        
        print(f"{odds_count} odds saved (TRJ: {trj}%)")
        
        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()
        # Acknowledge anyway to avoid infinite loop
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    """Start consumer in worker mode"""
    print("Starting odds consumer...")
    print(f"Connecting to RabbitMQ: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=int(RABBITMQ_PORT),
            credentials=credentials
        )
    )
    channel = connection.channel()
    
    # Declare queue (same as your scraper)
    channel.queue_declare(queue='odds', durable=True)
    
    print("Listening on queue 'odds'...")
    print("Waiting for messages. To exit press CTRL+C")
    
    # Start consuming
    channel.basic_consume(
        queue='odds',
        on_message_callback=callback,
        auto_ack=False
    )
    
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()