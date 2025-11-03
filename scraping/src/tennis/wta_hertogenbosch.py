# scraping/src/tennis/wta_hertogenbosch.py

from ._scraper_utils import scrape_league


def scrape_wta_hertogenbosch():
    """Scrape WTA Hertogenbosch"""
    return scrape_league(
        league_name="WTA Hertogenbosch",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-s-hertogenbosch",
        display_name="WTA Hertogenbosch"
    )
