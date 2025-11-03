# scraping/src/tennis/wta_hamburg.py

from ._scraper_utils import scrape_league


def scrape_wta_hamburg():
    """Scrape WTA Hamburg"""
    return scrape_league(
        league_name="WTA Hamburg",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-hambourg",
        display_name="WTA Hamburg"
    )
