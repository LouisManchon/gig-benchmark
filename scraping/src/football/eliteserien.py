# scraping/src/football/eliteserien.py

from ._scraper_utils import scrape_league


def scrape_eliteserien():
    """Scrape Eliteserien"""
    return scrape_league(
        league_name="Eliteserien",
        league_url="https://www.coteur.com/cotes/foot/norvege/eliteserien",
        display_name="Eliteserien"
    )
