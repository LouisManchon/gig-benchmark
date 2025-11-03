# scraping/src/tennis/atp_umag.py

from ._scraper_utils import scrape_league


def scrape_atp_umag():
    """Scrape ATP Umag"""
    return scrape_league(
        league_name="ATP Umag",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-umag",
        display_name="ATP Umag"
    )
