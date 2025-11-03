# scraping/src/tennis/atp_vienne.py

from ._scraper_utils import scrape_league


def scrape_atp_vienne():
    """Scrape ATP Vienne"""
    return scrape_league(
        league_name="ATP Vienne",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-vienne",
        display_name="ATP Vienne"
    )
