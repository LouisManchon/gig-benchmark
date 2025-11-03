# scraping/src/tennis/atp_houston.py

from ._scraper_utils import scrape_league


def scrape_atp_houston():
    """Scrape ATP Houston"""
    return scrape_league(
        league_name="ATP Houston",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-houston",
        display_name="ATP Houston"
    )
