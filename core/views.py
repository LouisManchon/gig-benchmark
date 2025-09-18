from rest_framework import viewsets
from .models import Sport, MarketName, League, Team, Player
from .serializers import (
    SportSerializer, MarketNameSerializer, LeagueSerializer, TeamSerializer, PlayerSerializer
)

class SportViewSet(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

class MarketNameViewSet(viewsets.ModelViewSet):
    queryset = MarketName.objects.all()
    serializer_class = MarketNameSerializer

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
