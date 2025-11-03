# scraping/src/tennis/wta_rome.py

from ._scraper_utils import scrape_league


def scrape_wta_rome():
    """Scrape WTA Rome"""
    return scrape_league(
        league_name="WTA Rome",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-rome",
        display_name="WTA Rome"
    )
