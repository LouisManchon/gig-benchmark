# scraping/src/football/urvalsdeild.py

from ._scraper_utils import scrape_league


def scrape_urvalsdeild():
    """Scrape Urvalsdeild"""
    return scrape_league(
        league_name="Urvalsdeild",
        league_url="https://www.coteur.com/cotes/foot/islande/urvalsdeild",
        display_name="Urvalsdeild"
    )
