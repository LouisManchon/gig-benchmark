from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db.models import Prefetch
from .models import Sport, MarketName, League, Team, Player, Odds
from .serializers import (
    SportSerializer, MarketNameSerializer, LeagueSerializer,
    TeamSerializer, PlayerSerializer, OddsSerializer
)
from core.keycloak_auth import (
    KeycloakAuthentication,
    IsKeycloakAdmin,
    IsKeycloakUser
)

class BaseViewSet(viewsets.ModelViewSet):
    """
    Classe de base avec permissions différenciées :
    - GET/HEAD/OPTIONS : Users + Admins
    - POST/PUT/PATCH/DELETE : Admins seulement
    """
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAuthenticated]  # Base: authentification requise

    def get_permissions(self):
        """
        Applique des permissions dynamiques :
        - Lecture (GET) : IsKeycloakUser (user ou admin)
        - Écriture (POST/PUT/DELETE) : IsKeycloakAdmin (admin seulement)
        """
        if self.action in ['list', 'retrieve']:  # SAFE_METHODS
            return [IsKeycloakUser()]
        else:  # Méthodes non-sûres
            return [IsKeycloakAdmin()]

class SportViewSet(BaseViewSet):
    queryset = Sport.objects.all().order_by('name')
    serializer_class = SportSerializer

class MarketNameViewSet(BaseViewSet):
    queryset = MarketName.objects.select_related('sport').all().order_by('name')
    serializer_class = MarketNameSerializer

class LeagueViewSet(BaseViewSet):
    queryset = League.objects.select_related('sport').all().order_by('name')
    serializer_class = LeagueSerializer

class TeamViewSet(BaseViewSet):
    queryset = Team.objects.select_related('league').prefetch_related(
        Prefetch('league__sport', queryset=Sport.objects.only('id', 'name'))
    ).all().order_by('name')
    serializer_class = TeamSerializer

class PlayerViewSet(BaseViewSet):
    queryset = Player.objects.select_related('team').prefetch_related(
        Prefetch('team__league', queryset=League.objects.only('id', 'name'))
    ).all().order_by('name')
    serializer_class = PlayerSerializer

class OddsViewSet(BaseViewSet):
    queryset = Odds.objects.select_related(
        'home_team', 'away_team', 'championship'
    ).prefetch_related(
        Prefetch('home_team__league', queryset=League.objects.only('id', 'name')),
        Prefetch('away_team__league', queryset=League.objects.only('id', 'name')),
        Prefetch('championship__sport', queryset=Sport.objects.only('id', 'name'))
    ).all().order_by('-date')
    serializer_class = OddsSerializer
