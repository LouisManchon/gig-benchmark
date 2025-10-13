from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db.models import Prefetch
from .models import Sport, MarketName, League, Team, Player, Odds
from .serializers import (
    SportSerializer, MarketNameSerializer, LeagueSerializer,
    TeamSerializer, PlayerSerializer, OddsSerializer
)
from core.keycloak_auth import KeycloakAuthentication

class BaseViewSet(viewsets.ModelViewSet):
    """
    Classe de base avec permissions différenciées :
    - GET/HEAD/OPTIONS : Users + Admins
    - POST/PUT/PATCH/DELETE : Admins seulement
    """
    permission_classes = [permissions.IsAuthenticated]  # Base: authentification requise

    def check_permissions(self, request):
        """Surcharge pour vérifier les rôles Keycloak."""
        super().check_permissions(request)

        # Récupérer les rôles depuis le token JWT
        roles = request.auth.get('resource_access', {}).get('gig-api', {}).get('roles', [])

        # Autoriser GET/HEAD/OPTIONS pour les users et admins
        if request.method in permissions.SAFE_METHODS:
            if not ('user' in roles or 'admin' in roles):
                raise PermissionDenied("Vous devez être un utilisateur ou admin pour accéder à cette ressource.")
        # Limiter POST/PUT/PATCH/DELETE aux admins
        else:
            if 'admin' not in roles:
                raise PermissionDenied("Seuls les admins peuvent modifier ou supprimer des données.")

    def get_permissions(self):
        """Garantit que IsAuthenticated est toujours appliqué."""
        return [permission() for permission in self.permission_classes]

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
