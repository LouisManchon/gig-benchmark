from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    SportViewSet, MarketNameViewSet, LeagueViewSet, TeamViewSet, PlayerViewSet
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Configuration de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Gig Benchmark API",
        default_version='v1',
        description="API pour le projet Gig Benchmark",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Configuration des routes API
router = DefaultRouter()
router.register(r'sports', SportViewSet)
router.register(r'market-names', MarketNameViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Toutes les routes API sous /api/
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Routes pour Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
