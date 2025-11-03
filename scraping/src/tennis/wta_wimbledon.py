# scraping/src/tennis/wta_wimbledon.py

from ._scraper_utils import scrape_league


def scrape_wta_wimbledon():
    """Scrape WTA Wimbledon"""
    return scrape_league(
        league_name="WTA Wimbledon",
        league_url="https://www.coteur.com/cotes/tennis/monde/wimbledon-simples-dames",
        display_name="WTA Wimbledon"
    )
