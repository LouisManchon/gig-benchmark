# scraping/src/football/primeira_liga.py

from ._scraper_utils import scrape_league


def scrape_primeira_liga():
    """Scrape Primeira Liga"""
    return scrape_league(
        league_name="Primeira Liga",
        league_url="https://www.coteur.com/cotes/foot/portugal/primeira-liga",
        display_name="Primeira Liga"
    )
