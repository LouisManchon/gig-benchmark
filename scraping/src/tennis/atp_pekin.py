# scraping/src/tennis/atp_pekin.py

from ._scraper_utils import scrape_league


def scrape_atp_pekin():
    """Scrape ATP Pékin"""
    return scrape_league(
        league_name="ATP Pékin",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-pekin",
        display_name="ATP Pékin"
    )
