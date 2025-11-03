# scraping/src/tennis/wta_tokyo.py

from ._scraper_utils import scrape_league


def scrape_wta_tokyo():
    """Scrape WTA Tokyo"""
    return scrape_league(
        league_name="WTA Tokyo",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-tokyo",
        display_name="WTA Tokyo"
    )
