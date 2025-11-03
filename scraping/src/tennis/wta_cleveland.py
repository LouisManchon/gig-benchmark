# scraping/src/tennis/wta_cleveland.py

from ._scraper_utils import scrape_league


def scrape_wta_cleveland():
    """Scrape WTA Cleveland"""
    return scrape_league(
        league_name="WTA Cleveland",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-cleveland",
        display_name="WTA Cleveland"
    )
