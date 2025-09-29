from rest_framework import viewsets
from .models import Sport, MarketName, League, Team, Player
from .serializers import (
    SportSerializer, MarketNameSerializer, LeagueSerializer, TeamSerializer, PlayerSerializer
)
from rest_framework import permissions

class SportViewSet(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [permissions.IsAuthenticated]

class MarketNameViewSet(viewsets.ModelViewSet):
    queryset = MarketName.objects.all()
    serializer_class = MarketNameSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]
