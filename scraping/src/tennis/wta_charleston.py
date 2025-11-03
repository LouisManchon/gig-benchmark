# scraping/src/tennis/wta_charleston.py

from ._scraper_utils import scrape_league


def scrape_wta_charleston():
    """Scrape WTA Charleston"""
    return scrape_league(
        league_name="WTA Charleston",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-charleston",
        display_name="WTA Charleston"
    )
