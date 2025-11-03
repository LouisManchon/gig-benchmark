# scraping/src/tennis/atp_halle.py

from ._scraper_utils import scrape_league


def scrape_atp_halle():
    """Scrape ATP Halle"""
    return scrape_league(
        league_name="ATP Halle",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-halle",
        display_name="ATP Halle"
    )
