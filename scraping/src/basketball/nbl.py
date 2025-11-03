# scraping/src/basketball/nbl.py

from ._scraper_utils import scrape_league


def scrape_nbl():
    """Scrape NBL"""
    return scrape_league(
        league_name="NBL",
        league_url="https://www.coteur.com/cotes/basket/australie/nbl",
        display_name="NBL"
    )
