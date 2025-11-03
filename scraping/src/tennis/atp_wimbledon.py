# scraping/src/tennis/atp_wimbledon.py

from ._scraper_utils import scrape_league


def scrape_atp_wimbledon():
    """Scrape ATP Wimbledon"""
    return scrape_league(
        league_name="ATP Wimbledon",
        league_url="https://www.coteur.com/cotes/tennis/monde/wimbledon-simples-hommes",
        display_name="ATP Wimbledon"
    )
