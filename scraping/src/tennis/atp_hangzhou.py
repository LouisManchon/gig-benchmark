# scraping/src/tennis/atp_hangzhou.py

from ._scraper_utils import scrape_league


def scrape_atp_hangzhou():
    """Scrape ATP Hangzhou"""
    return scrape_league(
        league_name="ATP Hangzhou",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/atp-hangzhou",
        display_name="ATP Hangzhou"
    )
