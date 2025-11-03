# scraping/src/tennis/atp_bastad.py

from ._scraper_utils import scrape_league


def scrape_atp_bastad():
    """Scrape ATP Bastad"""
    return scrape_league(
        league_name="ATP Bastad",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-bastad",
        display_name="ATP Bastad"
    )
