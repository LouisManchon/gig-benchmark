# scraping/src/tennis/atp_gstaad.py

from ._scraper_utils import scrape_league


def scrape_atp_gstaad():
    """Scrape ATP Gstaad"""
    return scrape_league(
        league_name="ATP Gstaad",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-gstaad",
        display_name="ATP Gstaad"
    )
