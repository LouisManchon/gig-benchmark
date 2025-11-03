# scraping/src/tennis/atp_munich.py

from ._scraper_utils import scrape_league


def scrape_atp_munich():
    """Scrape ATP Munich"""
    return scrape_league(
        league_name="ATP Munich",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-munich",
        display_name="ATP Munich"
    )
