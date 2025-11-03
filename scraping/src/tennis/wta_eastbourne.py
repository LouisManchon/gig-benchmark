# scraping/src/tennis/wta_eastbourne.py

from ._scraper_utils import scrape_league


def scrape_wta_eastbourne():
    """Scrape WTA Eastbourne"""
    return scrape_league(
        league_name="WTA Eastbourne",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-eastbourne",
        display_name="WTA Eastbourne"
    )
