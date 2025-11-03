# scraping/src/tennis/atp_barcelone.py

from ._scraper_utils import scrape_league


def scrape_atp_barcelone():
    """Scrape ATP Barcelone"""
    return scrape_league(
        league_name="ATP Barcelone",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-barcelone",
        display_name="ATP Barcelone"
    )
