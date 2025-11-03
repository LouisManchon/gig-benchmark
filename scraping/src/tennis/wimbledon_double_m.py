# scraping/src/tennis/wimbledon_double_m.py

from ._scraper_utils import scrape_league


def scrape_wimbledon_double_m():
    """Scrape Wimbledon Double M"""
    return scrape_league(
        league_name="Wimbledon Double M",
        league_url="https://www.coteur.com/cotes/tennis/monde/wimbledon-doubles-hommes",
        display_name="Wimbledon Double M"
    )
