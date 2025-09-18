from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    SportViewSet, MarketNameViewSet, LeagueViewSet, TeamViewSet, PlayerViewSet
)

router = DefaultRouter()
router.register(r'sports', SportViewSet)
router.register(r'market-names', MarketNameViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Toutes les routes API sous /api/
]
