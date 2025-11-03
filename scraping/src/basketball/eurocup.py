# scraping/src/basketball/eurocup.py

from ._scraper_utils import scrape_league


def scrape_eurocup():
    """Scrape Eurocup"""
    return scrape_league(
        league_name="Eurocup",
        league_url="https://www.coteur.com/cotes/basket/europe/eurocup-hommes",
        display_name="Eurocup"
    )
