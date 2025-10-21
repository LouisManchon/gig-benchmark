# core/views/data_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Q
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
