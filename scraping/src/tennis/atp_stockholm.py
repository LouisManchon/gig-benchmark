# scraping/src/tennis/atp_stockholm.py

from ._scraper_utils import scrape_league


def scrape_atp_stockholm():
    """Scrape ATP Stockholm"""
    return scrape_league(
        league_name="ATP Stockholm",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-stockholm",
        display_name="ATP Stockholm"
    )
