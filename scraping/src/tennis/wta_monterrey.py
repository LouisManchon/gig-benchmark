# scraping/src/tennis/wta_monterrey.py

from ._scraper_utils import scrape_league


def scrape_wta_monterrey():
    """Scrape WTA Monterrey"""
    return scrape_league(
        league_name="WTA Monterrey",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-monterrey",
        display_name="WTA Monterrey"
    )
