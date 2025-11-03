# scraping/src/tennis/wta_hong_kong.py

from ._scraper_utils import scrape_league


def scrape_wta_hong_kong():
    """Scrape WTA Hong Kong"""
    return scrape_league(
        league_name="WTA Hong Kong",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-hong-kong",
        display_name="WTA Hong Kong"
    )
