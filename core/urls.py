from django.urls import path
from . import views

urlpatterns = [
    path('sports/', views.SportList.as_view(), name='sports_list'),
    path('sports/<int:pk>/', views.SportDetail.as_view(), name='sport_detail'),

    path('leagues/', views.LeagueList.as_view(), name='leagues_list'),
    path('leagues/<int:pk>/', views.LeagueDetail.as_view(), name='league_detail'),

    path('teams/', views.TeamList.as_view(), name='teams_list'),
    path('teams/<int:pk>/', views.TeamDetail.as_view(), name='team_detail'),

    path('players/', views.PlayerList.as_view(), name='players_list'),
    path('players/<int:pk>/', views.PlayerDetail.as_view(), name='player_detail'),

    path('markets/', views.MarketNameList.as_view(), name='markets_list'),
    path('markets/<int:pk>/', views.MarketNameDetail.as_view(), name='market_detail'),

    path('test/', views.test_api, name='test_api'),
]
