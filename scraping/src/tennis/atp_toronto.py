# scraping/src/tennis/atp_toronto.py

from ._scraper_utils import scrape_league


def scrape_atp_toronto():
    """Scrape ATP Toronto"""
    return scrape_league(
        league_name="ATP Toronto",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-toronto",
        display_name="ATP Toronto"
    )
