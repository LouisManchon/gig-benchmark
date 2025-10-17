# core/views/data_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
from ..models import Odd, Bookmaker, League, Match
from ..serializers import OddSerializer, BookmakerSerializer, LeagueSerializer, MatchSerializer

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
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_odds_with_filters(request):
    # Récupère les filtres depuis les query params
    bookmaker_id = request.query_params.get('bookmaker')
    league_id = request.query_params.get('league')
    match_id = request.query_params.get('match')
    start_date = request.query_params.get('start')
    end_date = request.query_params.get('end')

    # Construis la requête avec les filtres
    odds = Odd.objects.all()
    if bookmaker_id:
        odds = odds.filter(bookmaker__id=bookmaker_id)
    if league_id:
        odds = odds.filter(match__league__id=league_id)
    if match_id:
        odds = odds.filter(match__id=match_id)
    if start_date and end_date:
        odds = odds.filter(scraped_at__range=[start_date, end_date])

    # Sérialise les résultats
    serializer = OddSerializer(odds, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_avg_trj(request):
    bookmaker_id = request.query_params.get('bookmaker')
    league_id = request.query_params.get('league')
    match_id = request.query_params.get('match')
    start_date = request.query_params.get('start')
    end_date = request.query_params.get('end')

    # Construis la requête avec les filtres
    odds = Odd.objects.all()
    if bookmaker_id:
        odds = odds.filter(bookmaker__id=bookmaker_id)
    if league_id:
        odds = odds.filter(match__league__id=league_id)
    if match_id:
        odds = odds.filter(match__id=match_id)
    if start_date and end_date:
        odds = odds.filter(scraped_at__range=[start_date, end_date])

    # Calcule la moyenne du TRJ par bookmaker
    avg_trj = odds.values('bookmaker__name').annotate(avg_trj=Avg('trj'))
    return Response(avg_trj)