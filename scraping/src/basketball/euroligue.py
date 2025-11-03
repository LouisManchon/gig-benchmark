# scraping/src/basketball/euroligue.py

from ._scraper_utils import scrape_league


def scrape_euroligue():
    """Scrape Euroligue"""
    return scrape_league(
        league_name="Euroligue",
        league_url="https://www.coteur.com/cotes/basket/europe/euroligue",
        display_name="Euroligue"
    )
