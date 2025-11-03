# scraping/src/tennis/wta_us_open.py

from ._scraper_utils import scrape_league


def scrape_wta_us_open():
    """Scrape WTA US Open"""
    return scrape_league(
        league_name="WTA US Open",
        league_url="https://www.coteur.com/cotes/tennis/monde/us-open-femmes",
        display_name="WTA US Open"
    )
