# scraping/src/football/ligue_1.py

from ._scraper_utils import scrape_league


def scrape_ligue_1():
    """Scrape Ligue 1"""
    return scrape_league(
        league_name="Ligue 1",
        league_url="https://www.coteur.com/cotes/foot/france/ligue-1",
        display_name="Ligue 1"
    )
