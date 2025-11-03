# scraping/src/tennis/wta_montreal.py

from ._scraper_utils import scrape_league


def scrape_wta_montreal():
    """Scrape WTA Montreal"""
    return scrape_league(
        league_name="WTA Montreal",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-montreal",
        display_name="WTA Montreal"
    )
