# scraping/src/tennis/wta_madrid.py

from ._scraper_utils import scrape_league


def scrape_wta_madrid():
    """Scrape WTA Madrid"""
    return scrape_league(
        league_name="WTA Madrid",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-madrid",
        display_name="WTA Madrid"
    )
