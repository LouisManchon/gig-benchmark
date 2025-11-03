# scraping/src/tennis/atp_hambourg.py

from ._scraper_utils import scrape_league


def scrape_atp_hambourg():
    """Scrape ATP Hambourg"""
    return scrape_league(
        league_name="ATP Hambourg",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-hambourg",
        display_name="ATP Hambourg"
    )
