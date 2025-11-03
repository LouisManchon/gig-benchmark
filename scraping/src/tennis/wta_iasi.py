# scraping/src/tennis/wta_iasi.py

from ._scraper_utils import scrape_league


def scrape_wta_iasi():
    """Scrape WTA Iasi"""
    return scrape_league(
        league_name="WTA Iasi",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/wta-iasi",
        display_name="WTA Iasi"
    )
