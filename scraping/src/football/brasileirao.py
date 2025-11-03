# scraping/src/football/brasileirao.py

from ._scraper_utils import scrape_league


def scrape_brasileirao():
    """Scrape Brasileirao"""
    return scrape_league(
        league_name="Brasileirao",
        league_url="https://www.coteur.com/cotes/foot/bresil/serie-a-1",
        display_name="Brasileirao"
    )
