# scraping/src/tennis/wimbledon_double_x.py

from ._scraper_utils import scrape_league


def scrape_wimbledon_double_x():
    """Scrape Wimbledon Double X"""
    return scrape_league(
        league_name="Wimbledon Double X",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-wimbledon-doubles-mixte",
        display_name="Wimbledon Double X"
    )
