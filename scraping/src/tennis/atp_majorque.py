# scraping/src/tennis/atp_majorque.py

from ._scraper_utils import scrape_league


def scrape_atp_majorque():
    """Scrape ATP Majorque"""
    return scrape_league(
        league_name="ATP Majorque",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-majorque",
        display_name="ATP Majorque"
    )
