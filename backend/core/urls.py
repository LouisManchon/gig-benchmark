from django.urls import path
from .views import data_views, scraping_views

urlpatterns = [
    path('scraping/health', scraping_views.health_check, name='scraping-health'),
    path('scraping/scrapers', scraping_views.list_scrapers, name='list-scrapers'),
    path('scraping/trigger', scraping_views.trigger_scraping, name='trigger-scraping'),
    # path('scraping/trigger-multiple', data_views.trigger_multiple_scraping, name='trigger-multiple'),
    # path('scraping/all', scraping_views.datascrape_all, name='scrape-all'),
    path('scraping/football/all', scraping_views.scrape_all_football, name='scrape-football'),
    path('scraping/basketball/all', scraping_views.scrape_all_basketball, name='scrape-basketball'),
    path('scraping/rugby/all', scraping_views.scrape_all_rugby, name='scrape-rugby'),
    path('scraping/tennis/all', scraping_views.scrape_all_tennis, name='scrape-tennis'),
    path('sports', data_views.get_distinct_sports),
    path('bookmakers', data_views.get_distinct_bookmakers),
    path('leagues', data_views.get_distinct_leagues),
    path('matches', data_views.get_distinct_matches),
    path('odds', data_views.get_odds_with_filters),
    path('avg-trj', data_views.get_avg_trj),
]