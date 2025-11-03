# scraping/src/tennis/wta_chennai.py

from ._scraper_utils import scrape_league


def scrape_wta_chennai():
    """Scrape WTA Chennai"""
    return scrape_league(
        league_name="WTA Chennai",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-chennai",
        display_name="WTA Chennai"
    )
