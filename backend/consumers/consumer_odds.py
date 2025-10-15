"""
Consumer RabbitMQ pour stocker les cotes en BDD
"""
import sys
sys.path.insert(0, "/app")

import os
import django
import json
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.production'))
django.setup()

from celery import Celery
from core.models import Sport, League, Team, Match, MarketName, Odd, Bookmaker
from django.utils import timezone
import pika

app = Celery('gig_consumer')
app.config_from_object('django.conf:settings', namespace='CELERY')

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '5672')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'gig_user')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'gig_password_2025')


def get_bookmaker_code(bookmaker_name):
    mapping = {
        'Pmu': 'PMU', 'PMU': 'PMU',
        'ParionsSport': 'PARIONSSPORT',
        'Zebet': 'ZEBET', 'ZEbet': 'ZEBET',
        'Winamax': 'WINAMAX', 'Betclic': 'BETCLIC',
        'Betsson': 'BETSSON', 'Bwin': 'BWIN',
        'Unibet': 'UNIBET', 'Olybet': 'OLYBET', 'OlyBet': 'OLYBET',
        'Feelingbet': 'FEELINGBET', 'FeelingBet': 'FEELINGBET',
        'Genybet': 'GENYBET', 'Vbet': 'VBET',
        'Bet365': 'BET365', 'NetBet': 'NETBET',
        'Pinnacle': 'PINNACLE', 'Pokerstars Sport': 'POKERSTARS',
    }
    return mapping.get(bookmaker_name, bookmaker_name.upper())


def get_league_code(league_name):
    """Génère un code de league"""
    mapping = {
        'Ligue 1': 'LIGUE1',
        'Premier League': 'PREMIERLEAGUE',
        'La Liga': 'LALIGA',
        'Serie A': 'SERIEA',
        'Bundesliga': 'BUNDESLIGA',
    }
    return mapping.get(league_name, league_name.upper().replace(' ', ''))


def parse_team_names(match_str):
    try:
        teams = match_str.split(' - ')
        if len(teams) == 2:
            return teams[0].strip(), teams[1].strip()
        return None, None
    except:
        return None, None


def get_sport_code(sport_name):
    mapping = {
        'football': 'FOOT',
        'basketball': 'BASK',
        'tennis': 'TENN',
        'rugby': 'RUGB',
    }
    return mapping.get(sport_name.lower(), 'FOOT')


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(f"\n✅ {message.get('match')} - {message.get('bookmaker')}")
        
        match_str = message.get('match')
        bookmaker_name = message.get('bookmaker')
        cotes = message.get('cotes', {})
        trj = message.get('trj')
        league_name = message.get('league', 'Ligue 1')
        sport_name = message.get('sport', 'football')
        
        if not match_str or not bookmaker_name or not cotes:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 1. Sport
        sport_code = get_sport_code(sport_name)
        try:
            sport = Sport.objects.get(code=sport_code)
        except Sport.DoesNotExist:
            print(f"❌ Sport {sport_code} introuvable")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 2. League - AVEC CODE !
        league_code = get_league_code(league_name)
        league, created = League.objects.get_or_create(
            sport=sport,
            name=league_name,
            defaults={
                'code': league_code,  # ✅ AJOUT DU CODE
                'country': 'France'
            }
        )
        if created:
            print(f"🆕 Ligue: {league.name} ({league_code})")
        
        # 3. Teams
        home_team_name, away_team_name = parse_team_names(match_str)
        if not home_team_name or not away_team_name:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        home_team, _ = Team.objects.get_or_create(league=league, name=home_team_name)
        away_team, _ = Team.objects.get_or_create(league=league, name=away_team_name)
        
        # 4. Match
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
            print(f"🆕 Match: {home_team.name} vs {away_team.name}")
        
        # 5. Market
        try:
            market = MarketName.objects.get(sport=sport, code='1X2')
        except MarketName.DoesNotExist:
            print(f"❌ Market 1X2 introuvable")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 6. Bookmaker
        bookmaker_code = get_bookmaker_code(bookmaker_name)
        try:
            bookmaker = Bookmaker.objects.get(code=bookmaker_code)
        except Bookmaker.DoesNotExist:
            print(f"❌ Bookmaker {bookmaker_code} introuvable")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # 7. Odds
        scraped_at = timezone.now()
        odds_count = 0
        
        outcomes = {'cote_1': '1', 'cote_N': 'X', 'cote_2': '2'}
        
        for cote_key, outcome in outcomes.items():
            if cote_key in cotes and cotes[cote_key]:
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
        
        print(f"💾 {odds_count} cotes (TRJ: {trj}%)")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"❌ {e}")
        import traceback
        traceback.print_exc()
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    print("\n" + "="*60)
    print("CONSUMER ODDS")
    print("="*60)
    print(f"RabbitMQ: {RABBITMQ_HOST}:{RABBITMQ_PORT}\n")
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=int(RABBITMQ_PORT), credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='odds', durable=True)
    
    print("👂 En écoute...\n")
    
    channel.basic_consume(queue='odds', on_message_callback=callback, auto_ack=False)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == '__main__':
    start_consumer()
