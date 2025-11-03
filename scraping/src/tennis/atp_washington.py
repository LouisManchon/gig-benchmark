# scraping/src/tennis/atp_washington.py

from ._scraper_utils import scrape_league


def scrape_atp_washington():
    """Scrape ATP Washington"""
    return scrape_league(
        league_name="ATP Washington",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-washington",
        display_name="ATP Washington"
    )
