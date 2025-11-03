# scraping/src/tennis/wta_guangzhou.py

from ._scraper_utils import scrape_league


def scrape_wta_guangzhou():
    """Scrape WTA Guangzhou"""
    return scrape_league(
        league_name="WTA Guangzhou",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-guangzhou",
        display_name="WTA Guangzhou"
    )
