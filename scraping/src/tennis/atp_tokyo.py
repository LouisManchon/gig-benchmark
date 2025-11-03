# scraping/src/tennis/atp_tokyo.py

from ._scraper_utils import scrape_league


def scrape_atp_tokyo():
    """Scrape ATP Tokyo"""
    return scrape_league(
        league_name="ATP Tokyo",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-tokyo",
        display_name="ATP Tokyo"
    )
