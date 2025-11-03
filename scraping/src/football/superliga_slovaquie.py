# scraping/src/football/superliga_slovaquie.py

from ._scraper_utils import scrape_league


def scrape_superliga_slovaquie():
    """Scrape Superliga Slovaquie"""
    return scrape_league(
        league_name="Superliga Slovaquie",
        league_url="https://www.coteur.com/cotes/foot/slovaquie/superliga-1",
        display_name="Superliga Slovaquie"
    )
