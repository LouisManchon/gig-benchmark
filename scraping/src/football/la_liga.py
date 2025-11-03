# scraping/src/football/la_liga.py

from ._scraper_utils import scrape_league


def scrape_la_liga():
    """Scrape La Liga"""
    return scrape_league(
        league_name="La Liga",
        league_url="https://www.coteur.com/cotes/foot/espagne/liga-bbva",
        display_name="La Liga"
    )
