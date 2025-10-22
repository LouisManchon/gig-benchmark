from django.contrib import admin
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.views import public_endpoint
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,  # ← Ajout pour vérifier un token
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core.views import (
    SportViewSet, MarketNameViewSet, LeagueViewSet,
    TeamViewSet, PlayerViewSet, OddsViewSet  # ← Ajout de OddsViewSet
)

def test_log(request):  # ✅ Doit être ici, avant urlpatterns
    return JsonResponse({"status": "success", "message": "Test log endpoint"})

@api_view(['GET'])
@authentication_classes([])  # ← Désactive toute authentification
@permission_classes([AllowAny])  # ← Autorise l'accès sans token
def public_endpoint(request):
    """Endpoint public accessible sans authentification."""
    return Response({"message": "Public endpoint - No auth required"})

# Configuration de Swagger (sécurisé avec IsAuthenticated)
schema_view = get_schema_view(
    openapi.Info(
        title="Gig Benchmark API",
        default_version='v1',
        description="API pour le projet Gig Benchmark (nécessite une authentification)",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Swagger est public
)

# Configuration du router avec basename explicite
router = DefaultRouter()
router.register(r'sports', SportViewSet, basename='sport')
router.register(r'market-names', MarketNameViewSet, basename='marketname')
router.register(r'leagues', LeagueViewSet, basename='league')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'odds', OddsViewSet, basename='odds')  # ← Ajout de la route pour Odds

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # ← Ajout de la version v1

    # Routes publiques (sans préfixe api/v1/ pour simplifier les tests)
    path('api/public/', public_endpoint, name='public-endpoint'),

    path('test-log/', test_log),

    # Routes pour Swagger (protégées)
    path('api/docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
