# scraping/src/basketball/serie_a2.py

from ._scraper_utils import scrape_league


def scrape_serie_a2():
    """Scrape Serie A2"""
    return scrape_league(
        league_name="Serie A2",
        league_url="https://www.coteur.com/cotes/basket/italie/serie-a2",
        display_name="Serie A2"
    )
