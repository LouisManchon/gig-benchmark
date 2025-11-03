# scraping/src/tennis/atp_rome.py

from ._scraper_utils import scrape_league


def scrape_atp_rome():
    """Scrape ATP Rome"""
    return scrape_league(
        league_name="ATP Rome",
        league_url="https://www.coteur.com/cotes/tennis/monde/masters-atp-rome",
        display_name="ATP Rome"
    )
