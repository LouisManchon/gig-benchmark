# scraping/src/tennis/atp_us_open_double.py

from ._scraper_utils import scrape_league


def scrape_atp_us_open_double():
    """Scrape ATP US Open - Double"""
    return scrape_league(
        league_name="ATP US Open - Double",
        league_url="https://www.coteur.com/cotes/tennis/monde/us-open-double-hommes",
        display_name="ATP US Open - Double"
    )
