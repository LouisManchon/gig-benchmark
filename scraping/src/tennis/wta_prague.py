# scraping/src/tennis/wta_prague.py

from ._scraper_utils import scrape_league


def scrape_wta_prague():
    """Scrape WTA Prague"""
    return scrape_league(
        league_name="WTA Prague",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-prague",
        display_name="WTA Prague"
    )
