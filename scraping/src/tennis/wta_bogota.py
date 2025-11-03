# scraping/src/tennis/wta_bogota.py

from ._scraper_utils import scrape_league


def scrape_wta_bogota():
    """Scrape WTA Bogota"""
    return scrape_league(
        league_name="WTA Bogota",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-bogota",
        display_name="WTA Bogota"
    )
