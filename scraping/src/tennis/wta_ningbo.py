# scraping/src/tennis/wta_ningbo.py

from ._scraper_utils import scrape_league


def scrape_wta_ningbo():
    """Scrape WTA Ningbo"""
    return scrape_league(
        league_name="WTA Ningbo",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-ningbo",
        display_name="WTA Ningbo"
    )
