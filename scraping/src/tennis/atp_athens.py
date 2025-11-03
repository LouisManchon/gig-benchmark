# scraping/src/tennis/atp_athens.py

from ._scraper_utils import scrape_league


def scrape_atp_athens():
    """Scrape ATP Athens"""
    return scrape_league(
        league_name="ATP Athens",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/atp-athenes",
        display_name="ATP Athens"
    )
