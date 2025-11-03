# scraping/src/tennis/atp_madrid.py

from ._scraper_utils import scrape_league


def scrape_atp_madrid():
    """Scrape ATP Madrid"""
    return scrape_league(
        league_name="ATP Madrid",
        league_url="https://www.coteur.com/cotes/tennis/monde/masters-madrid",
        display_name="ATP Madrid"
    )
