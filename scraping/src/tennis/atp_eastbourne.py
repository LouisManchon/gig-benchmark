# scraping/src/tennis/atp_eastbourne.py

from ._scraper_utils import scrape_league


def scrape_atp_eastbourne():
    """Scrape ATP Eastbourne"""
    return scrape_league(
        league_name="ATP Eastbourne",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-eastbourne",
        display_name="ATP Eastbourne"
    )
