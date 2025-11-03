# scraping/src/tennis/atp_basel.py

from ._scraper_utils import scrape_league


def scrape_atp_basel():
    """Scrape ATP Basel"""
    return scrape_league(
        league_name="ATP Basel",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-bale",
        display_name="ATP Basel"
    )
