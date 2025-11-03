# scraping/src/tennis/wta_us_open_double.py

from ._scraper_utils import scrape_league


def scrape_wta_us_open_double():
    """Scrape WTA US Open - Double"""
    return scrape_league(
        league_name="WTA US Open - Double",
        league_url="https://www.coteur.com/cotes/tennis/monde/us-open-doubles-femmes",
        display_name="WTA US Open - Double"
    )
