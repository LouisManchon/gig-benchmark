# scraping/src/football/primera_division_paraguay.py

from ._scraper_utils import scrape_league


def scrape_primera_division_paraguay():
    """Scrape Primera Division Paraguay"""
    return scrape_league(
        league_name="Primera Division Paraguay",
        league_url="https://www.coteur.com/cotes/foot/paraguay/primera-division-1",
        display_name="Primera Division Paraguay"
    )
