# scraping/src/tennis/wta_rouen.py

from ._scraper_utils import scrape_league


def scrape_wta_rouen():
    """Scrape WTA Rouen"""
    return scrape_league(
        league_name="WTA Rouen",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/wta-rouen",
        display_name="WTA Rouen"
    )
