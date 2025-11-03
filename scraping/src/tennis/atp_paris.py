# scraping/src/tennis/atp_paris.py

from ._scraper_utils import scrape_league


def scrape_atp_paris():
    """Scrape ATP Paris"""
    return scrape_league(
        league_name="ATP Paris",
        league_url="https://www.coteur.com/cotes/tennis/monde/masters-paris",
        display_name="ATP Paris"
    )
