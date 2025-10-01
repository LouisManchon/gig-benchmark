from rest_framework import viewsets
from rest_framework import permissions
from django.db.models import Prefetch
from .models import Sport, MarketName, League, Team, Player, Odds
from .serializers import (
    SportSerializer, MarketNameSerializer, LeagueSerializer,
    TeamSerializer, PlayerSerializer, OddsSerializer
)

class BaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Classe de base pour toutes les vues en lecture seule."""
    permission_classes = [permissions.IsAuthenticated]

class SportViewSet(BaseReadOnlyViewSet):
    queryset = Sport.objects.all().order_by('name')  # Tri alphabétique
    serializer_class = SportSerializer

class MarketNameViewSet(BaseReadOnlyViewSet):
    queryset = MarketName.objects.select_related('sport').all().order_by('name')
    serializer_class = MarketNameSerializer

class LeagueViewSet(BaseReadOnlyViewSet):
    queryset = League.objects.select_related('sport').all().order_by('name')
    serializer_class = LeagueSerializer

class TeamViewSet(BaseReadOnlyViewSet):
    queryset = Team.objects.select_related('league').prefetch_related(
        Prefetch('league__sport', queryset=Sport.objects.only('id', 'name'))
    ).all().order_by('name')
    serializer_class = TeamSerializer

class PlayerViewSet(BaseReadOnlyViewSet):
    queryset = Player.objects.select_related('team').prefetch_related(
        Prefetch('team__league', queryset=League.objects.only('id', 'name'))
    ).all().order_by('name')
    serializer_class = PlayerSerializer

class OddsViewSet(BaseReadOnlyViewSet):
    queryset = Odds.objects.select_related(
        'home_team', 'away_team', 'championship'
    ).prefetch_related(
        Prefetch('home_team__league', queryset=League.objects.only('id', 'name')),
        Prefetch('away_team__league', queryset=League.objects.only('id', 'name')),
        Prefetch('championship__sport', queryset=Sport.objects.only('id', 'name'))
    ).all().order_by('-date')  # Tri par date décroissante (plus récent en premier)
    serializer_class = OddsSerializer
