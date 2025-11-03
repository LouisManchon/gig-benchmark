# scraping/src/tennis/wta_nottingham.py

from ._scraper_utils import scrape_league


def scrape_wta_nottingham():
    """Scrape WTA Nottingham"""
    return scrape_league(
        league_name="WTA Nottingham",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-nottingham",
        display_name="WTA Nottingham"
    )
