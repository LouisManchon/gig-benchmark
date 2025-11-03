# scraping/src/football/leagues_cup.py

from ._scraper_utils import scrape_league


def scrape_leagues_cup():
    """Scrape Leagues Cup"""
    return scrape_league(
        league_name="Leagues Cup",
        league_url="https://www.coteur.com/cotes/foot/monde-1/international-leagues-cup",
        display_name="Leagues Cup"
    )
