# core/views/data_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Q, Max
from django.db.models.functions import TruncHour, TruncMinute
from django.utils import timezone
from datetime import datetime
from ..models import Odd, Bookmaker, League, Match, Sport
from ..serializers import OddSerializer, BookmakerSerializer, LeagueSerializer, MatchSerializer, SportSerializer
import traceback



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

# core/views/data_views.py

@api_view(['GET'])
def get_odds_with_evolution(request):
    """
    Récupère les cotes avec l'évolution du TRJ par rapport au scraping précédent
    """
    try:
        sport_id = request.query_params.get('sport')
        bookmaker_id = request.query_params.get('bookmaker')
        league_id = request.query_params.get('league')
        match_id = request.query_params.get('match')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        # Récupère les dernières cotes (scraping le plus récent)
        latest_odds = Odd.objects.select_related(
            'match__league__sport',
            'match__home_team',
            'match__away_team',
            'bookmaker',
            'market'
        ).all()
        
        # Applique les filtres
        if sport_id and sport_id != 'all':
            latest_odds = latest_odds.filter(match__league__sport__id=int(sport_id))
        if bookmaker_id and bookmaker_id != 'all':
            bookmaker_ids = [int(bid) for bid in bookmaker_id.split(',')]
            latest_odds = latest_odds.filter(bookmaker__id__in=bookmaker_ids)
        if league_id and league_id != 'all':
            league_ids = [int(lid) for lid in league_id.split(',')]
            latest_odds = latest_odds.filter(match__league__id__in=league_ids)
        if match_id and match_id != 'all':
            latest_odds = latest_odds.filter(match__id=match_id)
        if start_date and end_date:
            start_dt = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
            end_dt = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
            latest_odds = latest_odds.filter(match__match_date__range=[start_dt, end_dt])

        # Récupère seulement les plus récentes pour chaque match/bookmaker/outcome
        from django.db.models import Max
        
        latest_scraped = latest_odds.values('match_id', 'bookmaker_id', 'outcome').annotate(
            max_scraped=Max('scraped_at')
        )
        
        # Construire un dictionnaire pour la recherche rapide
        latest_lookup = {}
        for item in latest_scraped:
            key = f"{item['match_id']}_{item['bookmaker_id']}_{item['outcome']}"
            latest_lookup[key] = item['max_scraped']
        
        # Filtrer les odds pour ne garder que les plus récents
        result_odds = []
        for odd in latest_odds:
            key = f"{odd.match_id}_{odd.bookmaker_id}_{odd.outcome}"
            if key in latest_lookup and odd.scraped_at == latest_lookup[key]:
                # Récupère le TRJ précédent (avant-dernier scraping)
                previous_odd = Odd.objects.filter(
                    match_id=odd.match_id,
                    bookmaker_id=odd.bookmaker_id,
                    outcome=odd.outcome,
                    scraped_at__lt=odd.scraped_at
                ).order_by('-scraped_at').first()
                
                odd_data = OddSerializer(odd).data
                odd_data['previous_trj'] = previous_odd.trj if previous_odd else None
                odd_data['previous_scraped_at'] = previous_odd.scraped_at.isoformat() if previous_odd else None
                
                result_odds.append(odd_data)
        
        return Response(result_odds[:1000])  # Limite à 1000 résultats
    
    except Exception as e:
        print(f"Error in get_odds_with_evolution: {str(e)}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def get_avg_trj_with_evolution(request):
    """
    Récupère les moyennes TRJ avec évolution par bookmaker
    """
    try:
        sport_id = request.query_params.get('sport')
        bookmaker_id = request.query_params.get('bookmaker')
        league_id = request.query_params.get('league')
        match_id = request.query_params.get('match')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        # Base queryset avec tous les filtres
        odds = Odd.objects.select_related('bookmaker', 'match__league__sport')
        
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

        # ✅ Récupère les 2 dernières HEURES de scraping (pas les secondes exactes)
        distinct_hours = odds.annotate(
            scraped_hour=TruncHour('scraped_at')
        ).values('scraped_hour').distinct().order_by('-scraped_hour')[:2]
        
        if not distinct_hours or len(distinct_hours) == 0:
            print("❌ Aucune donnée de scraping trouvée")
            return Response([])
        
        latest_hour = distinct_hours[0]['scraped_hour']
        previous_hour = distinct_hours[1]['scraped_hour'] if len(distinct_hours) > 1 else None

        print(f"📅 Latest scraping hour: {latest_hour}")
        print(f"📅 Previous scraping hour: {previous_hour}")

        # Calcule la moyenne pour la dernière heure de scraping
        current_avg = odds.annotate(
            scraped_hour=TruncHour('scraped_at')
        ).filter(scraped_hour=latest_hour).values(
            'bookmaker__id', 'bookmaker__name'
        ).annotate(avg_trj=Avg('trj'))

        print(f"📊 Current avg - Nombre de bookmakers: {current_avg.count()}")

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

        # Combine les résultats
        result = []
        for item in current_avg:
            bookmaker_id_val = item['bookmaker__id']
            current_avg_trj = float(item['avg_trj']) if item['avg_trj'] else 0
            previous_avg_trj = float(previous_avg_dict.get(bookmaker_id_val, 0)) if bookmaker_id_val in previous_avg_dict else None
            
            result.append({
                'bookmaker__name': item['bookmaker__name'],
                'avg_trj': round(current_avg_trj, 2),
                'previous_avg_trj': round(previous_avg_trj, 2) if previous_avg_trj else None,
            })
        
        print(f"✅ Résultat final - {len(result)} bookmakers:")
        for item in result:
            print(f"   - {item['bookmaker__name']}: {item['avg_trj']}% (previous: {item['previous_avg_trj']}%)")
        
        return Response(result)
    
    except Exception as e:
        print(f"❌ Error in get_avg_trj_with_evolution: {str(e)}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)
