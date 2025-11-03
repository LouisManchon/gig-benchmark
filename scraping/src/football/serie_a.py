# scraping/src/football/serie_a.py

from ._scraper_utils import scrape_league


def scrape_serie_a():
    """Scrape Serie A"""
    return scrape_league(
        league_name="Serie A",
        league_url="https://www.coteur.com/cotes/foot/italie/serie-a",
        display_name="Serie A"
    )
