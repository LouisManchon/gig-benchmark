# scraping/src/tennis/atp_almaty.py

from ._scraper_utils import scrape_league


def scrape_atp_almaty():
    """Scrape ATP Almaty"""
    return scrape_league(
        league_name="ATP Almaty",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/atp-almaty",
        display_name="ATP Almaty"
    )
