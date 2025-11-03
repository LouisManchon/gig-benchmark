# scraping/src/tennis/wta_wuhan.py

from ._scraper_utils import scrape_league


def scrape_wta_wuhan():
    """Scrape WTA Wuhan"""
    return scrape_league(
        league_name="WTA Wuhan",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-wuhan",
        display_name="WTA Wuhan"
    )
