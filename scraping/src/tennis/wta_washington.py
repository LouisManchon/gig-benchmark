# scraping/src/tennis/wta_washington.py

from ._scraper_utils import scrape_league


def scrape_wta_washington():
    """Scrape WTA Washington"""
    return scrape_league(
        league_name="WTA Washington",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-washington",
        display_name="WTA Washington"
    )
