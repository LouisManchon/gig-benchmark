# scraping/src/tennis/atp_marrakech.py

from ._scraper_utils import scrape_league


def scrape_atp_marrakech():
    """Scrape ATP Marrakech"""
    return scrape_league(
        league_name="ATP Marrakech",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-marrakech",
        display_name="ATP Marrakech"
    )
