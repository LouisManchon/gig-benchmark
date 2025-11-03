# scraping/src/tennis/wta_berlin.py

from ._scraper_utils import scrape_league


def scrape_wta_berlin():
    """Scrape WTA Berlin"""
    return scrape_league(
        league_name="WTA Berlin",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-berlin",
        display_name="WTA Berlin"
    )
