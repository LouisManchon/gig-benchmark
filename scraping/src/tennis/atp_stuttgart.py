# scraping/src/tennis/atp_stuttgart.py

from ._scraper_utils import scrape_league


def scrape_atp_stuttgart():
    """Scrape ATP Stuttgart"""
    return scrape_league(
        league_name="ATP Stuttgart",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-stuttgart",
        display_name="ATP Stuttgart"
    )
