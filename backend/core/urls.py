from django.urls import path
from core.views.scraping_views import (
    health_check,
    list_scrapers,
    trigger_scraping,
    trigger_multiple_scraping,
    scrape_all,
    scrape_all_football,
    scrape_all_basketball,
    scrape_all_rugby,
    scrape_all_tennis
)

urlpatterns = [
    path('scraping/health', health_check, name='scraping-health'),
    path('scraping/scrapers', list_scrapers, name='list-scrapers'),
    path('scraping/trigger', trigger_scraping, name='trigger-scraping'),
    path('scraping/trigger-multiple', trigger_multiple_scraping, name='trigger-multiple'),
    path('scraping/all', scrape_all, name='scrape-all'),
    path('scraping/football/all', scrape_all_football, name='scrape-football'),
    path('scraping/basketball/all', scrape_all_basketball, name='scrape-basketball'),
    path('scraping/rugby/all', scrape_all_rugby, name='scrape-rugby'),
    path('scraping/tennis/all', scrape_all_tennis, name='scrape-tennis'),
]