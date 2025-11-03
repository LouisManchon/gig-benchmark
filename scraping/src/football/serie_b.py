# scraping/src/football/serie_b.py

from ._scraper_utils import scrape_league


def scrape_serie_b():
    """Scrape Serie B"""
    return scrape_league(
        league_name="Serie B",
        league_url="https://www.coteur.com/cotes/foot/italie/serie-b",
        display_name="Serie B"
    )
