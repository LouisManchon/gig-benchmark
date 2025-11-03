# scraping/src/tennis/atp_us_open.py

from ._scraper_utils import scrape_league


def scrape_atp_us_open():
    """Scrape ATP US Open"""
    return scrape_league(
        league_name="ATP US Open",
        league_url="https://www.coteur.com/cotes/tennis/monde/us-open",
        display_name="ATP US Open"
    )
