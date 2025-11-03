# scraping/src/tennis/wimbledon_double_w.py

from ._scraper_utils import scrape_league


def scrape_wimbledon_double_w():
    """Scrape Wimbledon Double W"""
    return scrape_league(
        league_name="Wimbledon Double W",
        league_url="https://www.coteur.com/cotes/tennis/monde/wimbledon-doubles-dames",
        display_name="Wimbledon Double W"
    )
