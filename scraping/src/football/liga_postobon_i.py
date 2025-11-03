# scraping/src/football/liga_postobon_i.py

from ._scraper_utils import scrape_league


def scrape_liga_postobon_i():
    """Scrape Liga Postobon I"""
    return scrape_league(
        league_name="Liga Postobon I",
        league_url="https://www.coteur.com/cotes/foot/colombie/liga-postobon-i",
        display_name="Liga Postobon I"
    )
