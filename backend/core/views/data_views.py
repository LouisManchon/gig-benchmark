# core/views/data_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Avg, Q, Max, Subquery, OuterRef
from django.db.models.functions import TruncHour, TruncMinute
from django.utils import timezone
from datetime import datetime
from ..models import Odd, Bookmaker, League, Match, Sport
from ..serializers import OddSerializer, BookmakerSerializer, LeagueSerializer, MatchSerializer, SportSerializer
import traceback
import time


@api_view(['GET'])
def get_distinct_sports(request):
    sports = Sport.objects.all()
    serializer = SportSerializer(sports, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_distinct_bookmakers(request):
    bookmakers = Bookmaker.objects.all()
    serializer = BookmakerSerializer(bookmakers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_distinct_leagues(request):
    leagues = League.objects.all()
    serializer = LeagueSerializer(leagues, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_distinct_matches(request):
    # Récupère les matchs distincts depuis Odds
    match_ids = Odd.objects.values_list('match_id', flat=True).distinct()
    matches = Match.objects.filter(id__in=match_ids)
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_odds_with_filters(request):
    try:
        sport_id = request.query_params.get('sport')
        bookmaker_id = request.query_params.get('bookmaker')
        league_id = request.query_params.get('league')
        match_id = request.query_params.get('match')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        odds = Odd.objects.select_related(
            'match__league__sport',
            'match__home_team',
            'match__away_team',
            'bookmaker',
            'market'
        ).all()
        
        # Applique les filtres
        if sport_id and sport_id != 'all':
            odds = odds.filter(match__league__sport__id=int(sport_id))
        if bookmaker_id and bookmaker_id != 'all':
            bookmaker_ids = [int(bid) for bid in bookmaker_id.split(',')]  # ✅ Convertir en int
            odds = odds.filter(bookmaker__id__in=bookmaker_ids)
        if league_id and league_id != 'all':
            league_ids = [int(lid) for lid in league_id.split(',')]  # ✅ Convertir en int
            odds = odds.filter(match__league__id__in=league_ids)
        if match_id and match_id != 'all':
            odds = odds.filter(match__id=match_id)
        if start_date and end_date:
            # ✅ Filtrer sur match__match_date au lieu de scraped_at
            start_dt = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
            end_dt = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
            odds = odds.filter(match__match_date__range=[start_dt, end_dt])

        odds = odds.order_by('-scraped_at')[:1000]
        serializer = OddSerializer(odds, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def get_avg_trj(request):
    try:
        sport_id = request.query_params.get('sport')
        bookmaker_id = request.query_params.get('bookmaker')
        league_id = request.query_params.get('league')
        match_id = request.query_params.get('match')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        odds = Odd.objects.select_related('bookmaker', 'match__league__sport').all()
        
        if sport_id and sport_id != 'all':
            odds = odds.filter(match__league__sport__id=int(sport_id))
        if bookmaker_id and bookmaker_id != 'all':
            bookmaker_ids = [int(bid) for bid in bookmaker_id.split(',')]
            odds = odds.filter(bookmaker__id__in=bookmaker_ids)
        if league_id and league_id != 'all':
            league_ids = [int(lid) for lid in league_id.split(',')]
            odds = odds.filter(match__league__id__in=league_ids)
        if match_id and match_id != 'all':
            odds = odds.filter(match__id=match_id)
        if start_date and end_date:
            # ✅ Filtrer sur match__match_date
            start_dt = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
            end_dt = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
            odds = odds.filter(match__match_date__range=[start_dt, end_dt])

        # Calcule la moyenne du TRJ par bookmaker
        avg_trj = odds.values('bookmaker__name').annotate(avg_trj=Avg('trj'))
        
        return Response(list(avg_trj))
    
    except Exception as e:
        print(f"Error in get_avg_trj: {str(e)}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_odds_with_evolution(request):
    """
    Récupère les cotes avec l'évolution - VERSION SIMPLIFIÉE
    """
    try:
        start_time = time.time()
        print("🔍 get_odds_with_evolution - START")
        
        # Filtres
        sport_id = request.query_params.get('sport')
        bookmaker_id = request.query_params.get('bookmaker')
        league_id = request.query_params.get('league')
        match_id = request.query_params.get('match')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        
        print(f"   Filters: sport={sport_id}, bookmaker={bookmaker_id}")
        
        # Base queryset
        odds = Odd.objects.select_related(
            'match__league__sport',
            'match__home_team',
            'match__away_team',
            'bookmaker',
            'market'
        )
        
        # Applique les filtres
        if sport_id and sport_id != 'all':
            odds = odds.filter(match__league__sport__id=int(sport_id))
        
        if bookmaker_id and bookmaker_id != 'all':
            bookmaker_ids = [int(bid) for bid in bookmaker_id.split(',')]
            odds = odds.filter(bookmaker__id__in=bookmaker_ids)
        
        if league_id and league_id != 'all':
            league_ids = [int(lid) for lid in league_id.split(',')]
            odds = odds.filter(match__league__id__in=league_ids)
        
        if match_id and match_id != 'all':
            odds = odds.filter(match__id=int(match_id))
        
        if start_date and end_date:
            start_dt = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
            end_dt = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
            odds = odds.filter(match__match_date__range=[start_dt, end_dt])
        
        print(f"⏱️ Filters applied: {time.time() - start_time:.2f}s")
        
        # ✅ Récupère les dernières cotes pour chaque (match, bookmaker, outcome)
        latest_scraped = odds.values('match_id', 'bookmaker_id', 'outcome').annotate(
            max_scraped=Max('scraped_at')
        )
        
        latest_scraped_list = list(latest_scraped)  # Force l'évaluation
        print(f"⏱️ Max scraped calculated: {time.time() - start_time:.2f}s - {len(latest_scraped_list)} combinations")
        
        # Crée un dict pour lookup rapide
        latest_lookup = {}
        for item in latest_scraped_list:
            key = f"{item['match_id']}_{item['bookmaker_id']}_{item['outcome']}"
            latest_lookup[key] = item['max_scraped']
        
        # ✅ Récupère les odds et filtre en Python
        odds_to_check = odds.order_by('-scraped_at')
        
        latest_odds = []
        for odd in odds_to_check:
            key = f"{odd.match_id}_{odd.bookmaker_id}_{odd.outcome}"
            if key in latest_lookup and odd.scraped_at == latest_lookup[key]:
                latest_odds.append(odd)
        
        print(f"⏱️ Latest odds filtered: {time.time() - start_time:.2f}s - Count: {len(latest_odds)}")
        
        # ✅ Récupère les cotes précédentes
        result_odds = []
        for odd in latest_odds:
            # Cherche la cote précédente
            previous_odd = Odd.objects.filter(
                match_id=odd.match_id,
                bookmaker_id=odd.bookmaker_id,
                outcome=odd.outcome,
                scraped_at__lt=odd.scraped_at
            ).order_by('-scraped_at').first()
            
            # ✅ Sérialisation manuelle
            odd_data = {
                'id': odd.id,
                'match': {
                    'id': odd.match.id,
                    'home_team': {'name': odd.match.home_team.name},
                    'away_team': {'name': odd.match.away_team.name},
                    'sport': {'name': odd.match.league.sport.name},
                    'league': {'name': odd.match.league.name},
                    'match_date': odd.match.match_date.isoformat() if odd.match.match_date else None,
                },
                'bookmaker': {'id': odd.bookmaker.id, 'name': odd.bookmaker.name},
                'outcome': odd.outcome,
                'odd_value': float(odd.odd_value) if odd.odd_value else None,
                'trj': float(odd.trj) if odd.trj else None,
                'scraped_at': odd.scraped_at.isoformat(),
                'previous_trj': float(previous_odd.trj) if previous_odd and previous_odd.trj else None,
                'previous_scraped_at': previous_odd.scraped_at.isoformat() if previous_odd else None,
            }
            
            result_odds.append(odd_data)
        
        print(f"⏱️ Response built: {time.time() - start_time:.2f}s")
        print(f"✅ TOTAL TIME: {time.time() - start_time:.2f}s")
        print(f"✅ Returning {len(result_odds)} odds")
        
        return Response(result_odds)
    
    except Exception as e:
        print(f"❌ Error in get_odds_with_evolution: {str(e)}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_avg_trj_with_evolution(request):
    """
    Récupère les moyennes TRJ avec évolution par bookmaker
    VERSION OPTIMISÉE
    """
    try:
        start_time = time.time()
        print("🔍 get_avg_trj_with_evolution - START")
        
        # Récupération des filtres
        sport_id = request.query_params.get('sport')
        bookmaker_id = request.query_params.get('bookmaker')
        league_id = request.query_params.get('league')
        match_id = request.query_params.get('match')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        
        # ✅ Base queryset optimisé
        odds = Odd.objects.select_related('bookmaker', 'match__league__sport')
        
        # Applique les filtres
        if sport_id and sport_id != 'all':
            odds = odds.filter(match__league__sport__id=int(sport_id))
        
        if bookmaker_id and bookmaker_id != 'all':
            bookmaker_ids = [int(bid) for bid in bookmaker_id.split(',')]
            odds = odds.filter(bookmaker__id__in=bookmaker_ids)
        
        if league_id and league_id != 'all':
            league_ids = [int(lid) for lid in league_id.split(',')]
            odds = odds.filter(match__league__id__in=league_ids)
        
        if match_id and match_id != 'all':
            odds = odds.filter(match__id=int(match_id))
        
        if start_date and end_date:
            start_dt = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
            end_dt = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
            odds = odds.filter(match__match_date__range=[start_dt, end_dt])
        
        print(f"⏱️ Filters applied: {time.time() - start_time:.2f}s")
        
        # ✅ Récupère les 2 dernières HEURES de scraping
        distinct_hours = odds.annotate(
            scraped_hour=TruncHour('scraped_at')
        ).values('scraped_hour').distinct().order_by('-scraped_hour')[:2]
        
        distinct_hours_list = list(distinct_hours)
        
        if not distinct_hours_list:
            print("❌ Aucune donnée de scraping trouvée")
            return Response([])
        
        latest_hour = distinct_hours_list[0]['scraped_hour']
        previous_hour = distinct_hours_list[1]['scraped_hour'] if len(distinct_hours_list) > 1 else None
        
        print(f"📅 Latest scraping hour: {latest_hour}")
        print(f"📅 Previous scraping hour: {previous_hour}")
        print(f"⏱️ Hours fetched: {time.time() - start_time:.2f}s")
        
        # ✅ Calcule les moyennes en UNE requête pour les deux périodes
        current_avg = odds.annotate(
            scraped_hour=TruncHour('scraped_at')
        ).filter(scraped_hour=latest_hour).values(
            'bookmaker__id', 'bookmaker__name'
        ).annotate(avg_trj=Avg('trj'))
        
        current_avg_list = list(current_avg)
        print(f"📊 Current avg - Nombre de bookmakers: {len(current_avg_list)}")
        print(f"⏱️ Current avg calculated: {time.time() - start_time:.2f}s")
        
        # Calcule la moyenne pour l'avant-dernière heure
        previous_avg_dict = {}
        if previous_hour:
            previous_avg = odds.annotate(
                scraped_hour=TruncHour('scraped_at')
            ).filter(scraped_hour=previous_hour).values(
                'bookmaker__id'
            ).annotate(avg_trj=Avg('trj'))
            
            previous_avg_dict = {item['bookmaker__id']: item['avg_trj'] for item in previous_avg}
            print(f"📊 Previous avg - Nombre de bookmakers: {len(previous_avg_dict)}")
        
        print(f"⏱️ Previous avg calculated: {time.time() - start_time:.2f}s")
        
        # ✅ Combine les résultats
        result = []
        for item in current_avg_list:
            bookmaker_id_val = item['bookmaker__id']
            current_avg_trj = float(item['avg_trj']) if item['avg_trj'] else 0
            previous_avg_trj = float(previous_avg_dict.get(bookmaker_id_val, 0)) if bookmaker_id_val in previous_avg_dict else None
            
            result.append({
                'bookmaker__name': item['bookmaker__name'],
                'avg_trj': round(current_avg_trj, 2),
                'previous_avg_trj': round(previous_avg_trj, 2) if previous_avg_trj else None,
            })
        
        print(f"⏱️ Response built: {time.time() - start_time:.2f}s")
        print(f"✅ TOTAL TIME: {time.time() - start_time:.2f}s")
        print(f"✅ Résultat final - {len(result)} bookmakers")
        
        return Response(result)
    
    except Exception as e:
        print(f"❌ Error in get_avg_trj_with_evolution: {str(e)}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)
