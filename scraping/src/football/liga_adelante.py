# scraping/src/football/liga_adelante.py

from ._scraper_utils import scrape_league


def scrape_liga_adelante():
    """Scrape Liga Adelante"""
    return scrape_league(
        league_name="Liga Adelante",
        league_url="https://www.coteur.com/cotes/foot/espagne/liga-adelante",
        display_name="Liga Adelante"
    )
